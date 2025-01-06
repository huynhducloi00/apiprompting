import gradio as gr
import numpy as np
import base64
from PIL import Image
from io import BytesIO

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def image_uploaded(img):
    # img_pil = Image.fromarray(img)
    # img_str = image_to_base64(img_pil)

    # img_str = f'data:image/png;base64,{img_str}'
    img_str = f'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png'
    
    # HTML content with a canvas element
    html_content = f"""
<h1>This is the img: img</h1>

<img id="image" src="{img_str}" alt="" onload="draw_image();">

<h1>This is the canvas: canvas</h1>

<canvas id="canvas" width="600"></canvas>

<button onclick="draw_image();" style="background-color:#eee;padding:25px">Draw Image</button>
"""

    return img, html_content

script = """s
/* this function is executed automatically at start (not when you load canvas) */
/* so draw_image() has to be inside (not in place of `async ()`) */
async () => {
    globalThis.draw_image = () => {
        var image  = document.getElementById("image");
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext('2d');
        ctx.drawImage(image, 0, 0);
    }
}
"""

with gr.Blocks(js=script) as demo:
    uploaded_image = gr.Image(type="numpy", show_label=False, interactive=True, show_download_button=False)
    original_image = gr.Image(type="numpy", interactive=False, show_label=False, show_download_button=False)

    bounding_box_editor = gr.HTML()
    
    uploaded_image.upload(image_uploaded, inputs=uploaded_image, outputs=[original_image, bounding_box_editor])
    
demo.launch(share=False, server_port=34851)