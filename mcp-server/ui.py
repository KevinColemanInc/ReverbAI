import streamlit as st
from PIL import Image
import io
import asyncio
import os
from main import call_agent

# --- Page Setup ---
st.set_page_config(page_title="ReverbAI", layout="wide")
st.title("🎨 ReverbAI – Logo Rebranding Agent")

# --- Session State for Chat History + Image Result ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_result_image" not in st.session_state:
    st.session_state.latest_result_image = None

# --- Image Upload Section ---
st.sidebar.header("📂 Upload Image File")
uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# --- Save uploaded image to temporary path ---
TEMP_PATH = "/tmp/reverbai_input.png"
if uploaded_file:
    with open(TEMP_PATH, "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.image(TEMP_PATH, caption="✅ Uploaded Image", use_column_width=True)

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="📷 Output Image")

# --- Chat Input ---
if user_prompt := st.chat_input("Describe your rebranding request (e.g. 'Replace Coke with MySoda')"):
    st.session_state.messages.append({
        "role": "user", "type": "text", "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        if not uploaded_file:
            st.warning("⚠️ Please upload an image first.")
        else:
            st.write("🔄 Running MCP agent...")

            try:
                # --- Call MCP Agent with saved image path ---
                result = asyncio.run(call_agent(TEMP_PATH, user_prompt))
                print("result from mcp: ", result)
                # Text Response
                st.session_state.messages.append({
                    "role": "assistant", "type": "text", "content": result.text
                })
                st.write(result.text)

                # Image Response
                if hasattr(result, "image_bytes") and result.image_bytes:
                    image = Image.open(io.BytesIO(result.image_bytes))
                    st.session_state.messages.append({
                        "role": "assistant", "type": "image", "content": image
                    })
                    st.session_state.latest_result_image = image  # store for below display
                    st.image(image, caption="📷 Rebranded Output")

            except Exception as e:
                error_msg = f"❌ Error during agent execution: {e}"
                st.session_state.messages.append({
                    "role": "assistant", "type": "text", "content": error_msg
                })
                st.error(error_msg)

# --- Section: Display Latest Result Image Separately ---
if st.session_state.latest_result_image:
    st.markdown("---")
    st.subheader("🖼️ Final Rebranded Image")
    st.image(st.session_state.latest_result_image, use_column_width=True)
