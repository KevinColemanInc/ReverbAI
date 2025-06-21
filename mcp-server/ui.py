import streamlit as st
from PIL import Image
import io
import asyncio

#from main import reverb_ai_mcp  # TODO: Make sure main.py exposes this function

# --- Page Setup ---
st.set_page_config(page_title="ReverbAI", layout="wide")
st.title("🎨 ReverbAI – Logo Rebranding Chat Agent")

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="Rebranded Output")

# --- Chat Input ---
if user_prompt := st.chat_input("Ask ReverbAI to rebrand your ad (e.g. 'Replace Coca-Cola with MySoda')"):
    st.session_state.messages.append({
        "role": "user", "type": "text", "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        st.write("🔄 Rebranding in progress...")

        try:
            # Call the MCP agent workflow
            result = asyncio.run(reverb_ai_mcp(user_prompt))

            # Add assistant's text response
            st.session_state.messages.append({
                "role": "assistant", "type": "text", "content": result.text
            })
            st.write(result.text)

            # Add assistant's image response (if any)
            if hasattr(result, "image_bytes") and result.image_bytes:
                image = Image.open(io.BytesIO(result.image_bytes))
                st.session_state.messages.append({
                    "role": "assistant", "type": "image", "content": image
                })
                st.image(image, caption="Rebranded Output")

        except Exception as e:
            error_msg = f"❌ Error during rebranding: {e}"
            st.session_state.messages.append({
                "role": "assistant", "type": "text", "content": error_msg
            })
            st.error(error_msg)


USE_MOCK = True  # Set to False when ready

if USE_MOCK:
    def reverb_ai_mcp(user_prompt):
        from types import SimpleNamespace
        from PIL import Image, ImageDraw
        import io

        img = Image.new("RGB", (400, 200), color="lightgray")
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), "Mock image: Logo replaced", fill="black")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return SimpleNamespace(
            text="✅ Mock: Successfully rebranded the advertisement.",
            image_bytes=buf.read()
        )
else:
    from main import reverb_ai_mcp
