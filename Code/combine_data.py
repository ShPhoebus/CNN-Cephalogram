import pandas as pd
import numpy as np


# remain = 21


##########################   1

arrays_path = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/Mathews/Mathews_arrays.npz"
)
loaded_arrays = np.load(arrays_path, allow_pickle=True)

image_array = loaded_arrays["image_array"]
landmark_array = loaded_arrays["landmark_array"]
filename_array = loaded_arrays["filename_array"]


# Desired indices to keep (0-20 and 24-44 inclusive)
indices_to_keep = list(range(21)) + list(range(24, 45))
# Keep only the desired indices in the second dimension
filtered_landmark_array = landmark_array[:, indices_to_keep]

##########################   2

arrays_path2 = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/CASEBolton/CASEBolton_arrays.npz"
)
loaded_arrays2 = np.load(arrays_path2, allow_pickle=True)

image_array2 = loaded_arrays2["image_array"]
landmark_array2 = loaded_arrays2["landmark_array"]
filename_array2 = loaded_arrays2["filename_array"]


# Desired indices to keep (0-20 and 24-44 inclusive)
indices_to_keep = list(range(21)) + list(range(25, 46))
# Keep only the desired indices in the second dimension
filtered_landmark_array2 = landmark_array2[:, indices_to_keep]


# print(landmark_array[0])
# print(filtered_landmark_array[0])

#################3

image_array_c = np.concatenate((image_array, image_array2), axis=0)
landmark_array_c = np.concatenate(
    (filtered_landmark_array, filtered_landmark_array2), axis=0
)
filename_array_c = np.concatenate((filename_array, filename_array2), axis=0)


# print(image_array_c.shape)
# print(landmark_array_c.shape)
# print(filename_array_c.shape)

############
np.savez(
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/combine_arrays_0504.npz",
    image_array=image_array_c,
    landmark_array=landmark_array_c,
    filename_array=filename_array_c,
)


#############################

# df = pd.DataFrame(
#     {
#         "filenames": filename_array_c.tolist(),
#         "nomorlized_images(INPUT)": image_array_c.tolist(),
#         "fixed_positons_of_landmarks(OUTPUT)": landmark_array_c.tolist(),
#     }
# )
# df.to_csv(
#     "C://Users/Phoebus/Desktop/DIP_Project/processCSV/combine_dataset_forCNN.csv",
#     index=False,
# )
