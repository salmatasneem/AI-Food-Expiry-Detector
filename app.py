import streamlit as st
import easyocr
import cv2
import re
from datetime import datetime
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Food Expiry Detector", layout="centered")

st.title("🥫 AI Food Expiry Date Detector")
st.write("Detects Manufacturing Date (MFD) and Expiry Date (EXP) separately.")

# -----------------------------
# LOAD EASY OCR ONLY ONCE (Prevents Memory Crash)
# -----------------------------
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload Food Package Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:

    # Convert uploaded image to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # RESIZE IMAGE (VERY IMPORTANT - Prevents Memory Error)
    # -----------------------------
    max_width = 800
    height, width = gray.shape

    if width > max_width:
        scale = max_width / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        gray = cv2.resize(gray, (new_width, new_height))

    # -----------------------------
    # OCR PROCESS
    # -----------------------------
    result = reader.readtext(gray)

    detected_text = ""
    for detection in result:
        detected_text += detection[1] + " "

    st.subheader("📄 Detected Text:")
    st.write(detected_text)

    expiry_date = None
    mfd_date = None

    # -----------------------------
    # REGEX FOR EXPIRY DATE
    # -----------------------------
    exp_pattern = r'EXP[:\s]*([\d]{1,2}[/-][\d]{1,2}[/-][\d]{2,4}|[\d]{1,2}\s+[A-Z]{3,9}\s+\d{4})'
    exp_match = re.search(exp_pattern, detected_text, re.IGNORECASE)

    if exp_match:
        expiry_date_str = exp_match.group(1)
        st.success(f"📅 Expiry Date (EXP): {expiry_date_str}")

        date_formats = [
            "%d/%m/%Y", "%d-%m-%Y",
            "%d %b %Y", "%d %B %Y"
        ]

        for fmt in date_formats:
            try:
                expiry_date = datetime.strptime(expiry_date_str, fmt)
                break
            except:
                continue

    # -----------------------------
    # REGEX FOR MFD DATE
    # -----------------------------
    mfd_pattern = r'MFD[:\s]*([\d]{1,2}[/-][\d]{1,2}[/-][\d]{2,4}|[\d]{1,2}\s+[A-Z]{3,9}\s+\d{4})'
    mfd_match = re.search(mfd_pattern, detected_text, re.IGNORECASE)

    if mfd_match:
        mfd_date_str = mfd_match.group(1)
        st.info(f"🏭 Manufacturing Date (MFD): {mfd_date_str}")

        date_formats = [
            "%d/%m/%Y", "%d-%m-%Y",
            "%d %b %Y", "%d %B %Y"
        ]

        for fmt in date_formats:
            try:
                mfd_date = datetime.strptime(mfd_date_str, fmt)
                break
            except:
                continue

    # -----------------------------
    # CHECK EXPIRY STATUS
    # -----------------------------
    if expiry_date:
        today = datetime.today()
        days_left = (expiry_date - today).days

        st.subheader("⏳ Expiry Status:")

        if days_left < 0:
            st.error("⚠️ Product Expired!")
        elif days_left <= 3:
            st.warning("⚠️ Product Expiring Soon!")
        else:
            st.success(f"✅ Product Safe. Days Left: {days_left}")
    else:
        st.error("❌ No EXP date detected.")