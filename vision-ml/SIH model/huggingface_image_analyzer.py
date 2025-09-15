"""
🍃 Simple Plant Disease Image Analyzer
=====================================
Analyze single images for plant diseases using the local Hugging Face model.

Usage:
    python huggingface_image_analyzer.py [image_path]
    
If no image path is provided, it will use 'leaf_sample.jpg' or the test image.

Features:
- Uses locally downloaded Hugging Face MobileNet model
- Shows top 5 predictions with confidence scores
- Displays the analyzed image
- No internet connection required
- Saves results to text file

Requirements: opencv-python, transformers, torch, pillow, matplotlib
"""

import cv2
import numpy as np
import torch
from PIL import Image
import matplotlib.pyplot as plt
import sys
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

class HuggingFaceImageAnalyzer:
    def __init__(self, model_path="./huggingface_plant_model"):
        """Initialize the image analyzer with local Hugging Face model"""
        self.model_path = model_path
        self.model = None
        self.processor = None
        self.class_names = []
        self.load_model()
        
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
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            exit(1)
    
    def analyze_image(self, image_path, top_k=5):
        """Analyze a single image for plant diseases"""
        try:
            # Load and validate image
            if not os.path.exists(image_path):
                print(f"❌ Error: Image not found at {image_path}")
                return None
            
            print(f"🖼️ Analyzing image: {image_path}")
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Error: Cannot load image {image_path}")
                return None
            
            # Convert BGR to RGB for PIL
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            print(f"📏 Image size: {image.shape}")
            
            # Process with Hugging Face processor
            inputs = self.processor(images=pil_image, return_tensors="pt")
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get top K predictions
            top_probs, top_indices = torch.topk(probabilities, min(top_k, len(self.class_names)))
            
            results = []
            for i in range(top_k):
                if i < len(top_indices[0]):
                    class_name = self.class_names[top_indices[0][i].item()]
                    confidence = top_probs[0][i].item()
                    results.append({
                        'rank': i + 1,
                        'disease': class_name,
                        'confidence': confidence
                    })
            
            return {
                'image_path': image_path,
                'image_shape': image.shape,
                'predictions': results,
                'top_prediction': results[0] if results else None
            }
            
        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            return None
    
    def display_results(self, analysis_result):
        """Display analysis results"""
        if not analysis_result:
            return
        
        print(f"\n🔍 Analysis Results")
        print("=" * 50)
        
        predictions = analysis_result['predictions']
        top_pred = analysis_result['top_prediction']
        
        # Main prediction
        if top_pred:
            confidence_emoji = "🟢" if top_pred['confidence'] > 0.7 else "🟡" if top_pred['confidence'] > 0.3 else "🔴"
            print(f"\n{confidence_emoji} Top Prediction:")
            print(f"   Disease: {top_pred['disease']}")
            print(f"   Confidence: {top_pred['confidence']:.1%}")
            
            # Extract plant and disease info
            if ' with ' in top_pred['disease']:
                plant, disease = top_pred['disease'].split(' with ', 1)
                print(f"   Plant: {plant}")
                print(f"   Disease: {disease}")
            elif top_pred['disease'].endswith('y Plant') or 'Healthy' in top_pred['disease']:
                print(f"   Status: HEALTHY PLANT")
        
        # All predictions
        print(f"\n📋 Top {len(predictions)} Predictions:")
        for pred in predictions:
            print(f"   {pred['rank']}. {pred['disease']}: {pred['confidence']:.1%}")
        
        # Confidence assessment
        if top_pred:
            if top_pred['confidence'] > 0.7:
                print(f"\n✅ High confidence prediction - Likely accurate")
            elif top_pred['confidence'] > 0.3:
                print(f"\n⚠️ Moderate confidence - Consider getting expert opinion")
            else:
                print(f"\n❌ Low confidence - Results may not be reliable")
    
    def save_results(self, analysis_result, output_file="analysis_results.txt"):
        """Save analysis results to file"""
        if not analysis_result:
            return
        
        try:
            with open(output_file, 'w') as f:
                f.write("Plant Disease Analysis Results\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Image: {analysis_result['image_path']}\n")
                f.write(f"Image Size: {analysis_result['image_shape']}\n")
                f.write(f"Model: Hugging Face MobileNetV2\n\n")
                
                top_pred = analysis_result['top_prediction']
                if top_pred:
                    f.write(f"Top Prediction:\n")
                    f.write(f"  Disease: {top_pred['disease']}\n")
                    f.write(f"  Confidence: {top_pred['confidence']:.1%}\n\n")
                
                f.write(f"All Predictions:\n")
                for pred in analysis_result['predictions']:
                    f.write(f"  {pred['rank']}. {pred['disease']}: {pred['confidence']:.1%}\n")
                
                f.write(f"\nAnalysis completed using local Hugging Face model\n")
            
            print(f"💾 Results saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")
    
    def show_image(self, image_path, analysis_result):
        """Display the analyzed image with results"""
        try:
            # Load and display image
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            plt.figure(figsize=(12, 8))
            
            # Show image
            plt.subplot(1, 2, 1)
            plt.imshow(rgb_image)
            plt.title(f"Analyzed Image\n{os.path.basename(image_path)}")
            plt.axis('off')
            
            # Show results as text
            plt.subplot(1, 2, 2)
            plt.axis('off')
            
            if analysis_result and analysis_result['predictions']:
                results_text = "🍃 Disease Analysis Results\n\n"
                
                top_pred = analysis_result['top_prediction']
                if top_pred:
                    results_text += f"🎯 Top Prediction:\n"
                    results_text += f"   {top_pred['disease']}\n"
                    results_text += f"   Confidence: {top_pred['confidence']:.1%}\n\n"
                
                results_text += f"📊 All Predictions:\n"
                for pred in analysis_result['predictions'][:5]:
                    results_text += f"   {pred['rank']}. {pred['disease'][:30]}...\n      {pred['confidence']:.1%}\n"
                
                plt.text(0.1, 0.9, results_text, transform=plt.gca().transAxes, 
                        fontsize=10, verticalalignment='top', fontfamily='monospace')
            
            plt.tight_layout()
            
            # Save the visualization
            output_image = f"analysis_{os.path.splitext(os.path.basename(image_path))[0]}.png"
            plt.savefig(output_image, dpi=300, bbox_inches='tight')
            print(f"📸 Visualization saved as: {output_image}")
            
            plt.show()
            
        except Exception as e:
            print(f"❌ Error displaying image: {str(e)}")

def find_image_file():
    """Find an image file to analyze"""
    # Priority order for finding images
    candidates = [
        'leaf_sample.jpg',
        'crab-apple-fruit-tree-rust.jpg',
        'test_image.jpg',
        'sample.jpg'
    ]
    
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    
    # Look for any image files
    for file in os.listdir('.'):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            return file
    
    return None

def main():
    """Main function"""
    print("🍃 Simple Plant Disease Image Analyzer")
    print("=" * 45)
    
    # Check requirements
    try:
        import cv2
        import torch
        import matplotlib.pyplot as plt
        from transformers import AutoModelForImageClassification
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Install with: pip install opencv-python torch transformers pillow matplotlib")
        return
    
    # Get image path
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = find_image_file()
        if not image_path:
            print("❌ No image file found!")
            print("💡 Usage: python huggingface_image_analyzer.py [image_path]")
            print("💡 Or save an image as 'leaf_sample.jpg' in the current directory")
            return
    
    # Initialize analyzer
    try:
        analyzer = HuggingFaceImageAnalyzer()
        
        # Analyze image
        result = analyzer.analyze_image(image_path)
        
        if result:
            # Display results
            analyzer.display_results(result)
            
            # Save results
            analyzer.save_results(result)
            
            # Show image visualization
            analyzer.show_image(image_path, result)
        
    except KeyboardInterrupt:
        print(f"\n👋 Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()