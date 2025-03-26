import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle, sys

collection_name = "CASEBolton"

sample_index1 = 361


if False:
    ############

    if collection_name == "CASEBolton":
        num_points = 25
    elif collection_name == "Mathews":
        num_points = 24
    else:
        print("error number points!!")
        sys.exit()
    # 路径
    arrays_path = (
        "C://Users/Phoebus/Desktop/DIP_Project/processCSV/"
        + collection_name
        + "/"
        + collection_name
        + "_arrays.npz"
    )
else:
    ############# combine
    arrays_path = (
        "C://Users/Phoebus/Desktop/DIP_Project/processCSV/combine_arrays_0504.npz"
    )
    num_points = 21

loaded_arrays = np.load(arrays_path, allow_pickle=True)

image_array = loaded_arrays["image_array"]
landmark_array = loaded_arrays["landmark_array"]
filename_array = loaded_arrays["filename_array"]


sample_index = sample_index1
first_image = image_array[sample_index]

print(filename_array[sample_index])

coords = landmark_array[sample_index]

x_points = coords[:num_points]
y_points = coords[num_points:]
# print(x_points)
# print(y_points)


plt.figure(figsize=(10, 8))
plt.title(filename_array[sample_index])
plt.imshow(first_image, cmap="gray")
plt.scatter(x_points[0], y_points[0], s=1, color="red", label="SELLA")
plt.scatter(x_points[1], y_points[1], s=1, color="blue", label="NASION")
plt.scatter(x_points[2], y_points[2], s=1, color="green", label="PORION")
plt.scatter(x_points[3], y_points[3], s=1, color="yellow", label="ORBITALE")
plt.scatter(x_points[4], y_points[4], s=1, color="magenta", label="U_I_APEX")
plt.scatter(x_points[5], y_points[5], s=1, color="orange", label="POINT_A")

plt.legend()
plt.show()
######
