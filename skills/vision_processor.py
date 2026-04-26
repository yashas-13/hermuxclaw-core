import os
import json
import base64
import requests

META = {
    "name": "vision_processor",
    "version": "1.0",
    "description": "Processes images using small, efficient vision models (targeted for 0.5B - 2B).",
    "inputs": ["image_path", "prompt"],
    "outputs": ["analysis"]
}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def run(input_data):
    image_path = input_data.get("image_path")
    prompt = input_data.get("prompt", "What is in this image?")
    
    if not image_path or not os.path.exists(image_path):
        return {"status": "error", "message": "Image path missing or invalid."}

    print(f"[*] Vision Processor: Analyzing {os.path.basename(image_path)} with low-RAM optimized model...")

    try:
        from openai import OpenAI
        api_key = os.environ.get("NIM_API_KEY", "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")
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        # We use the smallest available multimodal/vision model on NIM
        # Although specifically asked for 0.5B, the closest on NIM are around 2-4B.
        # We use phi-3-vision as it is known for high efficiency in small sizes.
        target_model = "microsoft/phi-3-vision-128k-instruct"
        
        base64_image = encode_image(image_path)
        
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=512,
        )
        
        analysis = response.choices[0].message.content
        return {"status": "success", "analysis": analysis}
        
    except Exception as e:
        print(f"[!] Vision Processor Failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test with a dummy or existing image if available
    pass
