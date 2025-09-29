import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time

# Store original torch.load function
original_torch_load = torch.load

# Override torch.load to disable weights_only
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = custom_load

# Plant leaf class names (you can customize these based on the model's classes)
class_names = {
    0: 'alstonia_scholaris', 1: 'arjun', 2: 'bael', 3: 'basil', 4: 'chinar', 
    5: 'guava', 6: 'jamun', 7: 'jatropha', 8: 'lemon', 9: 'mango', 
    10: 'moringa', 11: 'neem', 12: 'oleander', 13: 'parijat', 14: 'peepal', 
    15: 'plumeria', 16: 'pomegranate', 17: 'ashoka', 18: 'jackfruit', 19: 'coconut',
    20: 'betel', 21: 'drumstick', 22: 'lemon_grass', 23: 'senna', 24: 'rose_apple',
    25: 'curry', 26: 'cherry', 27: 'amla', 28: 'banana', 29: 'tea',
    30: 'mint', 31: 'ficus', 32: 'camphor', 33: 'bamboo', 34: 'rubber',
    35: 'eucalyptus', 36: 'papaya', 37: 'hibiscus', 38: 'cotton', 39: 'pomelo',
    40: 'indian_mustard', 41: 'tulsi', 42: 'tamarind', 43: 'castor', 44: 'insulin',
    45: 'cardamom', 46: 'unknown'
}

def load_model():
    """Load the plant leaf detection model"""
    model_path = "plant_leaf_model.pt"
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    print("Model loaded successfully!")
    return model

def draw_predictions(frame, results, confidence_threshold=0.25):
    """Draw bounding boxes and labels on the frame"""
    if results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        
        for box, conf, cls in zip(boxes, confidences, classes):
            if conf >= confidence_threshold:
                x1, y1, x2, y2 = map(int, box)
                class_id = int(cls)
                class_name = class_names.get(class_id, f"Class {class_id}")
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label background
                label = f"{class_name}: {conf:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                            (x1 + label_size[0], y1), (0, 255, 0), -1)
                
                # Draw label text
                cv2.putText(frame, label, (x1, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return frame

def main():
    """Main function to run webcam leaf detection"""
    # Load the model
    model = load_model()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set webcam resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Webcam initialized. Press 'q' to quit, 's' to save current frame")
    
    frame_count = 0
    fps_start_time = time.time()
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Run inference every few frames to improve performance
        if frame_count % 3 == 0:  # Process every 3rd frame
            # Run YOLO prediction
            results = model.predict(frame, conf=0.25, verbose=False)
            
            # Draw predictions on frame
            frame = draw_predictions(frame, results)
        
        # Calculate and display FPS
        frame_count += 1
        if frame_count % 30 == 0:
            fps_end_time = time.time()
            fps = 30 / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            print(f"FPS: {fps:.1f}")
        
        # Add instructions to frame
        cv2.putText(frame, "Press 'q' to quit, 's' to save", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display the frame
        cv2.imshow('Plant Leaf Detection - Webcam', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save current frame
            timestamp = int(time.time())
            filename = f"leaf_detection_capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Frame saved as {filename}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam stopped. Goodbye!")

if __name__ == "__main__":
    main()