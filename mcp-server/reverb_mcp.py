# server.py
from fastmcp import FastMCP
import openai
import requests
import yaml
from PIL import Image

# Load API key from config.yaml
with open("mcp_agent.secrets.yaml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["openai"]["api_key"]

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("add two numbers is working", a, b)
    return a + b * 2

from PIL import Image, ImageDraw, ImageFont

@mcp.tool
def add_banner_to_image(prompt: str, image_path: str) -> str:
    # Load the image
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    # Define banner size and colors
    banner_height = int(height * 0.15)  # Slightly taller to fit bigger text
    banner_color = (0, 0, 255, 255)  # Blue
    font_color = (255, 255, 255, 255)  # White

    # Create the banner overlay
    banner = Image.new("RGBA", (width, banner_height), banner_color)
    draw = ImageDraw.Draw(banner)

    # Load a bigger font (fallback to default if TTF font is unavailable)
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font = ImageFont.truetype(font_path, size=50)

    # Calculate text position using textbbox
    bbox = draw.textbbox((0, 0), prompt, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((width - text_width) // 2, (banner_height - text_height) // 2)

    # Draw text on banner
    draw.text(text_position, prompt, fill=font_color, font=font)

    # Combine banner and image
    combined = Image.new("RGBA", (width, height + banner_height))
    combined.paste(banner, (0, 0))
    combined.paste(image, (0, banner_height))

    # Save result
    output_path = "bannered.png"
    combined.save(output_path)
    print(f"[DEBUG] Saved image with banner to: {output_path}")

    return output_path





@mcp.tool
def gen_image(instructions: str, image_path: str) -> str:
    # Load main image and logo
    print(f"[DEBUG] Loading main image from: {image_path}")
    main_image = Image.open(image_path).convert("RGBA")

    print("[DEBUG] Loading watermark from: logo.png")
    watermark = Image.open("zapped.png").convert("RGBA")

    # Resize watermark if needed (optional)
    # watermark = watermark.resize((100, 100))

    # Calculate position for bottom-left
    padding = 10
    position = (padding, main_image.height - watermark.height - padding)

    # Composite watermark onto main image
    print(f"[DEBUG] Pasting watermark at: {position}")
    main_image.paste(watermark, position, watermark)  # Use watermark as mask for transparency

    # Save result
    output_path = "watermarked.png"
    main_image.save(output_path)
    print(f"[DEBUG] Saved watermarked image to: {output_path}")

    return output_path

@mcp.tool
def add_image_watermark(b64: str) -> str:
    """Add two numbers"""

    return b64

@mcp.prompt
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize the following text translating to french french:\n\n{text}"

if __name__ == "__main__":
    mcp.run()
