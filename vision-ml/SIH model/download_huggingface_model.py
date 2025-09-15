"""
Download Hugging Face Plant Disease Model for Local Use
======================================================
This script downloads the MobileNet plant disease model from Hugging Face
and saves it locally for offline use.
"""

import os
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
from huggingface_hub import snapshot_download

def download_model_locally():
    """Download the Hugging Face model and save it locally"""
    
    model_name = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    local_model_dir = "./huggingface_plant_model"
    
    print("🔄 Downloading Hugging Face Plant Disease Model...")
    print(f"📦 Model: {model_name}")
    print(f"📁 Local directory: {local_model_dir}")
    
    try:
        # Download the entire model repository
        print("\n📥 Downloading model files...")
        snapshot_download(
            repo_id=model_name,
            local_dir=local_model_dir,
            local_dir_use_symlinks=False  # Force actual file copies on Windows
        )
        
        print("✅ Model downloaded successfully!")
        print(f"📂 Model saved to: {os.path.abspath(local_model_dir)}")
        
        # Test loading the model locally
        print("\n🧪 Testing local model loading...")
        
        # Load model and processor from local directory
        model = AutoModelForImageClassification.from_pretrained(local_model_dir)
        processor = AutoImageProcessor.from_pretrained(local_model_dir)
        
        print("✅ Local model loaded successfully!")
        print(f"📊 Model has {len(model.config.id2label)} classes")
        print(f"🏷️ Sample classes: {list(model.config.id2label.values())[:5]}...")
        
        # Save model info
        info_file = os.path.join(local_model_dir, "model_info.txt")
        with open(info_file, 'w') as f:
            f.write(f"Model: {model_name}\n")
            f.write(f"Downloaded: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
            f.write(f"Classes: {len(model.config.id2label)}\n")
            f.write(f"Architecture: {model.config.model_type}\n")
            f.write("\nClass Labels:\n")
            for idx, label in model.config.id2label.items():
                f.write(f"{idx}: {label}\n")
        
        print(f"📝 Model info saved to: {info_file}")
        
        return local_model_dir
        
    except Exception as e:
        print(f"❌ Error downloading model: {str(e)}")
        return None

def get_model_size(directory):
    """Calculate the total size of downloaded model"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    
    # Convert to MB
    size_mb = total_size / (1024 * 1024)
    return size_mb

if __name__ == "__main__":
    print("🤖 Hugging Face Model Downloader")
    print("=" * 50)
    
    local_dir = download_model_locally()
    
    if local_dir and os.path.exists(local_dir):
        size_mb = get_model_size(local_dir)
        print(f"\n📊 Model Statistics:")
        print(f"   💾 Total size: {size_mb:.1f} MB")
        print(f"   📁 Files: {len([f for root, dirs, files in os.walk(local_dir) for f in files])}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Use the model offline by pointing to: {local_dir}")
        print(f"   2. Run the updated analysis script")
        print(f"   3. No internet required for future predictions!")
        
    print("\n✨ Download complete!")