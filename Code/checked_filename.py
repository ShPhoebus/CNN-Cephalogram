import pandas as pd
import numpy as np
import os


images_folder = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/annoted_images/checked/CASEBolton"
)

images_folder2 = (
    "C://Users/Phoebus/Desktop/DIP_Project/images/annoted_images/checked/Mathews"
)

checked_filename_list = []


for filename in os.listdir(images_folder):

    if filename.endswith(".png"):
        result = filename[8:]

        checked_filename_list.append(result)


for filename in os.listdir(images_folder2):

    if filename.endswith(".png"):
        result = filename[8:]

        checked_filename_list.append(result)

print(len(checked_filename_list))
############
np.savez(
    "C://Users/Phoebus/Desktop/DIP_Project/processCSV/checked_filename_case_mathews.npz",
    checked_filename_list=checked_filename_list,
)
