import tensorflow as tf
import numpy as np
import os
from agent_config import config

class InferenceEngine:
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.load_model()

    def load_model(self):
        if not os.path.exists(config.MODEL_PATH):
            print(f"Model not found at {config.MODEL_PATH}")
            return

        self.interpreter = tf.lite.Interpreter(model_path=config.MODEL_PATH)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, preprocessed_text):
        if not self.interpreter:
            print("Interpreter not initialized.")
            return {"label": "error", "confidence": 0.0}

        self.interpreter.set_tensor(self.input_details[0]['index'], preprocessed_text)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        # Output is sigmoid probability [0, 1]
        score = output_data[0][0]
        
        label = "scam" if score > 0.5 else "legit"
        # Confidence is probability if scam, else 1-prob
        confidence = float(score) if label == "scam" else float(1 - score)
        
        return {"label": label, "confidence": confidence, "score": float(score)}

if __name__ == "__main__":
    # Mock usage
    engine = InferenceEngine()
    dummy_input = np.zeros((1, 100), dtype=np.float32)
    print(engine.predict(dummy_input))
