import os
import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from PIL import Image

# Force TensorFlow to use only CPU (to avoid CUDA errors)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load the trained model without compilation issues
model = tf.keras.models.load_model("adulteration_detector_binary.h5", compile=False)

# Preprocessing function
def preprocess_image(img):
    img = img.resize((224, 224))  # Resize to match model input
    img_array = image.img_to_array(img) / 255.0  # Convert to numpy array and normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img = Image.open(img).convert("RGB")  # Open image and convert to RGB
    img_array = preprocess_image(img)  # Preprocess image

    # Make prediction
    prediction = model.predict(img_array)[0][0]  # Single value output

    # Convert prediction to label
    result = "Non compliant" if prediction > 0.5 else "Compliant"

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)