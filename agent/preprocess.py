import pickle
import re
import numpy as np
import tensorflow as tf
from agent_config import config

class AgentPreprocessor:
    def __init__(self):
        self.tokenizer = None
        self.max_length = 100
        self.load_tokenizer()

    def load_tokenizer(self):
        try:
            with open(config.TOKENIZER_PATH, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
        except Exception as e:
            print(f"Error loading tokenizer from {config.TOKENIZER_PATH}: {e}")
            # Fallback or error handling

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def preprocess(self, text):
        if not self.tokenizer:
            raise RuntimeError("Tokenizer not loaded")
        
        cleaned = self.clean_text(text)
        seq = self.tokenizer.texts_to_sequences([cleaned])
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            seq, maxlen=self.max_length, padding='post', truncating='post'
        )
        # TFLite expects float32 usually
        return padded.astype(np.float32)

if __name__ == "__main__":
    ap = AgentPreprocessor()
    print(ap.preprocess("Test message"))
