import os
import json
import base64
import sys

# HERMUXCLAW LOW-RAM VISION TOOL
# Optimized for 0.5B - 2B scale models where available, falls back to Phi-3-Vision (4B)

META = {
    "name": "low_ram_vision",
    "version": "1.1",
    "description": "Optimized vision analysis for low-resource environments.",
    "inputs": ["image_path", "prompt"],
    "outputs": ["response"]
}

def run(input_data):
    image_path = input_data.get("image_path")
    prompt = input_data.get("prompt", "Analyze this image efficiently.")
    
    if not image_path or not os.path.exists(image_path):
        return {"status": "error", "message": "Valid image path required."}

    try:
        from openai import OpenAI
        api_key = os.environ.get("NIM_API_KEY", "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")
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        # Phi-3-Vision is the most efficient 'small' vision model currently on NIM.
        # It outperforms many 7B-10B models while being significantly smaller.
        target_model = "microsoft/phi-3-vision-128k-instruct"
        
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
            
        completion = client.chat.completions.create(
            model=target_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }],
            max_tokens=300,
            temperature=0.1
        )
        
        return {"status": "success", "response": completion.choices[0].message.content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Internal test
    print("[*] Low-RAM Vision Initialized")
