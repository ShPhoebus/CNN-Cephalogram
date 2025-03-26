import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from pathlib import Path
import numpy as np
import os
import glob


def select_points_from_image(image_path, num_points=2):

    # Loading and Displaying Images
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.title("Click on the image to select a point")

    # Use ginput to select points
    points = plt.ginput(
        num_points, timeout=-1
    )  # Set timeout = -1 to make the window wait until the specified number of clicks
    plt.close()

    # Returns the coordinates of the selected point
    return (points[0], points[1])


# Initialize the list of image data and callout data
label_list1 = []
label_list2 = []
filename_list = []

# Picture Folder Path
images_folder = (
    "C://Users/Phoebus/Desktop/DIP Orhan Project/code/together_data/B0113_label/"
)

# Traverse each picture in the folder
for image_path_filename in glob.glob(os.path.join(images_folder, "*.png")):
    # Get image file name
    image_filename = os.path.basename(image_path_filename)
    # Full pathname of the image
    image_fullpath = images_folder + image_filename

    # Pick a point
    position1, position2 = select_points_from_image(
        image_fullpath, num_points=2
    )  # Select 1 point

    # Add images and callouts to the list
    label_list1.append(position1)
    label_list2.append(position2)
    filename_list.append(image_filename)

# At this time,
# `images` is the input to the CNN model
# `landmarks` is the output target annotation of the model, each image corresponds to 50 positions: [X of Sella, X of NASION, X of porion..., Y of Sella, Y of NASION, YY of porion.......]

print(label_list1)
print(label_list2)
print(filename_list)

# label_list = [
# [(474.0002723083368, 279.5921658986174)],
# [(475.6978005865102, 306.7526183493925)],
# [(477.3953288646836, 311.84520318391276)],
# [(445.14229157938837, 315.2402597402597)],
# [(502.8582530372852, 254.12924172601583)],
# [(426.4694805194805, 262.61688311688306)],
# [(440.0497067448679, 330.51801424382063)],
# [(451.93240469208206, 298.26497695852527)],
# [(424.7719522413071, 301.6600335148721)],
# ]
# filename_list = [
# "B0113, Age 10y 0m, Sex M, Angle Class II, Image 6 of 15.png",
# "B0113, Age 11y 0m, Sex M, Angle Class II, Image 7 of 15.png",
# "B0113, Age 12y 0m, Sex M, Angle Class II, Image 8 of 15.png",
# "B0113, Age 13y 0m, Sex M, Angle Class II, Image 9 of 15.png",
# "B0113, Age 16y 0m, Sex M, Angle Class II, Image 12 of 15.png",
# "B0113, Age 18y 1m, Sex M, Angle Class II, Image 14 of 15.png",
# "B0113, Age 7y 0m, Sex M, Angle Class II, Image 3 of 15.png",
# "B0113, Age 8y 1m, Sex M, Angle Class II, Image 4 of 15.png",
# "B0113, Age 9y 0m, Sex M, Angle Class II, Image 5 of 15.png",
# ]

# Create DataFrame
df = pd.DataFrame(
    {
        "filename": filename_list,
        "SELLA_position": label_list1,
        "NASION_position": label_list2,
    }
)

# Save DataFrame as CSV file
csv_file_path = "positions.csv"  # Path to the CSV file you want to save
df.to_csv(csv_file_path, index=False)
