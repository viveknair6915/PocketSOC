import tensorflow as tf
from dataset_loader import DatasetLoader
from preprocess import TextPreprocessor
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import numpy as np

def evaluate_model():
    # Load model
    model_path = 'model/best_model.keras'
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Load data
    loader = DatasetLoader()
    _, _, (X_test_raw, y_test) = loader.train_val_test_split()
    
    # Preprocess
    preprocessor = TextPreprocessor()
    preprocessor.load_tokenizer('model/tokenizer.pickle')
    X_test = preprocessor.transform(X_test_raw)
    
    # Predict
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    # metrics
    print("\n--- Evaluation Results ---")
    print(classification_report(y_test, y_pred, target_names=['Legit', 'Scam']))
    
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print(f"Confusion Matrix:\nTN: {tn} | FP: {fp}\nFN: {fn} | TP: {tp}")

if __name__ == "__main__":
    evaluate_model()
