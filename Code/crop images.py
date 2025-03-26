import cv2
import pandas as pd
from pathlib import Path
import numpy as np
import os
import glob

collection_name = "UTBurlington"

##############################################

crop_region = (0, 0, 800, 800)

images_folder = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/original/" + collection_name + "/"
)
target_path = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/cropped/"
    + collection_name
    + "_cropped/"
)
##############################################


def crop_image(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    x, y, width, height = crop_region
    cropped_image = image[y : y + height, x : x + width]
    return cropped_image


if not os.path.exists(target_path):
    os.makedirs(target_path)


list = glob.glob(os.path.join(images_folder, "*.png"))
for index, image_path_filename in enumerate(list):
    print("-----now dealing：" + str(index + 1) + "/" + str(len(list)))

    image_filename = os.path.basename(image_path_filename)

    image_fullpath = images_folder + image_filename

    cropped_image = crop_image(image_fullpath)

    cv2.imwrite(target_path + image_filename, cropped_image)
