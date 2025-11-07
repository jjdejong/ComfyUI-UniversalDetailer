# Troubleshooting Universal Detailer

## Node Runs Too Fast / No Processing

If the Universal Detailer node runs very quickly (< 1 second) and doesn't seem to process your images, check the following:

### 1. Check ComfyUI Console for Warnings

Look for these messages in your ComfyUI console:

**If you see**: `"ComfyUI sampling modules not available, using fallback"`
- **Problem**: The inpainting is being skipped because ComfyUI's sampling functions aren't accessible
- **Solution**: This is usually fine in a proper ComfyUI installation. If you see this, please report it as a bug.

**If you see**: `"Using fallback passthrough mode - inpainting may not work properly"`
- **Problem**: Inpainting is completely disabled, images are just passed through
- **Solution**: Reinstall ComfyUI or check that your installation isn't corrupted

**If you see**: `"Found 0 detections"`
- **Problem**: No faces/hands detected in your image
- **Solutions**:
  - Lower the confidence threshold (try 0.3-0.4)
  - Make sure your image actually contains faces/hands
  - Try a different detection model (yolov8s-face for better accuracy)
  - Ensure the image is clear and faces are visible

### 2. Verify Models are Loaded

Check the console for:
```
Successfully loaded detection model: yolov8n-face
```

If you see errors like:
```
Failed to load detection model: yolov8n-face
Model file not found: models/yolov8n-face.pt
```

**Solution**: Run the model setup script:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer
python setup_models.py
```

### 3. Test Detection Settings

Try these settings for better detection:

**For faces**:
```
detection_model: yolov8n-face or yolov8s-face
target_parts: face
confidence_threshold: 0.3-0.5 (lower = more sensitive)
```

**For hands**:
```
detection_model: hand_yolov8n (if available)
target_parts: hand
confidence_threshold: 0.3-0.4
```

### 4. Check Image Requirements

**Minimum requirements**:
- Image resolution: At least 512x512 pixels
- Face size: Faces should be at least 64x64 pixels in the image
- Clarity: Image should not be too blurry or dark
- Format: Standard RGB images (not grayscale)

### 5. Enable Detailed Logging

To see what's happening, check the ComfyUI console output. You should see:

```
Loading model yolov8n-face from models/yolov8n-face.pt
Successfully loaded and cached model: yolov8n-face
Running detection with confidence threshold: 0.5
Found X detections
Starting ComfyUI inpainting process
Step 1: Encoding image to latent space
...
Running 20 sampling steps with euler, cfg=7.0
```

If the steps messages appear, inpainting is working. If they don't, there's an issue with the ComfyUI integration.

### 6. Common Issues

#### Issue: "Steps setting doesn't seem to work"
**Symptoms**: Node completes in < 1 second regardless of steps value

**Causes**:
1. No detections found (check console for "Found 0 detections")
2. Inpainting is being skipped due to errors (check for ImportError or fallback messages)
3. ComfyUI modules not loading properly

**Solutions**:
1. Test with a clear image containing obvious faces
2. Lower confidence threshold to 0.3
3. Check ComfyUI console for error messages
4. Restart ComfyUI after installing the node

#### Issue: "Image looks unchanged"
**Symptoms**: Node completes but output looks identical to input

**Possible causes**:
1. No detections made (confidence too high)
2. Inpaint strength too low (try 0.75-0.85)
3. Mask padding too small (try 32-48)
4. Detection working but inpainting falling back to original

**Solutions**:
```python
confidence_threshold: 0.3-0.4  # Lower for more detections
inpaint_strength: 0.75-0.85    # Higher for more visible changes
mask_padding: 32-48            # Larger area to inpaint
steps: 20-30                   # More steps for better quality
```

#### Issue: "Model not found errors"
**Error**: `Model file not found: models/yolov8n-face.pt`

**Solution**:
```bash
cd ComfyUI/custom_nodes/ComfyUI-UniversalDetailer
python setup_models.py
```

Then restart ComfyUI.

### 7. Diagnostic Checklist

Run through this checklist:

- [ ] Models downloaded (`ls models/` should show `.pt` files)
- [ ] ComfyUI restarted after installation
- [ ] Test image contains clear faces/hands
- [ ] Confidence threshold is reasonable (0.3-0.5)
- [ ] Check console for "Found X detections" where X > 0
- [ ] No error messages in console
- [ ] Steps > 0 (recommended: 20)
- [ ] Model, VAE, and conditioning properly connected in workflow

### 8. Test Workflow

Here's a minimal test workflow:

1. Load Image node → Load a portrait photo with a clear face
2. Load Checkpoint node → Load your SD model
3. CLIP Text Encode (positive) → "high quality, detailed face"
4. CLIP Text Encode (negative) → "blurry, deformed"
5. Universal Detailer:
   - Image: from Load Image
   - Model: from checkpoint
   - VAE: from checkpoint
   - Positive: from CLIP positive
   - Negative: from CLIP negative
   - detection_model: yolov8n-face
   - confidence_threshold: 0.4
   - steps: 20
6. Save Image → Connect to Universal Detailer output

Run this and check the console for detection messages.

### 9. Getting Help

If none of the above helps, please report an issue with:

1. **Console output**: Copy all messages from ComfyUI console
2. **Settings**: Your node settings (steps, confidence, model, etc.)
3. **Test image info**: Resolution, whether it contains faces
4. **System info**: OS, GPU, VRAM amount
5. **ComfyUI version**: Your ComfyUI version

Create an issue at: https://github.com/jjdejong/ComfyUI-UniversalDetailer/issues

## Expected Performance

**Normal timing** (for reference):
- Model loading: 1-3 seconds (first time)
- Detection (yolov8n-face): 0.1-0.5 seconds
- Inpainting (20 steps, 1024x1024): 5-15 seconds
- **Total**: 6-18 seconds for first run, 5-15 seconds for subsequent runs

If your node completes in < 1 second total, something is being skipped.
