import torch
import numpy as np
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F

MODEL_PATH = "model/plant_disease_model.pth"
CLASS_PATH = "model/class_indices.npy"
IMAGE_PATH = "test.jpg"   # add any leaf image

# Load class names
class_names = np.load(CLASS_PATH, allow_pickle=True)

# Load model
model = models.mobilenet_v2(weights=None)
model.classifier[1] = torch.nn.Linear(model.last_channel, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

# Image transform
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Load image
image = Image.open(IMAGE_PATH).convert("RGB")
image = transform(image).unsqueeze(0)




with torch.no_grad():
    outputs = model(image)
    probs = F.softmax(outputs, dim=1)
    
    # Get top 5 predictions
    top_probs, top_preds = torch.topk(probs, 5)

# Convert to lists
top_probs = top_probs.squeeze().tolist()
top_preds = top_preds.squeeze().tolist()

print("\n🔍 Model Diagnosis:")
print("-" * 30)
print(f"Top Prediction: {class_names[top_preds[0]]}")
print(f"Confidence: {top_probs[0] * 100:.2f}%")
print("-" * 30)

print("📊 Top 5 Predictions:")
for i in range(len(top_probs)):
    print(f"{i+1}. {class_names[top_preds[i]]}: {top_probs[i] * 100:.2f}%")

THRESHOLD = 0.5  # Lowered threshold to see if it helps, original was 0.75

print("-" * 30)
if top_probs[0] < THRESHOLD:
    print("❌ Result: Not Leaf (Low Confidence)")
    print(f"⚠️  Confidence {top_probs[0] * 100:.2f}% is below threshold {THRESHOLD * 100}%")
else:
    print(f"✅ Result: {class_names[top_preds[0]]}")
    print(f"Confidence: {top_probs[0] * 100:.2f}%")

