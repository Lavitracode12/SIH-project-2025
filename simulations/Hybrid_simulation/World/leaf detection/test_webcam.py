import cv2

def test_webcam():
    """Test if webcam is working"""
    print("Testing webcam access...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return False
    
    ret, frame = cap.read()
    if ret:
        print("✅ Webcam is working!")
        print(f"Frame size: {frame.shape}")
        cap.release()
        return True
    else:
        print("❌ Cannot read from webcam")
        cap.release()
        return False

if __name__ == "__main__":
    test_webcam()