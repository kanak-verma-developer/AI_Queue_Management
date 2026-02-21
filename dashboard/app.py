import os
import sys
import time
import random
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from fpdf import FPDF

# -----------------------------
# Fix Backend Import Path
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Fix: Added '# noqa: E402' to ignore module level import warning
from backend.queue_logic import (  # noqa: E402
    add_to_queue,
    call_next,
    get_queue,
    get_completed,
    reset_queue
)

from backend.detection import detect_people  # noqa: E402

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="AI Queue Management", layout="wide")
st.title("🚀 AI Smart Queue Management System")

# =========================================================
# 🔐 LOGIN SYSTEM
# =========================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.markdown("## 🔐 Admin Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.sidebar.success("Login Successful")
            st.rerun()
        else:
            st.sidebar.error("Invalid Credentials")

    st.warning("Please login to access system controls.")
    st.stop()

# Logout
if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# =========================================================
# Session State
# =========================================================
if "current_serving" not in st.session_state:
    st.session_state.current_serving = None

priority_choices = ["Normal", "Senior", "VIP", "Emergency"]

# =========================================================
# NOW SERVING SECTION
# =========================================================
st.markdown("---")

if st.session_state.current_serving:
    st.success(
        f"🟢 NOW SERVING: Token "
        f"{st.session_state.current_serving['Token']} - "
        f"{st.session_state.current_serving['Name']}"
    )
else:
    st.info("No token currently being served.")

st.markdown("---")

# =========================================================
# SIDEBAR CONTROLS
# =========================================================
mode = st.sidebar.selectbox("Select Mode", ["Image Upload", "Live Camera"])

st.sidebar.markdown("## 🎛 Queue Controls")

if st.sidebar.button("▶ Call Next Token"):
    next_person = call_next()
    if next_person:
        st.session_state.current_serving = next_person
        st.sidebar.success(f"Serving Token {next_person['Token']}")
    else:
        st.sidebar.warning("Queue is empty")

if st.sidebar.button("🔄 Reset Entire Queue"):
    reset_queue()
    st.session_state.current_serving = None
    st.sidebar.success("Queue Reset Successfully")

# =========================================================
# IMAGE UPLOAD MODE
# =========================================================
if mode == "Image Upload":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Crowd Image", type=["jpg", "png"]
    )
    process_button = st.sidebar.button("Process Image")

    if uploaded_file and process_button:
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()), dtype=np.uint8
        )
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            st.error("Invalid image file.")
        else:
            img = cv2.resize(img, (640, 480))
            processed_img, count = detect_people(img)

            st.metric("👥 People Detected", count)

            for i in range(count):
                name = f"P-{i+1:02d}"
                priority = random.choice(priority_choices)
                add_to_queue(name, priority)

            st.success(f"{count} people added to queue!")

            st.image(
                cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB),
                caption=f"Detected: {count} People",
                use_column_width=True,
            )

# =========================================================
# LIVE CAMERA MODE
# =========================================================
if mode == "Live Camera":
    run_camera = st.sidebar.checkbox("Start Camera")

    if run_camera:
        cap = cv2.VideoCapture(0)
        FRAME_WINDOW = st.image([])
        metric_placeholder = st.empty()

        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("Camera not working")
                break

            frame = cv2.resize(frame, (640, 480))
            processed_frame, count = detect_people(frame)

            FRAME_WINDOW.image(
                cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            )

            metric_placeholder.metric("👥 People Detected", count)
            time.sleep(0.2)

        cap.release()

# =========================================================
# MANUAL ADD SECTION
# =========================================================
st.sidebar.markdown("## ➕ Manual Entry")

name_input = st.sidebar.text_input("Name")
priority_input = st.sidebar.selectbox("Priority", priority_choices)
add_button = st.sidebar.button("Add Person")

if add_button and name_input.strip():
    token = add_to_queue(name_input, priority_input)
    st.sidebar.success(f"Token {token} assigned")

# =========================================================
# DISPLAY CURRENT QUEUE
# =========================================================
queue_data = get_queue()

if queue_data:
    df = pd.DataFrame(queue_data)

    st.markdown("## 📋 Current Queue")
    st.dataframe(df, use_container_width=True)

    total = len(df)
    emergency = sum(df["Priority"] == "Emergency")
    vip = sum(df["Priority"] == "VIP")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Waiting", total)
    col2.metric("Emergency Cases", emergency)
    col3.metric("VIP Cases", vip)

    if total > 0:
        avg_wait = sum((i + 1) * 3 for i in range(total)) / total
        # Fix: Added space after comma (E231)
        st.info(f"⏳ Average Waiting Time: {round(avg_wait, 2)} minutes")

    st.markdown("## 📊 Priority Distribution")
    chart_df = df["Priority"].value_counts().reset_index()
    chart_df.columns = ["Priority", "Count"]
    st.bar_chart(chart_df.set_index("Priority"))

    # Export
    st.sidebar.markdown("## 📥 Export Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="queue_data.csv",
        mime="text/csv",
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Queue Report", ln=True, align="C")

    for _, row in df.iterrows():
        line = f"Token {row['Token']} - {row['Name']} ({row['Priority']})"
        pdf.cell(200, 10, line, ln=True)

    pdf_path = os.path.join(BASE_DIR, "queue_report.pdf")
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.sidebar.download_button(
            label="Download PDF",
            data=f,
            file_name="queue_report.pdf",
            mime="application/pdf",
        )

# =========================================================
# COMPLETED HISTORY
# =========================================================
completed_data = get_completed()

if completed_data:
    st.markdown("## ✅ Completed Tokens")
    completed_df = pd.DataFrame(completed_data)
    st.dataframe(completed_df, use_container_width=True)