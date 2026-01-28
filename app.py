import streamlit as st
import replicate
import os
import requests
import tempfile

# Force UTF-8 encoding for the system
import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# App Configuration
st.set_page_config(page_title="AI Video Transformer", page_icon="🎬")

st.title("🎬 AI Video Transformation")
st.write("Convert your videos into unique styles using AI (Copyright-Safe).")

# Retrieve API Token from Streamlit Secrets or Sidebar
if "REPLICATE_API_TOKEN" in st.secrets:
    replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]
else:
    replicate_api_token = st.sidebar.text_input("Enter Replicate API Token:", type="password")

os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

# Video Upload Section
uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov"])

# Prompt and Style Settings
prompt = st.text_area("Transformation Prompt:", "Transform to cinematic style, high quality, vibrant colors")
style = st.selectbox("Choose Style:", ["Cinematic", "Anime", "Cyberpunk", "Sketch"])

if st.button("Start Transformation"):
    if not replicate_api_token:
        st.error("Please provide a Replicate API Token in the sidebar or secrets!")
    elif uploaded_file is not None:
        with st.spinner("Processing... This may take 1-3 minutes."):
            try:
                # Use a temporary file with English-only naming to avoid ASCII errors
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    video_path = tmp_file.name

                # Run the AI Model (AnimateDiff)
                with open(video_path, "rb") as f:
                    output = replicate.run(
                        "lucataco/animate-diff:be05c13e691373a6895d3f3bc540e1a63f10137a177c3d2bdc2d30c45aa70739",
                        input={
                            "video": f,
                            "prompt": f"{prompt}, {style} style, high quality, unique textures",
                            "negative_prompt": "low quality, blurry, original pixels, duplicate"
                        }
                    )
                
                if output:
                    st.success("Transformation Successful!")
                    st.video(output)
                    
                    # Download Button
                    video_data = requests.get(output).content
                    st.download_button(
                        label="Download Transformed Video", 
                        data=video_data, 
                        file_name="transformed_video.mp4", 
                        mime="video/mp4"
                    )
                
                # Cleanup: Delete the temporary file
                os.unlink(video_path)

            except Exception as e:
                # Display error in English
                st.error(f"System Error: {str(e)}")
    else:
        st.warning("Please upload a video file first.")
