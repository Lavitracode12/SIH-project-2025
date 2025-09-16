import os
import torch
from ultralytics import YOLO

# Store original torch.load function
original_torch_load = torch.load

# Override torch.load to disable weights_only
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = custom_load

# Load model from local file (no internet required!)
model_path = "plant_leaf_model.pt"
print(f"Loading model from: {model_path}")

# Load model
model = YOLO(model_path)

# Run on an image
image = "image copy.png"
results = model.predict(image, save=True, conf=0.25)

# Print results
for result in results:
    print(f"Detected {len(result.boxes)} objects")
    if result.boxes is not None:
        for box in result.boxes:
            print(f"Class: {int(box.cls)}, Confidence: {float(box.conf):.2f}")

print("Predictions saved to runs/detect/predict/")