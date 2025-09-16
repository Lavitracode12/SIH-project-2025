# 🚀 SIH Project 2025 - Installation Guide

## 📋 System Requirements

### **Operating System**
- **Linux**: Ubuntu 20.04+ (recommended)
- **Windows**: Windows 10/11 (64-bit)
- **macOS**: macOS 10.15+ (Intel/Apple Silicon)

### **Software Prerequisites**
- **Python**: 3.8 or higher
- **Node.js**: 18.0 or higher (for dashboard)
- **Webots**: R2025a (for simulation)
- **Git**: Latest version

### **Hardware Requirements**
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space
- **GPU**: NVIDIA GPU with CUDA 11.8+ (optional, for acceleration)

---

## 🔧 Installation Steps

### **1. Clone the Repository**
```bash
git clone https://github.com/Lavitracode12/SIH-project-2025.git
cd SIH-project-2025
```

### **2. Set Up Python Environment**

#### **Option A: Using venv (Recommended)**
```bash
# Create virtual environment
python -m venv sih_env

# Activate environment
# Linux/macOS:
source sih_env/bin/activate
# Windows:
sih_env\Scripts\activate
```

#### **Option B: Using conda**
```bash
# Create conda environment
conda create -n sih_env python=3.9
conda activate sih_env
```

### **3. Install Python Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import torch, cv2, numpy, transformers, ultralytics; print('All packages installed successfully!')"
```

### **4. Install Webots Simulation Environment**

#### **Linux (Ubuntu/Debian)**
```bash
# Download and install Webots R2025a
wget https://github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb
sudo dpkg -i webots_2025a_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed
```

#### **Windows**
1. Download [Webots R2025a for Windows](https://github.com/cyberbotics/webots/releases/download/R2025a/webots-R2025a_setup.exe)
2. Run the installer as Administrator
3. Follow installation wizard

#### **macOS**
```bash
# Using Homebrew
brew install --cask webots

# Or download from:
# https://github.com/cyberbotics/webots/releases/download/R2025a/webots-R2025a.dmg
```

### **5. Set Up Dashboard Frontend**
```bash
# Navigate to dashboard
cd dashboard/client

# Install Node.js dependencies
npm install

# Verify installation
npm run dev
```

---

## 🎯 Quick Start Guide

### **1. Test Vision-ML System**
```bash
# Activate Python environment
source sih_env/bin/activate  # Linux/macOS
# or: sih_env\Scripts\activate  # Windows

# Test plant disease detection
cd vision-ml/real_vision/Hybrid\ system/leaf\ detection/
python hybrid_plant_analyzer.py

# Test video detection
cd ../video_detection/
python realtime_hybrid_analyzer.py
```

### **2. Run Simulation**
```bash
# Start Webots
webots

# Open world file
# File → Open World → simulations/Hybrid_simulation/World/worlds/field.wbt

# Run controllers from Webots interface:
# - keyboard: Manual control
# - wall_follower: Autonomous navigation
# - my_controller: Basic wall following
```

### **3. Launch Dashboard**
```bash
# Start development server
cd dashboard/client
npm run dev

# Access dashboard at: http://localhost:5173
```

---

## 🔍 Verification & Testing

### **Python Environment Test**
```bash
python -c "
import torch
import cv2
import numpy as np
from transformers import AutoModel
from ultralytics import YOLO
import matplotlib.pyplot as plt
print('✅ All core dependencies working!')
print(f'PyTorch version: {torch.__version__}')
print(f'OpenCV version: {cv2.__version__}')
print(f'NumPy version: {np.__version__}')
"
```

### **GPU Acceleration Test (Optional)**
```bash
python -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU device: {torch.cuda.get_device_name(0)}')
    print(f'CUDA version: {torch.version.cuda}')
"
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **1. OpenCV Installation Issues**
```bash
# If opencv-python fails to install
pip uninstall opencv-python
pip install opencv-python-headless

# For full OpenCV with GUI support
pip install opencv-contrib-python
```

#### **2. PyTorch CUDA Issues**
```bash
# Install CPU-only version if GPU not available
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### **3. Transformers Model Download Issues**
```bash
# Set cache directory
export HF_HOME=/path/to/cache
export TRANSFORMERS_CACHE=/path/to/cache

# Or download models manually
python vision-ml/SIH\ model/download_huggingface_model.py
```

#### **4. Webots Controller Issues**
- Ensure Webots is properly installed
- Add Webots to system PATH
- Check controller file permissions

#### **5. Frontend Build Issues**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📁 Project Structure Overview

```
SIH-project-2025/
├── 🤖 vision-ml/          # AI/ML components
├── 🎮 simulations/        # Webots simulation
├── 🌐 dashboard/          # React frontend
├── 📄 docs/              # Documentation
├── ⚙️  firmware/          # Hardware control
├── 🔧 hardware/          # Hardware designs
├── 📋 requirements.txt    # Python dependencies
└── 📖 INSTALLATION.md     # This file
```

---

## 🆘 Getting Help

### **Documentation**
- **Project Wiki**: [GitHub Wiki](https://github.com/Lavitracode12/SIH-project-2025/wiki)
- **API Documentation**: Available after running dashboard
- **Webots Documentation**: [Official Webots Docs](https://cyberbotics.com/doc/)

### **Support Channels**
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Email Support**: [Contact Team](mailto:team@sih-project.com)

### **Quick Links**
- 🔗 [Webots Installation Guide](https://cyberbotics.com/doc/guide/installation-procedure)
- 🔗 [PyTorch Installation](https://pytorch.org/get-started/locally/)
- 🔗 [Node.js Download](https://nodejs.org/en/download/)
- 🔗 [Transformers Documentation](https://huggingface.co/docs/transformers/)

---

## 🎉 Success!

If you've completed all steps successfully, you should now have:
- ✅ Complete Python environment with all ML libraries
- ✅ Webots simulation ready to run
- ✅ React dashboard running on localhost
- ✅ All AI models loaded and functional

**Next Steps:**
1. Explore the simulation controllers
2. Test plant disease detection
3. Run the complete agricultural rover simulation
4. Customize for your specific use case

Happy coding! 🚀🌱