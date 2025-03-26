import pandas as pd
from pathlib import Path
import numpy as np
import os
import glob
import cv2
import math, sys
import json

collection_name = "Mathews"
#########################################
if collection_name == "CASEBolton":
    num_points = 25
elif collection_name == "Mathews":
    num_points = 24
else:
    print("error number points!!")
    sys.exit()

#### input

csv_file_path1 = (
    "C:/Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_annoted_positions.csv"
)

images_folder1 = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/cropped/"
    + collection_name
    + "_cropped/"
)

landmarks_path1 = (
    "C://Users/Phoebus/Desktop/DIP_Project/Landmarks_CSV/" + collection_name + "/"
)

annot_landmarks_path = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_annoted_positions.csv"
)

#### output

merge_df_path = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_merge_df.csv"
)

merge_df_path2 = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_images_info.csv"
)

dataset_path1 = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_dataset_forCNN.csv"
)
# npz
arrays_path = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_arrays.npz"
)
##########################################


def full_name(list_institu, list_sers, list_side, list_order, list_lebal):
    name = (
        list_institu
        + "_"
        + list_sers
        + "_"
        + list_side
        + "_"
        + list_order
        + "_"
        + list_lebal
    )
    return name


csv_file_path = csv_file_path1


df = pd.read_csv(csv_file_path)

filename_list = df["filename"].tolist()

SELLA_list = df["sella"].apply(lambda x: eval(x)).tolist()
NASION_list = df["nasion"].apply(lambda x: eval(x)).tolist()

# print("Filename list:", filename_list)
# print("SELLA_list:", SELLA_list)
# print("NASION_list:", NASION_list)


images_folder = images_folder1

landmarks_path = landmarks_path1
# landmarks_path = "./together_data/B0113_crop/B0113.csv"
# landmarks_df = pd.read_csv(landmarks_path)


list_institu = []
list_sers = []
list_side = []
list_order = []
list_label = []
list_filename = []
list_full_path = []

for filename in os.listdir(images_folder):

    if filename.endswith(".png"):
        result = filename.split("_")
        list_institu.append(result[0])
        list_sers.append(result[1])
        list_side.append(result[2])
        list_order.append(result[3])
        list_label.append(result[4])
        list_filename.append(filename)
        list_full_path.append(
            images_folder
            + full_name(result[0], result[1], result[2], result[3], result[4])
        )

imagesInfo = {
    "institu": list_institu,
    "sers": list_sers,
    "side": list_side,
    "order": list_order,
    "label": list_label,
    "filename": list_filename,
    "full_path": list_full_path,
    "relative_positions": np.nan,
    "absolute_positions": np.nan,
    "normalized_no_label_image": np.nan,
}
df_images = pd.DataFrame(imagesInfo)


annot_landmarks_df = pd.read_csv(annot_landmarks_path)

merge_df = pd.merge(df_images, annot_landmarks_df, on="filename")
merge_df.to_csv(merge_df_path, index=False)
# print(merge_df)


images_list = []
landmark_list = []
filename_set_list = []
index_flag = 0

for index, row in merge_df.iterrows():
    index_flag = index

    # if index >= 100:
    #     break
    print("-----dealing：" + str(index + 1) + "/" + str(len(merge_df)))
    print(index, row["order"], row["filename"])

    landmarks_df = pd.read_csv(
        landmarks_path + row["institu"] + "_" + row["sers"] + "_Tables.csv"
    )

    x_order = "X" + row["order"]
    y_order = "Y" + row["order"]
    x_data = landmarks_df[x_order]
    y_data = landmarks_df[y_order]

    y_data = -y_data

    relative_positions = list(x_data) + list(y_data)
    merge_df.at[index, "relative_positions"] = str(relative_positions)
    # merge_df.to_csv("merge_df2.csv", index=False)
    # print(x_data)
    # print(y_data)

    ###############
    def preprocess_image_with_opencv(image_path):

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        image_array = image.astype("float32") / 255.0
        return image_array

    modif_fullpath = row["full_path"].rstrip("WithLabel.png") + "NoLabel.png"
    image = preprocess_image_with_opencv(modif_fullpath)

    merge_df.at[index, "normalized_no_label_image"] = str(image)

    cord = eval(row["sella"])
    x_SELLA_fix = cord[0]
    y_SELLA_fix = cord[1]
    cord = eval(row["nasion"])
    x_NASION_fix = cord[0]
    y_NASION_fix = cord[1]

    index_SELLA = 0
    index_NASION = 1
    x_SELLA_rel, y_SELLA_rel = x_data[index_SELLA], y_data[index_SELLA]
    x_NASION_rel, y_NASION_rel = x_data[index_NASION], y_data[index_NASION]

    rel_vector = np.array([x_NASION_rel - x_SELLA_rel, y_NASION_rel - y_SELLA_rel])
    abs_vector = np.array([x_NASION_fix - x_SELLA_fix, y_NASION_fix - y_SELLA_fix])
    scale_factor = np.linalg.norm(abs_vector) / np.linalg.norm(rel_vector)
    rotation_angle = math.atan2(abs_vector[1], abs_vector[0]) - math.atan2(
        rel_vector[1], rel_vector[0]
    )

    def rotate_and_scale(x, y, angle, scale):
        rotated_x = (x * math.cos(angle) - y * math.sin(angle)) * scale
        rotated_y = (x * math.sin(angle) + y * math.cos(angle)) * scale
        return rotated_x, rotated_y

    x_data_transformed = []
    y_data_transformed = []
    for x_rel, y_rel in zip(x_data, y_data):
        x_rotated, y_rotated = rotate_and_scale(
            x_rel - x_SELLA_rel, y_rel - y_SELLA_rel, rotation_angle, scale_factor
        )
        x_abs = x_rotated + x_SELLA_fix
        y_abs = y_rotated + y_SELLA_fix
        # if np.any(np.isnan(x_abs)):
        #     print("----contents contain nan")
        x_data_transformed.append(x_abs)
        y_data_transformed.append(y_abs)

    x_data = x_data_transformed
    y_data = y_data_transformed

    if np.any(np.isnan(np.array((list(x_data) + list(y_data))))):
        print("--contents contain nan")
        continue

    x_array = np.array(x_data)
    y_array = np.array(y_data)

    if np.any(x_array <= 0) or np.any(y_array <= 0):
        print("--contents contain values less than 0")
        continue

    if np.any(x_array >= 700) or np.any(y_array >= 700):
        print("--contents contain values greater than 700")
        continue

    if len(x_array) != num_points or len(y_array) != num_points:
        print(
            "--either x_array or y_array does not contain exactly "
            + str(num_points)
            + " elements"
        )
        continue

    images_list.append(image)
    landmark_list.append(np.array((list(x_data) + list(y_data))))
    filename_set_list.append(row["filename"])
    # print(landmark_list)

    absolute_positions = list(x_data) + list(y_data)
    merge_df.at[index, "absolute_positions"] = str(absolute_positions)

    # print(landmark_list)
    # print(images_list)
    # print(filename_set_list)

# print(type(landmark_list))
# print(type(images_list))
# print(type(filename_set_list))
# print(landmark_list[0])
# print(images_list[0])
# print(filename_set_list[0])


merge_df.to_csv(merge_df_path2, index=False)


# print(landmark_list[-2])
# print(landmark_list[-1])
image_array = np.array(images_list)
landmark_array = np.array(landmark_list)
filename_array = np.array(filename_set_list)

############
np.savez(
    arrays_path,
    image_array=images_list,
    landmark_array=landmark_list,
    filename_array=filename_set_list,
)


#############################

df = pd.DataFrame(
    {
        "filenames": filename_set_list,
        "nomorlized_images(INPUT)": images_list,
        "fixed_positons_of_landmarks(OUTPUT)": landmark_list,
    }
)
csv_file_path = dataset_path1
df.to_csv(csv_file_path, index=False)


print("# of samples：", (index_flag + 1))
print("good samples：", len(images_list))
