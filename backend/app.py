import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import uuid

from config import Config
from models import db, User, Prediction
from ml_utils import predictor

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
CORS(app) # Allow all for development
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Create DB Tables on startup
with app.app_context():
    db.create_all()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================
# AUTH ROUTES
# ==============================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password_hash=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User newly registered success"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        # Create JWT
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

# ==============================
# PREDICTION ROUTES
# ==============================

@app.route('/api/predict', methods=['POST'])
@jwt_required()
def predict():
    if 'image' not in request.files:
        return jsonify({"message": "No image part"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        # Save file with unique name
        user_id = get_jwt_identity()
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Run Inference
        result = predictor.predict(filepath)
        
        # Determine strict status
        if isinstance(result, tuple): # Error case
            return jsonify(result[0]), result[1]

        # Save to DB
        new_prediction = Prediction(
            user_id=int(user_id),
            image_path=unique_filename,
            prediction=result['prediction'],
            confidence=result['confidence']
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify(result), 200

    return jsonify({"message": "Invalid file type"}), 400

@app.route('/api/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=int(user_id))\
        .order_by(Prediction.created_at.desc())\
        .all()
    
    return jsonify([p.to_dict() for p in predictions]), 200

# ==============================
# UTILITY ROUTES
# ==============================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/history/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_history_item(id):
    user_id = get_jwt_identity()
    prediction = Prediction.query.filter_by(id=id, user_id=int(user_id)).first()
    
    if not prediction:
        return jsonify({"message": "Prediction not found"}), 404
        
    db.session.delete(prediction)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

@app.route('/')
def home():
    return jsonify({"message": "Plant Disease API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
