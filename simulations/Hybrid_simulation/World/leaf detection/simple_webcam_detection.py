import cv2
import torch
from ultralytics import YOLO
import time

# Store original torch.load function
original_torch_load = torch.load

# Override torch.load to disable weights_only
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = custom_load

def main():
    """Simple webcam leaf detection"""
    # Load the model
    print("Loading plant leaf detection model...")
    model = YOLO("plant_leaf_model.pt")
    print("Model loaded successfully!")
    
    # Initialize webcam
    print("Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam. Please check if camera is connected.")
        return
    
    print("Webcam ready! Hold a leaf in front of the camera.")
    print("Controls:")
    print("- Press 'q' to quit")
    print("- Press 's' to save current frame")
    print("- Press SPACE to take a detection screenshot")
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Run leaf detection
        results = model.predict(frame, conf=0.25, verbose=False)
        
        # Draw results on frame
        annotated_frame = results[0].plot()
        
        # Add instructions
        cv2.putText(annotated_frame, "Plant Leaf Detection - Press 'q' to quit", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show detection count
        if results[0].boxes is not None:
            num_detections = len(results[0].boxes)
            cv2.putText(annotated_frame, f"Leaves detected: {num_detections}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Plant Leaf Detection', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') or key == ord(' '):
            # Save current frame with detections
            timestamp = int(time.time())
            filename = f"leaf_detection_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"Screenshot saved as {filename}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped!")

if __name__ == "__main__":
    main()