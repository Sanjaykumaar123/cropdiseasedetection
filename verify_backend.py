import sys
import os

# Add backend to path so we can import ml_utils
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from ml_utils import predictor

print("Testing Backend Predictor Logic...")
print(f"Class names loaded: {len(predictor.class_names)}")
print(f"First 5 classes: {predictor.class_names[:5]}")

image_path = "test.jpg"

if not os.path.exists(image_path):
    print(f"Error: {image_path} not found")
else:
    print(f"\nPredicting on {image_path}...")
    result, status_code = predictor.predict(image_path)
    print("\nPrediction Result:")
    print(result)
