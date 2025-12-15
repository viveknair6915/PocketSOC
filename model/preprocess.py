import tensorflow as tf
import numpy as np
import json
import pickle
import os
import re

class TextPreprocessor:
    def __init__(self, max_vocab_size=10000, max_length=100, trunc_type='post', padding_type='post', oov_tok="<OOV>"):
        self.max_vocab_size = max_vocab_size
        self.max_length = max_length
        self.trunc_type = trunc_type
        self.padding_type = padding_type
        self.oov_tok = oov_tok
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(
            num_words=max_vocab_size, oov_token=oov_tok
        )

    def clean_text(self, text):
        """Basic text cleaning."""
        text = str(text).lower()
        text = re.sub(r'<.*?>', '', text) # Remove HTML tags
        text = re.sub(r'[^a-zA-Z\s]', '', text) # Keep only letters and spaces
        text = re.sub(r'\s+', ' ', text).strip() # Remove extra spaces
        return text

    def fit(self, texts):
        """Fit tokenizer on texts."""
        cleaned_texts = [self.clean_text(t) for t in texts]
        self.tokenizer.fit_on_texts(cleaned_texts)

    def transform(self, texts):
        """Convert texts to padded sequences."""
        cleaned_texts = [self.clean_text(t) for t in texts]
        sequences = self.tokenizer.texts_to_sequences(cleaned_texts)
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            sequences, maxlen=self.max_length, padding=self.padding_type, truncating=self.trunc_type
        )
        return padded

    def save_tokenizer(self, path='model/tokenizer.pickle'):
        """Save tokenizer to file."""
        with open(path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_tokenizer(self, path='model/tokenizer.pickle'):
        """Load tokenizer from file."""
        with open(path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

if __name__ == "__main__":
    # Test
    preprocessor = TextPreprocessor()
    sample_texts = ["Hello world", "This is a scam message"]
    preprocessor.fit(sample_texts)
    padded = preprocessor.transform(sample_texts)
    print("Padded shape:", padded.shape)
