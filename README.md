# CNN-Cephalogram

## 👥 Authors

- **Tianyi** 
- **Quevin** 

---

## 📝 Project Summary

**Landmark Annotation of Cephalograms using CNN**  
A deep learning-based solution for automated detection of anatomical landmarks in lateral cephalometric X-ray images. This tool streamlines the manual and error-prone process of identifying craniofacial reference points in dental imaging, leveraging the power of convolutional neural networks (CNNs).

---

## 📌 Overview

This project presents a Convolutional Neural Network model trained to predict over 20 craniofacial landmarks from cephalometric radiographs. It is designed to assist dental professionals with high-precision, automated annotation of lateral skull X-rays.

---

## 📁 Project Structure

```
├── Code/
│   ├── images web crawler.py       # Downloads images
│   ├── CSV web crawler.py          # Downloads landmark CSVs
│   ├── annote auto.py              # Auto-annotates reference points (Sella/Nasion)
│   ├── annote manually.py          # Manually annotate landmarks for selected images
│   ├── checked_filename.py         # Checks which annotation files have corresponding images
│   ├── crop images.py              # Crops images to 800x800
│   ├── data_process.py             # Preprocessing, filtering, coordinate transformation
│   ├── combine_data.py             # Combines multiple datasets
│   ├── CNN_Modeling.ipynb          # CNN training, prediction, visualization notebook
│   └── best_model.h5               # Final trained model for direct prediction
│
├── code_evaluation/               # Model evaluation & SDR / MSE analysis
```

---

## ⚙️ How to Use

The code is divided into two parts:

1. **Main pipeline** (`Code/` folder):  
Includes downloading, preprocessing, CNN modeling, and training.  
   There are **three ways to run** the pipeline:
   - **Option 1**: Use the scripts in the `Code/` folder to download and process image data, and generate `Mathews_arrays.npz` and `checked_filename_case_mathews.npz`. Then, load them into `CNN_Modeling.ipynb` for training and prediction.
   - **Option 2**: Directly load our pre-processed files `Mathews_arrays.npz` and `checked_filename_case_mathews.npz` into `CNN_Modeling.ipynb` without rerunning the entire preprocessing pipeline.
   - **Option 3**: Use parts of `CNN_Modeling.ipynb` to load the pretrained model `best_model.h5` and make predictions. In this case, input images must be preprocessed to match the expected format used in our training pipeline.


2. **Evaluation script** (`code_evaluation/` folder):  
   After training is completed, use this part to evaluate model performance based on SDR and MSE.


## 🧠 CNN_Modeling.ipynb Instructions

`CNN_Modeling.ipynb` is responsible for:
- Final data preprocessing  
- Data augmentation (brightness & contrast changes)  
- CNN model construction, training, and prediction  
- Visualizing predicted landmark positions on the original cephalometric images

#### 📂 Required Input Files

1. **`Mathews_arrays.npz`**  
   This file contains all processed image arrays and corresponding landmark labels.  
   🔗 [Download here](https://drive.google.com/drive/folders/16q40trNkZ3DX2L2LBb_b3oT76YWiaALf?usp=drive_link)

2. **`checked_filename_case_mathews.npz`**  
   This file provides a list of filenames with verified landmark annotations.  
   🔗 [Download here](https://drive.google.com/drive/folders/1P62Kaiw2NEr6_oJ3Wqhrt9xe8NW5hiR1?usp=drive_link)

3. **`best_model.h5`**  
   You can skip training and directly load the pre-trained model from this file.  
   📁 Available in the GitHub repository under `Code/`

#### 📤 Output Files Generated

Running `CNN_Modeling.ipynb` will generate the following CSVs for downstream evaluation:

- `dataset_prediction_labels.csv` – Predicted landmark coordinates  
- `dataset_ground_truth_labels.csv` – Ground truth landmark coordinates  
- `dataset_filename.csv` – Corresponding filenames for traceability

These files can be used as input for the accuracy evaluation script in the `code_evaluation/` folder.

---

📎 Data & Model Access
You can access all raw data, annotations, processed files, and model results from the following links:

1. **Original Cephalogram Images**  
   Raw cephalogram images from the Mathews dataset.  
   🔗 [Download here](https://drive.google.com/drive/folders/1_BglxT8Hd7vnMoLGQmr2bEitn2RuEuAA?usp=drive_link)

2. **Original CSV Landmark Annotations**  
   CSV files containing original annotated landmark coordinates.  
   🔗 [Download here](https://drive.google.com/drive/folders/1VtQbrxGptyeQSx9-rV2qJHkgH-xck1xI?usp=drive_link)

3. **Final CNN Model Prediction Results**  
   Predicted landmark coordinates generated by our trained CNN model (ready for evaluation).  
   🔗 [Download here](https://drive.google.com/drive/folders/1CcS_z0MO501looOrj4JBmM1pmQgrMGmp?usp=drive_link)

4. **Preprocessed Image and Dataset Files**  
   All intermediate results including checked filenames, preprocessed images, and label arrays.  
   🔗 [Download here](https://drive.google.com/drive/folders/1P62Kaiw2NEr6_oJ3Wqhrt9xe8NW5hiR1?usp=drive_link)




