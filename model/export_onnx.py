import tensorflow as tf
import tf2onnx
import onnx
import os

def export_onnx():
    model_path = 'model/best_model.keras'
    onnx_path = 'model/scam_detection.onnx'
    
    print(f"Loading model from {model_path}...")
    try:
        model = tf.keras.models.load_model(model_path)
    except OSError:
        print("Model not found. Please run train.py first.")
        return

    print("Converting to ONNX...")
    input_signature = [tf.TensorSpec([None, 100], tf.float32, name='embedding_input')]
    
    # Convert
    onnx_model, _ = tf2onnx.convert.from_keras(
        model, 
        input_signature=input_signature, 
        opset=13
    )
    
    onnx.save(onnx_model, onnx_path)
    print(f"Model saved to {onnx_path}")

if __name__ == "__main__":
    export_onnx()
