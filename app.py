import streamlit as st
import replicate
import os
import requests
import tempfile

# កំណត់ទំព័រ App
st.set_page_config(page_title="AI Video Transformer", page_icon="🎬")

st.title("🎬 AI Video Transformation")
st.write("បំប្លែងវីដេអូឱ្យដាច់ Copyright ៩០% ដោយប្រើ AI")

# ទាញយក API Token ពី Streamlit Secrets (សុវត្ថិភាពជាង)
if "REPLICATE_API_TOKEN" in st.secrets:
    replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]
else:
    replicate_api_token = st.sidebar.text_input("បញ្ចូល Replicate API Token:", type="password")

os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

# ផ្នែក Upload វីដេអូ
uploaded_file = st.file_uploader("ជ្រើសរើសវីដេអូ (MP4, MOV)", type=["mp4", "mov"])

# ផ្នែកកំណត់ Prompt
prompt = st.text_area("Prompt (ពណ៌នាពីអ្វីដែលអ្នកចង់បាន):", "Transform to cinematic style, high quality, vibrant colors")
style = st.selectbox("ជ្រើសរើស Style:", ["Cinematic", "Anime", "Cyberpunk", "Sketch"])

if st.button("ចាប់ផ្ដើមបំប្លែង (Transform)"):
    if not replicate_api_token:
        st.error("សូមបញ្ចូល API Token ជាមុនសិន!")
    elif uploaded_file is not None:
        with st.spinner("កំពុងដំណើរការ... សូមរង់ចាំ (អាចប្រើពេល ១-៣ នាទី)"):
            try:
                # ដំណោះស្រាយ៖ បង្កើត File បណ្ដោះអាសន្នដែលមានឈ្មោះជាអង់គ្លេស ដើម្បីការពារ ASCII Error
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    video_path = tmp_file.name

                # បញ្ជាទៅ Replicate
                output = replicate.run(
                    "lucataco/animate-diff:be05c13e691373a6895d3f3bc540e1a63f10137a177c3d2bdc2d30c45aa70739",
                    input={
                        "video": open(video_path, "rb"),
                        "prompt": f"{prompt}, {style} style, high detail, copyright-free transformation",
                        "negative_prompt": "original footage, bad quality, blurry"
                    }
                )
                
                if output:
                    st.success("បំប្លែងជោគជ័យ!")
                    st.video(output)
                    
                    # ប៊ូតុងទាញយក
                    video_data = requests.get(output).content
                    st.download_button(label="ទាញយកវីដេអូ", data=video_data, file_name="transformed_video.mp4", mime="video/mp4")
                
                # លុប File បណ្ដោះអាសន្នចេញពី Server
                os.unlink(video_path)

            except Exception as e:
                st.error(f"មានបញ្ហា៖ {str(e)}")
    else:
        st.warning("សូម Upload វីដេអូជាមុនសិន!")
