import streamlit as st
import replicate
import os
import requests
import tempfile

# បង្ខំឱ្យប្រព័ន្ធប្រើ UTF-8 ជាដាច់ខាត
import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

st.set_page_config(page_title="AI Video Transformer", page_icon="🎬")

st.title("🎬 AI Video Transformation")
st.write("បំប្លែងវីដេអូឱ្យដាច់ Copyright ៩០% ដោយប្រើ AI")

# ទាញយក Token ពី Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]
else:
    replicate_api_token = st.sidebar.text_input("បញ្ចូល Replicate API Token:", type="password")

os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

uploaded_file = st.file_uploader("ជ្រើសរើសវីដេអូ", type=["mp4", "mov"])

prompt = st.text_area("Prompt:", "Transform to cinematic style, high quality, vibrant colors")
style = st.selectbox("Style:", ["Cinematic", "Anime", "Cyberpunk", "Sketch"])

if st.button("ចាប់ផ្ដើមបំប្លែង (Transform)"):
    if not replicate_api_token:
        st.error("សូមបញ្ចូល API Token!")
    elif uploaded_file is not None:
        with st.spinner("Processing..."):
            try:
                # ប្រើឈ្មោះ File បណ្ដោះអាសន្នជាភាសាអង់គ្លេសសុទ្ធ
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    video_path = tmp_file.name

                # បញ្ជូនទៅ Replicate (ប្រើ file object)
                with open(video_path, "rb") as f:
                    output = replicate.run(
                        "lucataco/animate-diff:be05c13e691373a6895d3f3bc540e1a63f10137a177c3d2bdc2d30c45aa70739",
                        input={
                            "video": f,
                            "prompt": prompt,
                            "negative_prompt": "low quality, original pixels"
                        }
                    )
                
                if output:
                    st.success("ជោគជ័យ!")
                    st.video(output)
                    video_data = requests.get(output).content
                    st.download_button(label="Download", data=video_data, file_name="result.mp4")
                
                os.unlink(video_path)
            except Exception as e:
                # បង្ហាញ Error ជាភាសាអង់គ្លេសដើម្បីកុំឱ្យ Error ជាន់ Error
                st.error(f"System Error: {str(e).encode('utf-8')}")
    else:
        st.warning("Please upload a video.")
