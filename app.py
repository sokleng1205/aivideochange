import streamlit as st
import replicate
import os
import requests

# រៀបចំទំព័រ App
st.set_page_config(page_title="AI Video Transformer", page_icon="🎬")

st.title("🎬 AI Video Transformation (Copyright-Safe)")
st.write("បំប្លែងវីដេអូរបស់អ្នកឱ្យមានស្ទីលថ្មីប្លែកដោយប្រើ AI")

# បញ្ចូល API Token
api_token = st.sidebar.text_input("បញ្ចូល Replicate API Token:", type="password")
os.environ["REPLICATE_API_TOKEN"] = api_token

# ផ្នែក Upload វីដេអូ
uploaded_file = st.file_uploader("ជ្រើសរើសវីដេអូពីក្នុងម៉ាស៊ីន (MP4, MOV)", type=["mp4", "mov"])

# ផ្នែកកំណត់ Prompt និង Style
prompt = st.text_area("Prompt (ពណ៌នាពីអ្វីដែលអ្នកចង់បំប្លែង):", "Transform to anime style, high quality, vibrant colors")
style = st.selectbox("ជ្រើសរើស Style:", ["Anime", "Cyberpunk", "Cinematic", "Sketch"])

if st.button("ចាប់ផ្ដើមបំប្លែង (Transform)"):
    if not api_token:
        st.error("សូមបញ្ចូល API Token ជាមុនសិន!")
    elif uploaded_file is not None:
        with st.spinner("កំពុងដំណើរការ... អាចប្រើពេល ១-៣ នាទី"):
            try:
                # ១. បង្ហោះវីដេអូទៅកាន់ Cloud ជាបណ្ដោះអាសន្ន (ឧទាហរណ៍ប្រើ Replicate direct upload)
                # ក្នុងករណី MVP នេះ យើងប្រើ Model AnimateDiff
                output = replicate.run(
                    "lucataco/animate-diff:be05c13e691373a6895d3f3bc540e1a63f10137a177c3d2bdc2d30c45aa70739",
                    input={
                        "video": uploaded_file,
                        "prompt": f"{prompt}, {style} style, 90% unique",
                        "negative_prompt": "original footage, low resolution"
                    }
                )
                
                if output:
                    st.success("បំប្លែងជោគជ័យ!")
                    st.video(output)
                    st.download_button("ទាញយកវីដេអូ", requests.get(output).content, file_name="transformed_video.mp4")
            except Exception as e:
                st.error(f"មានបញ្ហា: {e}")
    else:
        st.warning("សូម Upload វីដេអូជាមុនសិន!")