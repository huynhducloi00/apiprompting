import argparse
from functools import partial
import json
import base64
import gradio as gr
import requests
from openai import OpenAI
import io

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
model_name='llava-hf/llava-v1.6-34b-hf'
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

            
def http_bot(args, image, prompt):
    base64_image=convert_to_base64(image)
    response = client.chat.completions.create(
        temperature=0,
        model=model_name,
        messages=[{
            "role": "user",
            "content": [
                # NOTE: The prompt formatting with the image token `<image>` is not needed
                # since the prompt will be processed automatically by the API server.
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image.decode('utf-8')}"}},
            ],
        }],
        stream=True
    )
    output=[]
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            output.append(chunk.choices[0].delta.content)
            yield "".join(output)
    
im = { 
  "background": "https://people.sc.fsu.edu/~jburkardt/data/png/dragon.png",
  "layers" : [],  
  "composite": None
}
def convert_to_base64(im):
  im1=im["composite"].convert('RGB')
  with io.BytesIO() as buffered:
    im1.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
  return img_str
def output_img(im):
    return im["composite"].convert('RGB')
def build_demo(args):
    with gr.Blocks() as demo:
        gr.Markdown("# Testing different models /Image prompt annotation improvments\n")
        btn = gr.Button("Submit")
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    picture_box=gr.ImageEditor(type='pil')
                    result_img=gr.Image()
                _ = gr.ClearButton(picture_box)
            # adjusted_box=gr.ImageEditor()
            with gr.Column():
                inputbox = gr.Textbox("What will the girl on the right write on the board?",label="Input",
                                    placeholder="Enter text and press ENTER"
                                    )
                outputbox = gr.Textbox(label="Output",
                                    lines=10, max_lines=12,
                                    placeholder="What output")
        
        picture_box.change(output_img, picture_box, result_img)
        btn.click(partial(http_bot,args),
                        [picture_box,inputbox],
                        outputbox
                        )
    return demo

total=0
def on_button_click():
    global total
    total+=1
    print(f"Button clicked! {total}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--port", type=int, default=32955)
    parser.add_argument("--model-name",
                        type=str,
                        default="llava-hf/llava-v1.6-34b-hf")
    parser.add_argument("--model-url",
                        type=str,
                        default="http://localhost:8000/v1/completions")
    args = parser.parse_args()
    # print(http_bot(args, '2+2='))
    
    demo = build_demo(args)
    
    demo.launch(server_name=args.host,
                        server_port=args.port,
                        share=True)


# headers = {"Content-Type": "application/json"}
    # pload = {
    #     "model": args.model_name,
    #     "prompt": prompt,
    #     "stream": True,
    #     "max_tokens": 128,
    #     'temperature':0,
    #     # "response_format":{"type":"text"}
    # }
    # response = requests.post(args.model_url,
    #                          headers=headers,
    #                          json=pload,
    #                          stream=True
    #                          )
    # print('xong:', curlify.to_curl(response.request)) 
    # return chat_response.choices[0].message.content
    # print(f"loi ", args.model_url,'\n',prompt, response)
    # concat=''
    # output=[]
    # for chunk in response.iter_lines():
    #     if chunk:
    #         text=chunk.decode()[5:]
    #         if '[DONE]' in text:
    #             break
    #         data = json.loads(text)
    #         output.append(data['choices'][0]['text'])
    #         # print('OUTPUT: ',output)
    #         yield "".join(output)
            # concat+=output
    # print('+'*10)
    # return concat
        # inputbox.submit(partial(http_bot,args), [inputbox], [outputbox])
        # gr.Examples([im], outputs=picture_box)
    