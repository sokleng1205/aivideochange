import streamlit as st
import replicate
import os
import requests
import tempfile

# Force UTF-8 encoding
import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

st.set_page_config(page_title="AI Video Pro Transformer", page_icon="🎬")

st.title("🎬 AI Video Transformation Pro")
st.write("Professional AI presets for high-quality, copyright-safe video.")

# API Token Logic
if "REPLICATE_API_TOKEN" in st.secrets:
    replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]
else:
    replicate_api_token = st.sidebar.text_input("Enter Replicate API Token:", type="password")

os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

# 1. Preset Definitions
STLYE_PRESETS = {
    "Studio Ghibli": "Studio Ghibli art style, hand-painted watercolor, lush green landscapes, soft natural lighting, Spirited Away aesthetic, masterpiece",
    "Spider-Verse": "Spider-man Into the Spider-Verse style, stylized 3D animation, halftone dot patterns, chromatic aberration, comic book ink lines, vibrant colors",
    "Cyberpunk 2077": "Futuristic cyberpunk aesthetic, neon glowing lights, rainy urban streets, high contrast, blade runner vibe, cinematic lighting",
    "90s Retro Anime": "90s vintage anime aesthetic, retro cel-shaded, slight film grain, Sailor Moon style, nostalgic colors",
    "Oil Painting": "Classic oil painting, thick brushstrokes, visible canvas texture, impasto technique, museum quality art",
    "Custom (Manual)": ""
}

# UI Layout
uploaded_file = st.file_uploader("Step 1: Upload Video", type=["mp4", "mov"])

# 2. Preset Selection
selected_preset = st.selectbox("Step 2: Choose Art Style", list(STLYE_PRESETS.keys()))

# 3. Prompt Logic
user_description = st.text_area("Step 3: Add specific details (optional):", placeholder="e.g. night time, snow falling, character wearing a suit")

if st.button("Start Transformation"):
    if not replicate_api_token:
        st.error("Missing API Token!")
    elif uploaded_file is not None:
        with st.spinner(f"Transforming into {selected_preset} style..."):
            try:
                # English-only temp filename to avoid ASCII crash
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    video_path = tmp_file.name

                # Combine Preset + User Input
                preset_keywords = STLYE_PRESETS[selected_preset]
                final_prompt = f"{user_description}, {preset_keywords}, 8k resolution, highly detailed, professional render"

                with open(video_path, "rb") as f:
                    output = replicate.run(
                        "lucataco/animate-diff:be05c13e691373a6895d3f3bc540e1a63f10137a177c3d2bdc2d30c45aa70739",
                        input={
                            "video": f,
                            "prompt": final_prompt,
                            "negative_prompt": "photorealistic, real life, low quality, blurry, duplicate, watermark"
                        }
                    )
                
                if output:
                    st.success("Done!")
                    st.video(output)
                    st.download_button("Download Result", requests.get(output).content, "transformed.mp4")
                
                os.unlink(video_path)
            except Exception as e:
                st.error(f"System Error: {str(e)}")
    else:
        st.warning("Please upload a file.")
