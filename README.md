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

├── Code/
│   ├── chrome-win64/               # Automated downloading tool (Selenium-based)
│   ├── Landmarks_CSV/              # Downloaded landmark CSVs
│   ├── image/                      # Raw cephalogram images
│   ├── processCSV/                 # Processed data outputs
│   ├── best results code/         # Best training + model combo (final model)
│   ├── images web crawler.py      # Downloads images
│   ├── CSV web crawler.py         # Downloads landmark CSVs
│   ├── annote auto.py             # Auto-annotates reference points (Sella/Nasion)
│   ├── crop images.py             # Crops images to 800x800
│   ├── data_process.py            # Preprocessing, filtering, coordinate transform
│   └── combine_data.py            # Combines datasets
│
├── code_evaluation/               # Model evaluation & SDR / MSE analysis
│   └── evaluation.py              # Run this to get SDR and MSE results

## ⚙️ How to Use

The code is divided into two parts:

1. **Main pipeline** (`Code/` folder):  
   Includes downloading, preprocessing, CNN modeling, and training.

2. **Evaluation script** (`code_evaluation/` folder):  
   After training is completed, use this part to evaluate model performance based on SDR and MSE.
