# 🥫 AI Food Expiry Date Detector

The **AI Food Expiry Date Detector** is a Streamlit-based web application that detects **Manufacturing Date (MFD)** and **Expiry Date (EXP)** from food package images using **OCR (Optical Character Recognition)**.

This project helps users quickly verify product validity by uploading an image of the food package label. The system extracts text using **EasyOCR**, identifies date patterns using **Regular Expressions (Regex)**, and displays the expiry status based on the current date.

---

## 🚀 Features

- Upload food package images (JPG, PNG, JPEG)
- Extracts text from images using **EasyOCR**
- Detects:
  - 🏭 Manufacturing Date (MFD)
  - 📅 Expiry Date (EXP)
- Supports multiple date formats
- Shows product expiry status:
  - ✅ Safe
  - ⚠️ Expiring Soon
  - ❌ Expired
- User-friendly UI built with **Streamlit**
- Image resizing & preprocessing for improved performance

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **EasyOCR**
- **OpenCV**
- **Regex**
- **Datetime**
- **NumPy**

---

## 📌 How It Works

1. User uploads an image of a food product package.
2. The app preprocesses the image (grayscale + resizing).
3. OCR extracts all visible text from the label.
4. Regex patterns detect MFD and EXP values.
5. The system compares EXP date with today's date.
6. Expiry status is displayed with remaining days.

---

## 📷 Sample Output

- Detected Text from Image
- Expiry Date (EXP)
- Manufacturing Date (MFD)
- Expiry Status with alerts

---

