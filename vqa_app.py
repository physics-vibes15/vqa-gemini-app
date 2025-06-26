import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("🧠 Visual Question Answering with Gemini 1.5")
st.subheader("Upload an image")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    question = st.text_input("Ask a question about the image")

    if question and st.button("Get Answer"):
        try:
            uploaded_file.seek(0)  # Reset file pointer
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = model.generate_content(
                [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {"text": question}
                ]
            )
            st.success("Answer:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")

