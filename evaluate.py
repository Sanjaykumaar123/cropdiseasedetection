import torch
import numpy as np
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score

DATASET_DIR = "dataset/PlantVillage/val"
MODEL_PATH = "model/plant_disease_model.pth"
CLASS_PATH = "model/class_indices.npy"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load classes
class_names = np.load(CLASS_PATH, allow_pickle=True)

# Model
model = models.mobilenet_v2(weights=None)
model.classifier[1] = torch.nn.Linear(model.last_channel, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(DATASET_DIR, transform=transform)
loader = DataLoader(dataset, batch_size=32, shuffle=False)

y_true, y_pred = [], []

with torch.no_grad():
    for inputs, labels in loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)

        y_true.extend(labels.cpu().numpy())
        y_pred.extend(preds.cpu().numpy())

acc = accuracy_score(y_true, y_pred)
print(f"✅ Validation Accuracy: {acc * 100:.2f}%")
