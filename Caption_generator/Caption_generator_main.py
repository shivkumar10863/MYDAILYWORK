from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from PIL import Image
import torch

# Smaller model for testing
model_name = "Qwen/Qwen2.5-VL-3B-Instruct"

# Load model
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

processor = AutoProcessor.from_pretrained(model_name)

# Open image
image = Image.open("Caption_generator\test.jpg").convert("RGB")

# Prepare input
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": "Describe this image in one sentence."}
        ]
    }
]

# Convert to model format
text = processor.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = processor(
    text=[text],
    images=[image],
    return_tensors="pt"
)

inputs = inputs.to(model.device)

# Generate caption
output = model.generate(
    **inputs,
    max_new_tokens=50
)

result = processor.batch_decode(
    output,
    skip_special_tokens=True
)

print("\nCaption:")
print(result[0])