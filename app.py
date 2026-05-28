import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io
import os

# -------------------------------
# CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI Image Description Generator",
    page_icon="🖼️",
    layout="wide"
)

# -------------------------------
# API KEY
# -------------------------------

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

# -------------------------------
# TITLE
# -------------------------------

st.title("🖼️ AI Image Description & Alt-Text Generator")

st.markdown("""
Upload up to 5 images and generate:

- Accessibility Alt-Text
- Detailed Description
- SEO Caption
""")

# -------------------------------
# FILE UPLOAD
# -------------------------------

uploaded_files = st.file_uploader(
    "Upload Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# -------------------------------
# PROCESS IMAGES
# -------------------------------

results = []

if uploaded_files:

    if len(uploaded_files) > 5:
        st.error("Please upload a maximum of 5 images.")
    else:

        for uploaded_file in uploaded_files:

            image = Image.open(uploaded_file)

            st.image(image, caption=uploaded_file.name, use_container_width=True)

            prompt = """
            Analyze this image and generate:

            1. Brief accessibility alt-text (1 sentence)
            2. Detailed image description
            3. SEO-friendly caption

            Format:
            Alt-Text:
            Description:
            SEO Caption:
            """

            with st.spinner(f"Generating content for {uploaded_file.name}..."):

                response = model.generate_content(
                    [prompt, image]
                )

                output = response.text

                st.markdown("### Generated Result")
                st.write(output)

                results.append({
                    "Image Name": uploaded_file.name,
                    "Generated Output": output
                })

# -------------------------------
# EXPORT CSV
# -------------------------------

if results:

    df = pd.DataFrame(results)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="image_descriptions.csv",
        mime="text/csv"
    )
