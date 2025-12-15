import tensorflow as tf
import os
import numpy as np
from dataset_loader import DatasetLoader
from preprocess import TextPreprocessor
import json

def build_model(vocab_size, embedding_dim=16, max_length=100):
    """Builds a lightweight CNN model for text classification."""
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.Conv1D(64, 5, activation='relu'),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(24, activation='relu'),
        tf.keras.layers.Dropout(0.5), # Regularization
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model():
    # 1. Load Data
    loader = DatasetLoader()
    (X_train_raw, y_train), (X_val_raw, y_val), (X_test_raw, y_test) = loader.train_val_test_split()

    # 2. Preprocess
    preprocessor = TextPreprocessor(max_length=100)
    preprocessor.fit(X_train_raw)
    
    X_train = preprocessor.transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)
    X_test = preprocessor.transform(X_test_raw)

    # Save tokenizer for agent usage
    preprocessor.save_tokenizer('model/tokenizer.pickle')

    # 3. Build Model
    vocab_size = min(preprocessor.max_vocab_size, len(preprocessor.tokenizer.word_index) + 1)
    model = build_model(vocab_size)
    model.summary()

    # 4. Train
    checkpoint_filepath = 'model/best_model.keras' # Using .keras format
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=False,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True
    )

    history = model.fit(
        X_train, y_train,
        epochs=10,
        validation_data=(X_val, y_val),
        callbacks=[model_checkpoint_callback],
        verbose=1
    )

    # 5. Evaluate on test set
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy*100:.2f}%")

    # Save metadata
    metadata = {
        "max_length": 100,
        "vocab_size": vocab_size,
        "embedding_dim": 16,
        "model_type": "CNN"
    }
    with open('model/model_metadata.json', 'w') as f:
        json.dump(metadata, f)

if __name__ == "__main__":
    train_model()
