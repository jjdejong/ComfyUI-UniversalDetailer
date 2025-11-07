# YOLOv Models Setup Guide

This guide explains how to get the required YOLOv detection models installed and operational for ComfyUI Universal Detailer.

## Quick Start

### Method 1: Automatic Setup Script (Recommended)

Run the included setup script to download all models automatically:

```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer
python setup_models.py
```

This will download all required models to the `models/` directory.

### Method 2: Automatic Download on First Use

The Universal Detailer node will automatically attempt to download models when you first use them in ComfyUI. Simply:

1. Add the Universal Detailer node to your workflow
2. Select a detection model from the dropdown
3. Run the workflow - the model will download automatically if not present

**Note**: If automatic download fails (e.g., due to event loop conflicts), use Method 1 or Method 3.

### Method 3: Manual Download

If automatic methods fail, manually download and place the models:

1. **Create the models directory**:
   ```bash
   mkdir -p ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models
   ```

2. **Download models** from the URLs below

3. **Place files** in the `models/` directory with exact filenames

## Available Models

### Face Detection Models

All face models are from the [Bingsu/adetailer](https://huggingface.co/Bingsu/adetailer) Hugging Face repository.

#### YOLOv8n-face (Recommended for most users)
- **Filename**: `yolov8n-face.pt`
- **Size**: ~6.2 MB
- **Speed**: Fast
- **Accuracy**: Good
- **Download URL**: https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt
- **Use case**: General face detection, fast processing

**Manual download**:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models
curl -L -o yolov8n-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt"
```

Or using wget:
```bash
wget -O yolov8n-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt"
```

#### YOLOv8s-face (High accuracy)
- **Filename**: `yolov8s-face.pt`
- **Size**: ~22.5 MB
- **Speed**: Medium
- **Accuracy**: High
- **Download URL**: https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8s.pt
- **Use case**: High-quality face detection, when accuracy is priority

**Manual download**:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models
curl -L -o yolov8s-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8s.pt"
```

Or using wget:
```bash
wget -O yolov8s-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8s.pt"
```

#### YOLOv8m-face (Maximum accuracy)
- **Filename**: `yolov8m-face.pt`
- **Size**: ~52 MB
- **Speed**: Slower
- **Accuracy**: Highest
- **Download URL**: https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt
- **Use case**: Maximum quality face detection

**Manual download**:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models
curl -L -o yolov8m-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt"
```

Or using wget:
```bash
wget -O yolov8m-face.pt "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt"
```

### General Object Detection

#### YOLOv8n
- **Filename**: `yolov8n.pt`
- **Size**: ~6.2 MB
- **Download URL**: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
- **Use case**: General object detection (80 COCO classes including person)

**Manual download**:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models
curl -L -o yolov8n.pt "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
```

### Hand Detection Models

#### hand_yolov8n (Manual installation required)
- **Filename**: `hand_yolov8n.pt`
- **Size**: ~6.2 MB
- **Note**: This model requires manual sourcing as there's no public download URL
- **Use case**: Hand and finger detection

**To obtain this model**:
1. Train your own YOLOv8 model on hand detection dataset, OR
2. Find a pre-trained model from the community
3. Place it in the `models/` directory with the exact filename `hand_yolov8n.pt`

## Verification

### Check Installed Models

List the models in your models directory:

```bash
ls -lh ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models/
```

You should see files like:
```
yolov8n-face.pt    (~6 MB)
yolov8s-face.pt    (~22 MB)
yolov8n.pt         (~6 MB)
```

### Test Model Loading

Run the basic test script:

```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer
python basic_test.py
```

This will verify that models can be loaded correctly.

### Test in ComfyUI

1. Restart ComfyUI (if running)
2. Add "Universal Detailer" node to your workflow
3. Select a detection model from the dropdown
4. Connect required inputs (image, model, VAE, conditioning)
5. Run the workflow

## Troubleshooting

### Problem: Automatic download fails with "Cannot run the event loop"

**Cause**: Asyncio event loop conflict in ComfyUI environment

**Solution**: Use the setup script instead:
```bash
python setup_models.py
```

### Problem: "Model file not found" error

**Cause**: Model not downloaded or in wrong location

**Solution**:
1. Check that `models/` directory exists in the plugin directory
2. Verify model files are present with correct filenames
3. Run `python setup_models.py` to download missing models

### Problem: "Failed to load YOLO model: 'model-name' does not exist"

**Cause**: Model file doesn't exist or has wrong filename

**Solution**:
1. Ensure exact filename matches (e.g., `yolov8n-face.pt` not `yolov8n_face.pt`)
2. Re-download the model using setup script
3. Check file permissions (should be readable)

### Problem: Download times out or fails

**Cause**: Network issues or firewall blocking downloads

**Solution**:
1. Check internet connectivity
2. Try manual download with `curl` or `wget`
3. Download on another machine and transfer files
4. Check if corporate firewall is blocking GitHub releases

### Problem: Model loads but detection doesn't work

**Cause**: Wrong model for the target type

**Solution**:
- Use `yolov8n-face` or `yolov8s-face` for face detection
- Use `hand_yolov8n` for hand detection (if available)
- Check confidence threshold isn't too high (try 0.3-0.5)

## Advanced Setup

### Custom Models Directory

To use a different models directory:

```bash
python setup_models.py --models-dir /path/to/custom/models
```

Then update the node configuration to point to this directory.

### Download Specific Model Only

```bash
python setup_models.py --model yolov8n-face
```

### Force Re-download

To re-download models (e.g., if corrupted):

```bash
python setup_models.py --force
```

### Using Proxy

If behind a proxy, set environment variables before running:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
python setup_models.py
```

## Model Storage Locations

Default model locations for different installations:

**Standard ComfyUI installation**:
```
ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models/
```

**Portable ComfyUI**:
```
ComfyUI_windows_portable/ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models/
```

**Docker installation**:
```
/app/ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/models/
```

## Model File Requirements

For models to work correctly:

1. ✅ Exact filename match (case-sensitive)
2. ✅ Valid PyTorch model file (.pt format)
3. ✅ File size > 0 bytes (complete download)
4. ✅ Read permissions for ComfyUI user
5. ✅ Located in correct `models/` directory

## Performance Recommendations

### For Fast Processing
- Use `yolov8n-face` (smallest, fastest)
- Lower confidence threshold increases speed
- Process smaller images when possible

### For High Accuracy
- Use `yolov8s-face` (larger, more accurate)
- Higher confidence threshold (0.6-0.7)
- Ensure good input image quality

### For Memory-Constrained Systems
- Use nano models (`yolov8n-face`)
- Limit cache size in model manager
- Process images sequentially not in batch

## Support

If you continue to have issues:

1. Check the logs in ComfyUI console for detailed error messages
2. Verify all dependencies are installed (`pip install -r requirements.txt`)
3. Try downloading models manually and placing them in the correct directory
4. Report issues on GitHub with:
   - Error messages from console
   - Output of `ls -lh models/`
   - ComfyUI version
   - Operating system

## Quick Reference

| Model Name | Filename | Size | Purpose | Speed | Accuracy |
|------------|----------|------|---------|-------|----------|
| yolov8n-face | yolov8n-face.pt | 6.2MB | Face detection | Fast | Good |
| yolov8s-face | yolov8s-face.pt | 22.5MB | Face detection | Medium | High |
| yolov8n | yolov8n.pt | 6.2MB | Object detection | Fast | Good |
| hand_yolov8n | hand_yolov8n.pt | 6.2MB | Hand detection | Fast | Good |

---

**Last Updated**: 2025-11-07
**Plugin Version**: 2.0.0
