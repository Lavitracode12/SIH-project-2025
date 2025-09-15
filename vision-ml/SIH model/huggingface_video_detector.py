"""
🎥 Hugging Face Plant Disease Video Detector
==========================================
Real-time plant disease detection using webcam and local Hugging Face model.

Features:
- Uses locally downloaded Hugging Face MobileNet model
- Real-time webcam video analysis
- Disease detection with confidence scores
- No internet connection required
- Press 'q' to quit, 's' to save frame, 'p' to pause

Requirements: opencv-python, transformers, torch, pillow
"""

import cv2
import numpy as np
import torch
from PIL import Image
import time
import os
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoModelForImageClassification, AutoImageProcessor
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("❌ Error: transformers not installed. Run: pip install transformers")
    exit(1)

class HuggingFaceVideoDetector:
    def __init__(self, model_path="./huggingface_plant_model"):
        """Initialize the video detector with local Hugging Face model"""
        self.model_path = model_path
        self.model = None
        self.processor = None
        self.class_names = []
        self.load_model()
        
        # Video processing settings
        self.detection_interval = 30  # Process every 30 frames for performance
        self.frame_count = 0
        self.last_prediction = None
        self.confidence_threshold = 0.3
        
    def load_model(self):
        """Load the local Hugging Face model"""
        if not os.path.exists(self.model_path):
            print(f"❌ Error: Local model not found at {self.model_path}")
            print("💡 Run download_huggingface_model.py first to download the model")
            exit(1)
            
        try:
            print(f"🤖 Loading Hugging Face model from: {self.model_path}")
            self.model = AutoModelForImageClassification.from_pretrained(self.model_path)
            self.processor = AutoImageProcessor.from_pretrained(self.model_path)
            
            # Extract class names
            self.class_names = list(self.model.config.id2label.values())
            
            print(f"✅ Model loaded successfully!")
            print(f"📊 Model has {len(self.class_names)} disease classes")
            print(f"🏷️ Sample classes: {self.class_names[:3]}...")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            exit(1)
    
    def preprocess_frame(self, frame):
        """Preprocess video frame for model prediction"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)
        
        return pil_image
    
    def predict_disease(self, frame):
        """Predict plant disease from video frame"""
        try:
            # Preprocess frame
            pil_image = self.preprocess_frame(frame)
            
            # Process with Hugging Face processor
            inputs = self.processor(images=pil_image, return_tensors="pt")
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get top prediction
            confidence, predicted_idx = torch.max(probabilities, 1)
            predicted_class = self.class_names[predicted_idx.item()]
            confidence_score = confidence.item()
            
            return {
                'disease': predicted_class,
                'confidence': confidence_score,
                'all_probabilities': probabilities[0].tolist()
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {str(e)}")
            return None
    
    def get_top_predictions(self, frame, top_k=3):
        """Get top K predictions for better analysis"""
        try:
            pil_image = self.preprocess_frame(frame)
            inputs = self.processor(images=pil_image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get top K predictions
            top_probs, top_indices = torch.topk(probabilities, top_k)
            
            results = []
            for i in range(top_k):
                class_name = self.class_names[top_indices[0][i].item()]
                confidence = top_probs[0][i].item()
                results.append({
                    'disease': class_name,
                    'confidence': confidence
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Top predictions error: {str(e)}")
            return []
    
    def draw_predictions(self, frame, predictions):
        """Draw prediction results on video frame"""
        if not predictions:
            return frame
        
        # Create overlay
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Background for text
        cv2.rectangle(overlay, (10, 10), (width-10, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Title
        cv2.putText(frame, "🍃 Plant Disease Detection", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Main prediction
        main_pred = predictions[0]
        color = (0, 255, 0) if main_pred['confidence'] > self.confidence_threshold else (0, 165, 255)
        
        cv2.putText(frame, f"Disease: {main_pred['disease']}", 
                   (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"Confidence: {main_pred['confidence']:.1%}", 
                   (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Status indicator
        status = "HIGH CONFIDENCE" if main_pred['confidence'] > self.confidence_threshold else "LOW CONFIDENCE"
        cv2.putText(frame, status, (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Controls
        cv2.putText(frame, "Controls: 'q'=quit, 's'=save, 'p'=pause", 
                   (20, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def save_frame(self, frame, predictions):
        """Save current frame with predictions"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"plant_detection_{timestamp}.jpg"
        
        # Add prediction text to saved image
        if predictions:
            pred_text = f"Disease: {predictions[0]['disease']} ({predictions[0]['confidence']:.1%})"
            cv2.putText(frame, pred_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imwrite(filename, frame)
        print(f"📸 Frame saved as: {filename}")
    
    def run_detection(self):
        """Main video detection loop"""
        print(f"\n🎥 Starting webcam detection...")
        print(f"📋 Controls:")
        print(f"   'q' - Quit")
        print(f"   's' - Save current frame")
        print(f"   'p' - Pause/Resume")
        print(f"   ESC - Quit")
        
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Cannot open webcam")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        paused = False
        print(f"✅ Webcam started! Press 'q' to quit...")
        
        try:
            while True:
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        print("❌ Error: Cannot read from webcam")
                        break
                    
                    # Process frame for prediction (every N frames for performance)
                    if self.frame_count % self.detection_interval == 0:
                        predictions = self.get_top_predictions(frame, top_k=3)
                        if predictions:
                            self.last_prediction = predictions
                    
                    # Draw predictions on frame
                    if self.last_prediction:
                        frame = self.draw_predictions(frame, self.last_prediction)
                    
                    self.frame_count += 1
                
                # Display frame
                cv2.imshow('Plant Disease Detection - Hugging Face Model', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    break
                elif key == ord('s'):  # Save frame
                    self.save_frame(frame, self.last_prediction)
                elif key == ord('p'):  # Pause/Resume
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMED"
                    print(f"🎬 Video {status}")
        
        except KeyboardInterrupt:
            print(f"\n⚠️ Detection interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            print(f"🎬 Video detection stopped")

def main():
    """Main function to run the video detector"""
    print("🍃 Hugging Face Plant Disease Video Detector")
    print("=" * 50)
    
    # Check requirements
    try:
        import cv2
        import torch
        from transformers import AutoModelForImageClassification
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Install with: pip install opencv-python torch transformers pillow")
        return
    
    # Initialize and run detector
    try:
        detector = HuggingFaceVideoDetector()
        detector.run_detection()
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()