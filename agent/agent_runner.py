import time
import sys
from agent_config import config
from preprocess import AgentPreprocessor
from inference import InferenceEngine
from event_sender import EventSender

class AgentRunner:
    def __init__(self):
        print("Initializing PocketSOC Mobile Agent...")
        self.preprocessor = AgentPreprocessor()
        self.engine = InferenceEngine()
        self.sender = EventSender()
        print("Agent Initialized.")

    def process_message(self, text):
        print(f"\nProcessing Message: '{text}'")
        
        # 1. Preprocess
        processed = self.preprocessor.preprocess(text)
        
        # 2. Inference
        result = self.engine.predict(processed)
        confidence = result['confidence']
        label = result['label']
        score = result['score']
        
        print(f"Result: {label.upper()} (Confidence: {confidence:.4f}, Score: {score:.4f})")
        
        # 3. Check Threshold & Act
        if label == "scam" and confidence >= config.CONFIDENCE_THRESHOLD:
            print(">>> THREAT DETECTED! Sending report to backend...")
            
            incident_data = {
                "original_text": text,
                "detected_label": label,
                "confidence": confidence,
                "raw_score": score,
                "action_taken": "blocked"
            }
            
            self.sender.send_event(incident_data)
        else:
            print("Message appears safe or below threshold.")

    def run_loop(self):
        print("Agent is running. Describe simulated SMS messages below. Type 'exit' to quit.")
        while True:
            try:
                text = input(">> Enter SMS content: ").strip()
                if text.lower() == 'exit':
                    break
                if not text:
                    continue
                
                self.process_message(text)
            except KeyboardInterrupt:
                break
        print("Agent stopped.")

if __name__ == "__main__":
    runner = AgentRunner()
    if len(sys.argv) > 1:
        # One-shot mode
        runner.process_message(sys.argv[1])
    else:
        # Interactive mode
        runner.run_loop()
