# -*- coding:utf-8 -*-

import cv2, os
import numpy as np

collection_name = "CASEBolton"
#############################
img_directory = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/original/" + collection_name + "/"
)
save_folder1 = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/annoted_images/"
    + collection_name
    + "/"
)
save_folder2 = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/fiducial_annoted_images/"
    + collection_name
    + "/"
)
save_folder3 = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_annoted_positions.csv"
)
save_folder4 = (
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
    + collection_name
    + "/"
    + collection_name
    + "_fiducial_annoted_positions.csv.csv"
)
# 1 for fudicial，0 for sella和nasion
fudicial_FLAG = 0
#############################


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


def auto_points(directory, list_institu, list_sers, list_side, list_order, list_lebal):

    full = full_name(list_institu, list_sers, list_side, list_order, list_lebal)
    filename = directory + full
    image = cv2.imread(filename)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # cv2.imshow("Points", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow("Points", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(image, (cX, cY), 2, (0, 255, 0), -1)

    # cv2.imshow("Result", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    points = []
    for cnt in contours:
        M = cv2.moments(cnt)
        # 计算质心
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            points.append((cx, cy))

    img_height, img_width = image.shape[:2]

    margin = 3

    points = [
        point
        for point in points
        if not (
            (
                point[1] <= margin
                and (point[0] <= margin or point[0] >= img_width - margin)
            )
        )
    ]

    if fudicial_FLAG == 0:
        #####################Sella，Nasion

        points_sorted = sorted(points, key=lambda x: x[1])
        points_filted_y = points_sorted[2:5]
        # print(points_filted_y)
        # for point in points_sorted:
        #     cv2.circle(image, point, radius=3, color=(0, 0, 255), thickness=-1)
        #
        #     cv2.imshow("Points", image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        points_sorted = sorted(points_filted_y, key=lambda x: x[0])
        points_filted_x = points_sorted[1:]
        # print(points_filted_x)
        # for point in points_filted_x:
        #     cv2.circle(image, point, radius=3, color=(0, 0, 255), thickness=-1)
        #
        #     cv2.imshow("Points", image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        # 确定哪个是Sella，哪个是Nasion
        sella = min(points_filted_x, key=lambda x: x[0])
        nasion = max(points_filted_x, key=lambda x: x[0])
        #####################Sella，Nasion结束

    if fudicial_FLAG == 1:
        #####################

        points_sorted = sorted(points, key=lambda x: x[0])

        points_filted_y = points_sorted[0:2]
        # print(points_filted_y)
        # for point in points_sorted:
        #     cv2.circle(image, point, radius=3, color=(0, 0, 255), thickness=-1)
        #
        #     cv2.imshow("Points", image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        points_sorted = sorted(points_filted_y, key=lambda x: x[1])
        points_filted_x = points_sorted
        # print(points_filted_x)
        # for point in points_filted_x:
        #     cv2.circle(image, point, radius=3, color=(0, 0, 255), thickness=-1)
        #     cv2.imshow("Points", image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        fiducial_b = min(points_filted_x, key=lambda x: x[1])
        fiducial_a = max(points_filted_x, key=lambda x: x[1])
        #####################

    # sella_x, sella_y = sella
    # nasion_x, nasion_y = nasion
    # sella_x_modified = sella_x + 1
    # sella_y_modified = sella_y - 1
    # nasion_x_modified = nasion_x + 1
    # nasion_y_modified = nasion_y - 1

    # sella = (sella_x_modified, sella_y_modified)
    # nasion = (nasion_x_modified, nasion_y_modified)
    # print("sella(x,y)=" + str(sella))
    # print("nasion(x,y)=" + str(nasion))

    if fudicial_FLAG == 0:

        # sella
        cv2.circle(image, sella, radius=2, color=(0, 0, 255), thickness=-1)
        # nasion
        cv2.circle(image, nasion, radius=2, color=(255, 0, 0), thickness=-1)
    if fudicial_FLAG == 1:
        # fiducial_b
        cv2.circle(image, fiducial_b, radius=2, color=(0, 0, 255), thickness=-1)
        # fiducial_a
        cv2.circle(image, fiducial_a, radius=2, color=(0, 0, 255), thickness=-1)

    # cv2.imshow("Sella and Nasion Points", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    if fudicial_FLAG == 0:

        positons.append((full, sella, nasion))

        filename2 = full
        anonot_filename = "annoted_" + filename2
        save_folder = save_folder1
        cv2.imwrite(str(save_folder + anonot_filename), image)
    if fudicial_FLAG == 1:

        positons.append((full, fiducial_a, fiducial_b))

        filename2 = full
        anonot_filename = "fiducial_annoted_" + filename2
        save_folder = save_folder2
        cv2.imwrite(str(save_folder + anonot_filename), image)


directory = img_directory
list_institu = []
list_sers = []
list_side = []
list_order = []
list_lebal = []
for filename in os.listdir(directory):

    if filename.endswith(".png"):
        result = filename.split("_")
        list_institu.append(result[0])
        list_sers.append(result[1])
        list_side.append(result[2])
        list_order.append(result[3])
        list_lebal.append(result[4])


positons = []


for index, key in enumerate(list_lebal):
    if key == "WithLabel.png":

        # if list_sers[index] == "B0277" and list_order[index] == "2":
        print("-----now dealing：" + str(index + 1) + "/" + str(len(list_lebal)))
        auto_points(
            directory,
            list_institu[index],
            list_sers[index],
            list_side[index],
            list_order[index],
            list_lebal[index],
        )


import pandas as pd

df = pd.DataFrame(positons)

if fudicial_FLAG == 0:
    df.columns = ["filename", "sella", "nasion"]

    df.to_csv(save_folder3, index=False)
if fudicial_FLAG == 1:
    df.columns = ["filename", "fiducial_a", "fiducial_b"]

    df.to_csv(save_folder4, index=False)
