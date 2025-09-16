#!/usr/bin/env python3
"""
Quick Hybrid Analysis Script
Simple interface for running hybrid plant analysis
"""

import sys
import os
from hybrid_plant_analyzer import HybridPlantAnalyzer

def quick_analysis(image_path, confidence=0.10):
    """Quick analysis of a single image"""
    print(f"🔬 Quick Hybrid Analysis: {os.path.basename(image_path)}")
    print("-" * 50)
    
    # Initialize analyzer
    analyzer = HybridPlantAnalyzer()
    
    if not analyzer.is_ready():
        print("❌ Failed to load models")
        return
    
    # Analyze image
    result = analyzer.analyze_image(image_path, leaf_confidence=confidence, save_crops=True)
    
    if result:
        # Create annotated image
        analyzer.create_annotated_image(image_path, result)
        
        # Print summary
        print(f"\n🎯 FINAL SUMMARY:")
        print(f"📸 Image: {os.path.basename(image_path)}")
        print(f"🌿 Total leaves: {result['total_leaves']}")
        print(f"✅ Healthy: {result['healthy_count']}")
        print(f"⚠️  Diseased: {result['diseased_count']}")
        
        if result['total_leaves'] > 0:
            health_percentage = (result['healthy_count'] / result['total_leaves']) * 100
            print(f"📊 Plant health: {health_percentage:.1f}%")
            
            if health_percentage >= 80:
                print("🌟 EXCELLENT plant health!")
            elif health_percentage >= 60:
                print("👍 GOOD plant health")
            elif health_percentage >= 40:
                print("⚠️  MODERATE plant health - monitor closely")
            else:
                print("🚨 POOR plant health - needs attention!")
        
        return result
    else:
        print("❌ Analysis failed")
        return None

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Analyze specific image
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            quick_analysis(image_path)
        else:
            print(f"❌ Image not found: {image_path}")
    else:
        # Interactive mode
        print("🌿🔬 Quick Hybrid Plant Analysis")
        print("=" * 40)
        
        # Find available images
        sample_images = []
        
        # Check samples directory
        samples_dir = "../samples"
        if os.path.exists(samples_dir):
            for file in os.listdir(samples_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    sample_images.append(os.path.join(samples_dir, file))
        
        # Check current directory
        for file in os.listdir('.'):
            if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and 
                not file.startswith('detected_') and 
                not file.startswith('leaf_crop_') and
                not file.startswith('hybrid_analysis_')):
                sample_images.append(file)
        
        if not sample_images:
            print("❌ No images found!")
            print("Usage: python3 quick_analysis.py <image_path>")
            return
        
        print("Available images:")
        for i, img in enumerate(sample_images, 1):
            print(f"  {i}. {os.path.basename(img)}")
        
        try:
            choice = input(f"\nSelect image (1-{len(sample_images)}) or 'all': ")
            
            if choice.lower() == 'all':
                # Analyze all images
                for img in sample_images:
                    print(f"\n{'='*60}")
                    quick_analysis(img)
            else:
                # Analyze selected image
                idx = int(choice) - 1
                if 0 <= idx < len(sample_images):
                    quick_analysis(sample_images[idx])
                else:
                    print("❌ Invalid choice")
        
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()