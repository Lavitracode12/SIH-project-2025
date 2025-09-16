#!/usr/bin/env python3
"""
Hybrid Plant Analysis System
1. Uses YOLO model to detect and locate leaves in images
2. Crops detected leaf regions
3. Applies ViT disease detection model to classify leaf health
4. Combines results for comprehensive plant analysis
"""

import os
import torch
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from transformers import ViTImageProcessor, ViTForImageClassification
import time

# Store original torch.load function
original_torch_load = torch.load

# Override torch.load to disable weights_only
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = custom_load

# Plant leaf class names for YOLO detection
leaf_class_names = {
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

class HybridPlantAnalyzer:
    """Hybrid system combining leaf detection and disease classification"""
    
    def __init__(self, leaf_model_path="plant_leaf_model.pt", disease_models_dir="../Disease detection/local_models"):
        self.leaf_model_path = leaf_model_path
        self.disease_models_dir = disease_models_dir
        self.leaf_detector = None
        self.disease_processor = None
        self.disease_model = None
        
        # Load models
        self.load_models()
    
    def load_models(self):
        """Load both leaf detection and disease classification models"""
        print("🔄 Loading Hybrid Plant Analysis Models...")
        
        # Load leaf detection model
        if os.path.exists(self.leaf_model_path):
            try:
                self.leaf_detector = YOLO(self.leaf_model_path)
                print("✅ Leaf detection model loaded successfully!")
            except Exception as e:
                print(f"❌ Error loading leaf detection model: {e}")
                return False
        else:
            print(f"❌ Leaf detection model not found: {self.leaf_model_path}")
            return False
        
        # Load disease detection models
        feature_extractor_path = os.path.join(self.disease_models_dir, "feature_extractor")
        disease_model_path = os.path.join(self.disease_models_dir, "classification_model")
        
        if os.path.exists(feature_extractor_path) and os.path.exists(disease_model_path):
            try:
                self.disease_processor = ViTImageProcessor.from_pretrained(feature_extractor_path, local_files_only=True)
                self.disease_model = ViTForImageClassification.from_pretrained(disease_model_path, local_files_only=True)
                print("✅ Disease detection models loaded successfully!")
                
                # Show disease classes (excluding 'Invalid')
                disease_classes = [label for label in self.disease_model.config.id2label.values() if label != "Invalid"]
                print(f"🏷️  Disease classes: {len(disease_classes)} types")
                
            except Exception as e:
                print(f"❌ Error loading disease detection models: {e}")
                return False
        else:
            print(f"❌ Disease detection models not found in: {self.disease_models_dir}")
            return False
        
        print("🎉 All models loaded successfully!")
        return True
    
    def is_ready(self):
        """Check if all models are loaded and ready"""
        return (self.leaf_detector is not None and 
                self.disease_processor is not None and 
                self.disease_model is not None)
    
    def detect_leaves(self, image, confidence=0.10):
        """Detect leaves in image using YOLO model"""
        if not self.leaf_detector:
            return []
        
        try:
            results = self.leaf_detector.predict(image, conf=confidence, verbose=False)
            detections = []
            
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    class_id = int(box.cls.item())
                    confidence_score = float(box.conf.item())
                    coords = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    
                    species = leaf_class_names.get(class_id, f"Unknown ({class_id})")
                    
                    detections.append({
                        'species': species,
                        'confidence': confidence_score,
                        'bbox': coords,
                        'class_id': class_id
                    })
            
            return detections
            
        except Exception as e:
            print(f"❌ Error in leaf detection: {e}")
            return []
    
    def crop_leaf_region(self, image, bbox, padding=10):
        """Crop leaf region from image with optional padding"""
        try:
            if isinstance(image, str):
                # If image is a path, load it
                image = cv2.imread(image)
            
            h, w = image.shape[:2]
            x1, y1, x2, y2 = bbox
            
            # Add padding and ensure coordinates are within image bounds
            x1 = max(0, int(x1 - padding))
            y1 = max(0, int(y1 - padding))
            x2 = min(w, int(x2 + padding))
            y2 = min(h, int(y2 + padding))
            
            # Crop the region
            cropped = image[y1:y2, x1:x2]
            
            # Convert BGR to RGB for PIL
            cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            return Image.fromarray(cropped_rgb)
            
        except Exception as e:
            print(f"❌ Error cropping leaf region: {e}")
            return None
    
    def classify_leaf_health(self, leaf_image, min_confidence=0.30):
        """Classify leaf health using disease detection model"""
        if not self.disease_processor or not self.disease_model:
            return None
        
        try:
            # Process image
            inputs = self.disease_processor(images=leaf_image, return_tensors="pt")
            
            # Make prediction
            outputs = self.disease_model(**inputs)
            logits = outputs.logits
            predicted_idx = logits.argmax(-1).item()
            
            # Calculate confidence
            probabilities = logits.softmax(-1)
            confidence = probabilities[0][predicted_idx].item()
            
            # Get class label
            predicted_class = self.disease_model.config.id2label[predicted_idx]
            
            # Skip 'Invalid' classifications
            if predicted_class == "Invalid":
                return None
            
            # Filter by minimum confidence threshold
            if confidence < min_confidence:
                print(f"   ⚠️  Low confidence ({confidence:.3f}) - below threshold ({min_confidence})")
                return None
            
            # Determine health status
            is_healthy = "Healthy" in predicted_class
            
            return {
                'disease': predicted_class,
                'confidence': confidence,
                'is_healthy': is_healthy,
                'health_status': 'Healthy' if is_healthy else 'Diseased'
            }
            
        except Exception as e:
            print(f"❌ Error in disease classification: {e}")
            return None
    
    def analyze_image(self, image_path, leaf_confidence=0.10, save_crops=True):
        """Complete hybrid analysis of an image"""
        if not self.is_ready():
            print("❌ Models not ready for analysis")
            return None
        
        print(f"\n🔍 Analyzing: {os.path.basename(image_path)}")
        print("=" * 60)
        
        # Load image
        if isinstance(image_path, str):
            if not os.path.exists(image_path):
                print(f"❌ Image not found: {image_path}")
                return None
            image = cv2.imread(image_path)
        else:
            image = image_path
        
        if image is None:
            print("❌ Failed to load image")
            return None
        
        # Step 1: Detect leaves
        print("📍 Step 1: Detecting leaves...")
        leaf_detections = self.detect_leaves(image, confidence=leaf_confidence)
        
        if not leaf_detections:
            print("❌ No leaves detected in image")
            return None
        
        print(f"✅ Found {len(leaf_detections)} leaf/leaves")
        
        # Step 2: Analyze each detected leaf
        analysis_results = []
        
        for i, detection in enumerate(leaf_detections, 1):
            print(f"\n🌱 Analyzing Leaf {i}/{len(leaf_detections)}:")
            print(f"   Species: {detection['species']}")
            print(f"   Detection confidence: {detection['confidence']:.3f}")
            
            # Crop leaf region
            leaf_image = self.crop_leaf_region(image, detection['bbox'])
            
            if leaf_image is None:
                print("   ❌ Failed to crop leaf region")
                continue
            
            # Save cropped leaf if requested
            if save_crops:
                crop_filename = f"leaf_crop_{i}_{os.path.basename(image_path)}"
                leaf_image.save(crop_filename)
                print(f"   💾 Saved crop: {crop_filename}")
            
            # Classify leaf health
            health_result = self.classify_leaf_health(leaf_image, min_confidence=0.30)
            
            if health_result:
                print(f"   🏥 Health Status: {health_result['health_status']}")
                print(f"   🎯 Disease: {health_result['disease']}")
                print(f"   📊 Health confidence: {health_result['confidence']:.3f}")
                
                # Health status emoji
                if health_result['is_healthy']:
                    print("   ✅ HEALTHY LEAF")
                else:
                    print("   ⚠️  DISEASED LEAF")
                
                # Combine results
                combined_result = {
                    'leaf_id': i,
                    'species': detection['species'],
                    'species_confidence': detection['confidence'],
                    'bbox': detection['bbox'],
                    'health_status': health_result['health_status'],
                    'disease': health_result['disease'],
                    'health_confidence': health_result['confidence'],
                    'is_healthy': health_result['is_healthy']
                }
                
                analysis_results.append(combined_result)
            else:
                print("   ❌ Failed to classify leaf health")
        
        # Generate summary
        if analysis_results:
            healthy_count = sum(1 for r in analysis_results if r['is_healthy'])
            diseased_count = len(analysis_results) - healthy_count
            
            print(f"\n📊 ANALYSIS SUMMARY:")
            print(f"   🌿 Total leaves analyzed: {len(analysis_results)}")
            print(f"   ✅ Healthy leaves: {healthy_count}")
            print(f"   ⚠️  Diseased leaves: {diseased_count}")
            print(f"   📈 Health ratio: {healthy_count/len(analysis_results)*100:.1f}%")
        
        return {
            'image_path': image_path,
            'total_leaves': len(analysis_results),
            'healthy_count': healthy_count,
            'diseased_count': diseased_count,
            'results': analysis_results
        }
    
    def create_annotated_image(self, image_path, analysis_result, output_path=None):
        """Create annotated image showing both detection and health status"""
        if not analysis_result:
            return None
        
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        for result in analysis_result['results']:
            bbox = result['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            
            # Choose color based on health status
            if result['is_healthy']:
                color = (0, 255, 0)  # Green for healthy
                status_text = "HEALTHY"
            else:
                color = (0, 0, 255)  # Red for diseased
                status_text = "DISEASED"
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Prepare text
            species_text = f"{result['species']}"
            disease_text = f"{result['disease']}"
            conf_text = f"{result['health_confidence']:.2f}"
            
            # Draw text background
            text_y = y1 - 10
            cv2.rectangle(image, (x1, text_y - 60), (x1 + 250, text_y), color, -1)
            
            # Draw text
            cv2.putText(image, species_text, (x1 + 5, text_y - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, f"{status_text}: {disease_text}", (x1 + 5, text_y - 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(image, f"Conf: {conf_text}", (x1 + 5, text_y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Save annotated image
        if output_path is None:
            output_path = f"hybrid_analysis_{os.path.basename(image_path)}"
        
        cv2.imwrite(output_path, image)
        print(f"💾 Saved annotated image: {output_path}")
        return output_path

def main():
    """Main function to run hybrid plant analysis"""
    print("🌿🔬 Hybrid Plant Analysis System")
    print("=" * 50)
    print("Combining leaf detection + disease classification")
    
    # Initialize analyzer
    analyzer = HybridPlantAnalyzer()
    
    if not analyzer.is_ready():
        print("❌ Failed to initialize analyzer")
        return
    
    # Find test images
    test_images = []
    
    # Check samples directory
    samples_dir = "../samples"
    if os.path.exists(samples_dir):
        for file in os.listdir(samples_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
                test_images.append(os.path.join(samples_dir, file))
    
    # Check current directory for original images (not detected_*)
    for file in os.listdir('.'):
        if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')) and 
            not file.startswith('detected_') and 
            not file.startswith('leaf_crop_') and
            not file.startswith('hybrid_analysis_')):
            test_images.append(file)
    
    if not test_images:
        print("❌ No test images found!")
        return
    
    print(f"🔍 Found {len(test_images)} test images")
    
    # Analyze each image
    for image_path in test_images:
        result = analyzer.analyze_image(image_path, leaf_confidence=0.10, save_crops=True)
        
        if result:
            # Create annotated image
            analyzer.create_annotated_image(image_path, result)
    
    print("\n🎉 Hybrid analysis completed!")
    print("📁 Check the directory for:")
    print("   - leaf_crop_*.* (individual leaf crops)")
    print("   - hybrid_analysis_*.* (annotated results)")

if __name__ == "__main__":
    main()