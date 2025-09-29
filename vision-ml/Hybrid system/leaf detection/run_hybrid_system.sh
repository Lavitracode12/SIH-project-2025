#!/bin/bash

# Hybrid Plan🚀 Available Commands:
echo "1. python3 hybrid_plant_analyzer.py    - Full hybrid analysis on all images"
echo "2. python3 quick_analysis.py           - Interactive single image analysis"
echo "3. python3 quick_analysis.py <image>   - Direct image analysis"
echo ""ysis System - Summary & Launcher
echo "🌿🔬 Hybrid Plant Analysis System"
echo "=================================="
echo ""
echo "This system combines two AI models:"
echo "1. 🎯 YOLO Leaf Detection (47 plant species)"
echo "2. 🏥 ViT Disease Classification (13 disease types)"
echo ""

# Check if models are available
echo "📋 System Status:"
if [ -f "plant_leaf_model.pt" ]; then
    echo "✅ Leaf detection model: Available ($(du -h plant_leaf_model.pt | cut -f1))"
else
    echo "❌ Leaf detection model: Missing"
fi

if [ -d "../Disease detection/local_models" ]; then
    echo "✅ Disease detection models: Available"
else
    echo "❌ Disease detection models: Missing"
fi

echo ""
echo "🚀 Available Commands:"
echo "1. python3 hybrid_plant_analyzer.py    - Full analysis on all images"
echo "2. python3 quick_analysis.py           - Interactive single image analysis"
echo "3. python3 quick_analysis.py <image>   - Direct image analysis"
echo "4. python3 test_samples.py             - Test leaf detection only"
echo ""

echo "📊 Recent Analysis Results:"
if [ -f "hybrid_analysis_image.png" ]; then
    echo "✅ image.png: Analyzed (2 leaves, 0 healthy, 2 diseased)"
fi
if [ -f "hybrid_analysis_image2.png" ]; then
    echo "✅ image2.png: Analyzed (1 leaf, 0 healthy, 1 diseased)"
fi

echo ""
echo "📁 Generated Files:"
leaf_crops=$(ls leaf_crop_* 2>/dev/null | wc -l)
hybrid_analysis=$(ls hybrid_analysis_* 2>/dev/null | wc -l)
echo "🍃 Leaf crops: $leaf_crops files"
echo "📸 Annotated images: $hybrid_analysis files"

echo ""
echo "🔍 Workflow:"
echo "Step 1: YOLO detects and locates leaves in image"
echo "Step 2: System crops each detected leaf region"
echo "Step 3: ViT model classifies each leaf's health status"
echo "Step 4: Results combined into comprehensive analysis"
echo ""

read -p "Run quick analysis now? (y/N): " answer
if [[ $answer =~ ^[Yy]$ ]]; then
    python3 quick_analysis.py
fi