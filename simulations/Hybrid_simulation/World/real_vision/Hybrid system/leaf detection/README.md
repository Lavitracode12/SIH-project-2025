# Hybrid Plant Analysis System

## 🌿🔬 Overview
This system combines YOLO leaf detection with ViT disease classification for comprehensive plant health analysis.

## 📁 Essential Files

### Core System
- **`hybrid_plant_analyzer.py`** - Main hybrid analysis system
- **`plant_leaf_model.pt`** - YOLO model for leaf detection (22.5MB)
- **`quick_analysis.py`** - User-friendly interface for single image analysis
- **`run_hybrid_system.sh`** - System launcher and status checker

### Required Dependencies
- **`../Disease detection/local_models/`** - ViT disease detection models (ONLY)
  - `feature_extractor/` - Image preprocessing model
  - `classification_model/` - Disease classification model

## 🚀 Usage

### Quick Start
```bash
# Interactive mode
python3 quick_analysis.py

# Direct image analysis
python3 quick_analysis.py <image_path>

# Batch analysis of all images
python3 hybrid_plant_analyzer.py
```

### System Launcher
```bash
bash run_hybrid_system.sh
```

## ⚙️ Configuration

### Confidence Thresholds
- **Leaf Detection**: 0.10 (10% confidence)
- **Disease Classification**: 0.30 (30% confidence)

### Supported Features
- **47 plant species** detection
- **12 disease types** classification  
- **Automatic leaf cropping**
- **Health status assessment**
- **Visual annotations**

## 📊 Output Files
- **`leaf_crop_*.png`** - Individual cropped leaf regions
- **`hybrid_analysis_*.png`** - Annotated images with results

## 🔧 System Requirements
- Python 3.x
- OpenCV, PIL, transformers, ultralytics
- CUDA (optional, for GPU acceleration)

---
*Clean hybrid detection system - unnecessary files removed*