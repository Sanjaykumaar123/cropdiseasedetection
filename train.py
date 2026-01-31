import os
import copy
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# =========================
# CONFIGURATION
# =========================
DATASET_DIR = "dataset/PlantVillage"
IMG_SIZE = (160,160)
BATCH_SIZE = 32
EPOCHS = 25

LEARNING_RATE = 1e-4
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "plant_disease_model.pth")
CLASS_PATH = os.path.join(MODEL_DIR, "class_indices.npy")

# =========================
# TRAIN FUNCTION
# =========================
def train_model():
    print(f"Using device: {DEVICE}")

    # Check dataset structure
    train_dir = os.path.join(DATASET_DIR, "train")
    val_dir = os.path.join(DATASET_DIR, "val")

    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("❌ ERROR: Dataset must contain 'train' and 'val' folders")
        return

    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # =========================
    # DATA TRANSFORMS
    # =========================
    data_transforms = {
        "train": transforms.Compose([
            transforms.Resize(IMG_SIZE),
            transforms.RandomRotation(20),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ]),
        "val": transforms.Compose([
            transforms.Resize(IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ]),
    }

    # =========================
    # DATASETS & LOADERS
    # =========================
    image_datasets = {
        "train": datasets.ImageFolder(train_dir, data_transforms["train"]),
        "val": datasets.ImageFolder(val_dir, data_transforms["val"]),
    }

    dataloaders = {
        x: DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
        for x in ["train", "val"]
    }

    dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "val"]}
    class_names = image_datasets["train"].classes

    print("Classes found:")
    print(class_names)

    # Save class indices
    np.save(CLASS_PATH, class_names)

    # =========================
    # MODEL (MobileNetV2)
    # =========================
    model = models.mobilenet_v2(
        weights=models.MobileNet_V2_Weights.IMAGENET1K_V1
    )

    # Allow all parameters to train (Finetuning)
    for param in model.parameters():
        param.requires_grad = True

    # Replace classifier
    model.classifier[1] = nn.Linear(
        model.last_channel, len(class_names)
    )

    model = model.to(DEVICE)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)

    # =========================
    # TRAINING LOOP
    # =========================
    since = time.time()
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    history = {
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": []
    }

    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        print("-" * 30)

        for phase in ["train", "val"]:
            if phase == "train":
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(DEVICE)
                labels = labels.to(DEVICE)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            history[f"{phase}_loss"].append(epoch_loss)
            history[f"{phase}_acc"].append(epoch_acc.item())

            print(f"{phase.upper()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

            if phase == "val" and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

                # save best model immediately
                torch.save(model.state_dict(), MODEL_PATH)
                print("💾 Best model saved:", MODEL_PATH)



    # =========================
    # TRAINING COMPLETE
    # =========================
    time_elapsed = time.time() - since
    print(f"\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
    print(f"Best Validation Accuracy: {best_acc:.4f}")

    model.load_state_dict(best_model_wts)

    # Save model
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

    # =========================
    # PLOT TRAINING HISTORY
    # =========================
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history["train_acc"], label="Train Acc")
    plt.plot(history["val_acc"], label="Val Acc")
    plt.title("Accuracy")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history["train_loss"], label="Train Loss")
    plt.plot(history["val_loss"], label="Val Loss")
    plt.title("Loss")
    plt.legend()

    plt.savefig(os.path.join(MODEL_DIR, "training_history.png"))
    print("📊 Training history saved")

    plt.close()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    train_model()
