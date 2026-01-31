import os
import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np

# Configuration
DATASET_DIR = 'dataset/PlantVillage'
IMG_SIZE = (224, 224)

def check_data():
    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory '{DATASET_DIR}' not found.")
        return

    # Adjusted for train/val split structure
    train_dir = os.path.join(DATASET_DIR, 'train')
    if not os.path.exists(train_dir):
        print(f"Error: Training directory '{train_dir}' not found. Ensure 'dataset/PlantVillage/train' exists.")
        return

    # Count classes and images
    classes = os.listdir(train_dir)
    print(f"Found {len(classes)} classes in train set: {classes}")

    total_images = 0
    for cls in classes:
        cls_path = os.path.join(train_dir, cls)
        if os.path.isdir(cls_path):
            count = len(os.listdir(cls_path))
            print(f"  {cls}: {count} images")
            total_images += count
    
    print(f"Total images found: {total_images}")

    # Visualize augmentation using PyTorch transforms
    print("Visualizing data augmentation...")
    
    # Define transforms similar to Keras logic
    data_transforms = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.RandomRotation(20),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])

    # Find a sample image
    sample_img_path = None
    for root, dirs, files in os.walk(train_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                sample_img_path = os.path.join(root, file)
                break
        if sample_img_path:
            break
            
    if sample_img_path:
        from PIL import Image
        img = Image.open(sample_img_path)
        
        plt.figure(figsize=(10,10))
        for i in range(9):
            augmented_img = data_transforms(img)
            # Convert back to PIL for display (permute tensor: C,H,W -> H,W,C)
            display_img = augmented_img.permute(1, 2, 0).numpy()
            
            plt.subplot(3, 3, i+1)
            plt.imshow(display_img)
            plt.axis('off')
            
        plt.show()
        print("Augmentation visualization shown.")
    else:
        print("No images found to visualize.")

if __name__ == "__main__":
    check_data()
