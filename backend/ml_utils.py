import torch
import numpy as np
from torchvision import models, transforms
from PIL import Image, ImageOps
import torch.nn.functional as F
import os

# Paths relative to backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "plant_disease_model.pth")
CLASS_PATH = os.path.join(PROJECT_ROOT, "model", "class_indices.npy")

class PlantDiseasePredictor:
    def __init__(self):
        self.device = torch.device("cpu") # Use CPU for inference to be safe/simple
        self.class_names = None
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
        self.load_artifacts()

    def load_artifacts(self):
        try:
            # Load Class Names
            if os.path.exists(CLASS_PATH):
                self.class_names = np.load(CLASS_PATH, allow_pickle=True)
                print(f"✅ Loaded {len(self.class_names)} classes.")
                if len(self.class_names) > 0:
                    print(f"   Sample classes: {self.class_names[:3]}")
            else:
                print(f"❌ Error: Class file not found at {CLASS_PATH}")
                return

            # Load Model
            if os.path.exists(MODEL_PATH):
                self.model = models.mobilenet_v2(weights=None)
                # Adjust classifier to match training
                self.model.classifier[1] = torch.nn.Linear(self.model.last_channel, len(self.class_names))
                
                # Load state dict
                self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                self.model.to(self.device)
                self.model.eval()
                print("✅ Model loaded successfully.")
            else:
                print(f"❌ Error: Model file not found at {MODEL_PATH}")

        except Exception as e:
            print(f"❌ Exception loading artifacts: {e}")

    def predict(self, image_path):
        if self.model is None or self.class_names is None:
            return {"error": "Model not loaded"}, 500

        try:
            image = Image.open(image_path).convert("RGB")
            
            # Handle EXIF Orientation
            try:
                image = ImageOps.exif_transpose(image)
            except Exception:
                pass # safely ignore if no exif
                
            print(f"📸 Processed Image: {image.size} mode={image.mode} path={os.path.basename(image_path)}")

            image_tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensor)
                probs = F.softmax(outputs, dim=1)
                
                # Get top 5 predictions for debugging
                top5_prob, top5_idx = torch.topk(probs, 5)
                print(f"🔍 Top 5 Predictions for {os.path.basename(image_path)}:")
                for i in range(5):
                    class_name = self.class_names[top5_idx[0][i].item()]
                    prob_score = top5_prob[0][i].item()
                    print(f"   {i+1}. {class_name}: {prob_score*100:.2f}%")

                confidence, pred = torch.max(probs, 1)

            confidence_val = confidence.item()
            pred_idx = pred.item()
            
            THRESHOLD = 0.50

            if confidence_val < THRESHOLD:
                print(f"⚠️ Rejected: Confidence {confidence_val:.2f} < {THRESHOLD}")
                return {
                    "status": "rejected",
                    "prediction": "Unknown / Low Confidence",
                    "confidence": round(confidence_val * 100, 2),
                    "details": "Confidence too low to confirm diagnosis."
                }
            else:
                predicted_class = self.class_names[pred_idx]
                print(f"✅ Accepted: {predicted_class} ({confidence_val:.2f})")
                return {
                    "status": "success",
                    "prediction": predicted_class,
                    "confidence": round(confidence_val * 100, 2)
                }

        except Exception as e:
            return {"error": str(e)}, 500

# Global instance
predictor = PlantDiseasePredictor()
