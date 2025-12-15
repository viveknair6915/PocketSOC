import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

class DatasetLoader:
    def __init__(self, dataset_path="model/dataset.csv"):
        self.dataset_path = dataset_path

    def load_dataset(self):
        """Loads dataset from CSV, handling potential errors."""
        if not os.path.exists(self.dataset_path):
            # Create dummy dataset if not exists for demonstration
            print(f"Dataset not found at {self.dataset_path}. Creating dummy dataset.")
            self._create_dummy_dataset()
        
        df = pd.read_csv(self.dataset_path)
        
        # Basic validation
        if 'text' not in df.columns or 'label' not in df.columns:
            raise ValueError("Dataset must contain 'text' and 'label' columns")
            
        return df

    def _create_dummy_dataset(self):
        """Creates a small dummy dataset for testing functionality."""
        data = {
            'text': [
                "Your account has been compromised. Click here to reset.",
                "Hey method, are we still on for lunch?",
                "URGENT: Verify your bank details immediately.",
                "See you at the meeting tomorrow.",
                "You have won a lottery! Claim now!",
                "Can you review this code?",
                "IRS alert: Tax fraud detected.",
                "Happy birthday! Have a great day.",
                "Click this link to claim your prize.",
                "Don't forget to buy milk.",
                "Security Alert: Unusual sign-in activity detected.",
                "Hi, checking in on the project status.",
                "CONGRATULATIONS! You've been selected for a cash prize.",
                "Can we reschedule our call to 3pm?",
                "Final Notice: Your package delivery failed. pay fee now.",
                "Are you coming to the party tonight?",
                "WINNER! Apple iPhone 15 Pro waiting for you.",
                "Just sent you the files via email.",
                "Your subscription is expiring. Renew immediately.",
                "Let's grab coffee later.",
                "Limited time offer! 90% off on all items.",
                "Meeting minutes attached.",
                "Suspicious Login Attempt. Secur your account.",
                "Did you see the game last night?",
                "Verify your identity to avoid account lock.",
                "Please reply with your confirmation.",
                "You have a new voicemail from unknown caller.",
                "Thanks for your help yesterday.",
                "Refund processed. Click to accept.",
                "What time is the movie?"
            ] * 4, # Multiply list to get more samples
            'label': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] * 4 # 1 = Scam, 0 = Legitimate
        }
        df = pd.DataFrame(data)
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
        df.to_csv(self.dataset_path, index=False)

    def train_val_test_split(self, test_size=0.2, val_size=0.1, random_state=42):
        """Splits data into train, validation, and test sets."""
        df = self.load_dataset()
        
        # Balance dataset if needed (simple undersampling for this demo if highly imbalanced)
        # For this demo, we assume the input is roughly balanced or we just use it as is.
        
        X = df['text'].values
        y = df['label'].values
        
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=(test_size + val_size), random_state=random_state, stratify=y
        )
        
        val_ratio = val_size / (test_size + val_size)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=(1 - val_ratio), random_state=random_state, stratify=y_temp
        )
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)

if __name__ == "__main__":
    loader = DatasetLoader()
    (Xt, yt), (Xv, yv), (Xte, yte) = loader.train_val_test_split()
    print(f"Train size: {len(Xt)}, Val size: {len(Xv)}, Test size: {len(Xte)}")
