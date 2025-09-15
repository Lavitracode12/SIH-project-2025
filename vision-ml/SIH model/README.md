# 🍃 Hugging Face Plant Disease Detection Kit# Plant Disease Detection on Video



A streamlined plant disease detection system using locally stored Hugging Face models. No internet connection required after initial setup!This project applies a trained ResNet-9 model to detect plant diseases in video streams or files.



## 📁 What's Included## Features



```- **Real-time Detection**: Process webcam feed or video files

📦 SIH model/- **38 Disease Classes**: Detects diseases across multiple plant types including:

├── 🤖 huggingface_plant_model/          # Local AI model (9.1 MB)  - Tomato (Late blight, Early blight, Bacterial spot, etc.)

├── 🍎 crab-apple-fruit-tree-rust.jpg    # Test image  - Apple (Apple scab, Black rot, Cedar apple rust)

├── 📥 download_huggingface_model.py     # Model downloader (already run)  - Corn (Northern Leaf Blight, Common rust, etc.)

├── 📸 huggingface_image_analyzer.py     # Single image analysis  - Grape (Black rot, Leaf blight, Esca)

├── 🎥 huggingface_video_detector.py     # Webcam video analysis  - Potato (Late blight, Early blight)

└── 📋 requirements.txt                  # Dependencies  - And many more...

```

- **Visual Feedback**: Overlays predictions with confidence scores

## 🚀 Quick Start- **Multiple Input Sources**: Supports video files, webcam, or image sequences

- **Output Options**: Save processed video or view live

### 1. Install Dependencies

```bash## Setup

pip install -r requirements.txt

```1. **Install Dependencies**:

   ```bash

### 2. Analyze Images   pip install -r requirements.txt

```bash   ```

# Analyze the test image

python huggingface_image_analyzer.py2. **Ensure Model Files**:

   - Make sure you have either `plant-disease-model.pth` or `plant-disease-model-complete.pth`

# Analyze your own image   - These should be in the same directory as the script

python huggingface_image_analyzer.py path/to/your/image.jpg

## Usage

# Or save your image as 'leaf_sample.jpg' and run:

python huggingface_image_analyzer.py### Basic Usage

```

1. **Process a video file**:

### 3. Real-time Webcam Detection   ```bash

```bash   python plant_disease_video_detector.py --input your_video.mp4 --model plant-disease-model-complete.pth

python huggingface_video_detector.py   ```

```

2. **Use webcam**:

## 🎮 Controls   ```bash

   python plant_disease_video_detector.py --input webcam --model plant-disease-model-complete.pth

### Video Detector Controls:   ```

- **'q'** or **ESC** - Quit

- **'s'** - Save current frame with prediction3. **Save output video**:

- **'p'** - Pause/Resume video   ```bash

   python plant_disease_video_detector.py --input your_video.mp4 --model plant-disease-model-complete.pth --output processed_video.mp4

### Image Analyzer Features:   ```

- Shows top 5 predictions with confidence scores

- Saves results to `analysis_results.txt`4. **Process without display** (useful for batch processing):

- Creates visualization image   ```bash

- Displays analyzed image with results   python plant_disease_video_detector.py --input your_video.mp4 --model plant-disease-model-complete.pth --output processed_video.mp4 --no-display

   ```

## 🤖 Model Information

### Command Line Arguments

- **Architecture**: MobileNetV2

- **Classes**: 38 plant diseases- `--input` or `-i`: Input source (video file path or "webcam")

- **Input Size**: 224x224 pixels- `--model` or `-m`: Path to the trained model file (.pth)

- **Model Size**: 9.1 MB- `--output` or `-o`: Output video path (optional)

- **Offline**: ✅ No internet required- `--no-display`: Disable live video display



### Supported Disease Classes:### Examples

- Apple Scab, Black Rot, Cedar Apple Rust

- Bell Pepper Bacterial Spot```bash

- Grape Esca (Black Measles)# Process a plant video from file

- Tomato diseases (Early/Late Blight, Leaf Mold, etc.)python plant_disease_video_detector.py -i garden_video.mp4 -m plant-disease-model-complete.pth

- Healthy plants detection

- And 30+ more diseases...# Live webcam detection

python plant_disease_video_detector.py -i webcam -m plant-disease-model-complete.pth

## 📊 Understanding Results

# Process and save output

### Confidence Levels:python plant_disease_video_detector.py -i plant_footage.avi -m plant-disease-model-complete.pth -o results.mp4

- 🟢 **>70%**: High confidence - Likely accurate```

- 🟡 **30-70%**: Moderate confidence - Consider expert opinion

- 🔴 **<30%**: Low confidence - Results may not be reliable## How It Works



### Output Files:1. **Frame Extraction**: Extracts frames from video source

- `analysis_results.txt` - Detailed text results2. **Preprocessing**: Resizes frames to 256x256 pixels and normalizes

- `analysis_[image_name].png` - Visual analysis3. **Model Inference**: Applies ResNet-9 model to classify plant health

- `plant_detection_[timestamp].jpg` - Saved video frames4. **Visualization**: Overlays results on original frames

5. **Output**: Displays live or saves processed video

## 🔧 System Requirements

## Model Information

### Hardware:

- Webcam (for video detection)- **Architecture**: ResNet-9 (9-layer Residual Network)

- CPU: Any modern processor- **Input Size**: 256x256 RGB images

- RAM: 2GB+ available- **Classes**: 38 plant disease categories

- Storage: 50MB+ free space- **Training**: Trained on PlantVillage dataset with augmentation



### Software:## Output Information

- Python 3.8+

- OpenCV (camera access)The script displays:

- PyTorch (AI processing)- **Plant Type**: Detected plant species

- Transformers (model loading)- **Health Status**: HEALTHY or DISEASED

- Matplotlib (visualization)- **Disease Name**: Specific disease if detected

- **Confidence Score**: Model's confidence in prediction

## 💡 Tips for Best Results- **Processing FPS**: Real-time processing speed



### Image Quality:## Performance Notes

- Use well-lit images

- Focus on leaf surfaces- **GPU Acceleration**: Automatically uses CUDA if available

- Avoid blurry or dark images- **Processing Speed**: Varies based on hardware (typically 5-30 FPS)

- Include diseased areas clearly- **Memory Usage**: Approximately 1-2GB RAM with GPU



### Camera Setup:## Troubleshooting

- Good lighting conditions

- Stable camera position1. **Import Errors**: Ensure all requirements are installed

- Hold plants steady2. **Model Loading**: Check model file path and compatibility

- Focus on individual leaves3. **Video Issues**: Verify video format and codec support

4. **Performance**: Use GPU for faster processing

## 🔬 Technical Details

## Supported Plant Types

### Model Performance:

- **Training Data**: PlantVillage datasetThe model can detect diseases in:

- **Accuracy**: ~88% on test data- Apple, Blueberry, Cherry, Corn (Maize), Grape

- **Processing Speed**: ~30 FPS on modern CPU- Orange, Peach, Pepper (Bell), Potato, Raspberry

- **Memory Usage**: <1GB RAM- Soybean, Squash, Strawberry, Tomato



### Processing Pipeline:## Disease Categories

1. Image preprocessing (resize, normalize)

2. Feature extraction (MobileNetV2)Includes both healthy and diseased categories for comprehensive plant health assessment.

3. Classification (38-class softmax)

4. Post-processing (confidence ranking)Press 'q' during live processing to quit the application.

## 🛠️ Troubleshooting

### Common Issues:

**"Model not found"**
```bash
# Re-download the model
python download_huggingface_model.py
```

**"Cannot open webcam"**
- Check camera permissions
- Close other camera applications
- Try different camera index (0, 1, 2...)

**"Missing packages"**
```bash
pip install opencv-python torch transformers pillow matplotlib
```

**Low accuracy on real images**
- The model was trained on specific datasets
- Real-world conditions may differ
- Use as a preliminary screening tool

## 📈 Model Comparison

| Feature | Hugging Face Model | Your Original ResNet-9 |
|---------|-------------------|------------------------|
| Accuracy | Higher (~88%) | Variable |
| Internet | Not required | Not required |
| Size | 9.1 MB | Larger |
| Speed | Fast | Fast |
| Reliability | High | Architecture issues |

## 🎯 Use Cases

### Agriculture:
- Field disease screening
- Crop health monitoring
- Early disease detection
- Farmer education tool

### Research:
- Plant pathology studies
- Disease pattern analysis
- Educational demonstrations
- Data collection

### Personal:
- Garden plant health
- Houseplant care
- Learning plant diseases
- Photo analysis

## 🔄 Updates and Maintenance

The model is static and doesn't require updates. However, you can:
- Re-download newer model versions
- Add new test images
- Modify confidence thresholds
- Customize output formats

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Verify all dependencies are installed
3. Test with the provided sample image
4. Check camera permissions for video mode

---

## ⚡ Quick Commands Summary

```bash
# Single image analysis
python huggingface_image_analyzer.py

# Video detection
python huggingface_video_detector.py

# Re-download model if needed
python download_huggingface_model.py
```

**Ready to detect plant diseases! 🍃🔬**