import tensorflow as tf
import os

def convert_tflite():
    model_path = 'model/best_model.keras'
    tflite_path = 'model/scam_detection.tflite'
    
    print(f"Loading model from {model_path}...")
    try:
        model = tf.keras.models.load_model(model_path)
    except OSError:
        print("Model not found. Please run train.py first.")
        return

    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimization (Quantization)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Force float32 output for simplicity in this demo, or use float16
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
        
    print(f"TFLite model saved to {tflite_path}")
    print(f"Model size: {os.path.getsize(tflite_path) / 1024:.2f} KB")

if __name__ == "__main__":
    convert_tflite()
