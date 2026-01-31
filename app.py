import os
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Configuration
MODEL_PATH = 'model/plant_disease_model.pth'
IMG_SIZE = (224, 224)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Class Names
def get_class_names():
    if os.path.exists('model/class_indices.npy'):
        return np.load('model/class_indices.npy', allow_pickle=True)
    return []

# Load Model
@st.cache_resource
def load_trained_model(num_classes):
    if not os.path.exists(MODEL_PATH):
        return None
    
    # Recreate the model architecture
    model = models.mobilenet_v2(weights=None) # Weights not needed for inference, we load state_dict
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
        model = model.to(DEVICE)
        model.eval()
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

# Preprocessing
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0).to(DEVICE)

st.set_page_config(page_title="Plant Disease Prediction", page_icon="🌿")

st.title("🌿 Plant Disease Prediction System")
st.markdown("""
Upload a plant leaf image to detect diseases.
Supported crops: Potato, Tomato, Pepper, etc.
""")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if st.button('Predict'):
        class_indices = get_class_names()
        if len(class_indices) == 0:
            st.error("Class indices not found! Please run train.py first.")
        else:
            model = load_trained_model(len(class_indices))
            
            if model is None:
                st.error("Model not found! Please run train.py first to generate the model.")
            else:
                with st.spinner('Analyzing...'):
                    input_tensor = preprocess_image(image)
                    
                    with torch.no_grad():
                        outputs = model(input_tensor)
                        probabilities = torch.nn.functional.softmax(outputs, dim=1)
                        
                    confidence, predicted_idx = torch.max(probabilities, 1)
                    confidence = confidence.item() * 100
                    predicted_label = class_indices[predicted_idx.item()]

                    st.success(f"**Prediction:** {predicted_label}")
                    st.info(f"**Confidence:** {confidence:.2f}%")
                    
                    # Determine status
                    if "healthy" in predicted_label.lower():
                        st.balloons()
                        st.write("✅ **Status:** Healthy Plant")
                    else:
                        st.warning("⚠️ **Status:** Diseased Plant")
                        st.markdown("### Recommendation")
                        st.write("Consult an agricultural expert for appropriate treatment.")

st.markdown("---")
st.markdown("Developed for Plant Disease Detection Project")
