# Quick Diagnostic: What Output Are You Seeing?

If you're seeing "dark transparent bounding boxes" instead of enhanced faces, here's how to diagnose:

## Check Your Workflow Connections

The Universal Detailer node has **5 outputs** in this order:

```
Output 0: image (IMAGE) ← THIS is what you want for the final result
Output 1: detection_masks (MASK) ← Shows detected regions as masks
Output 2: face_masks (MASK) ← Face masks only
Output 3: hand_masks (MASK) ← Hand masks only
Output 4: detection_info (STRING) ← JSON debug info
```

### Common Mistake
**Are you connecting Output 1 (detection_masks) to your PreviewImage/SaveImage node?**

If yes, that's why you see bounding boxes! The masks show WHERE faces were detected, not the enhanced result.

### Correct Connection
```
Universal Detailer → Output 0 (image) → PreviewImage or SaveImage
```

## In ComfyUI Workflow

1. **Find your Universal Detailer node**
2. **Look at the output connections** - there should be 5 small circles on the right side
3. **The TOP circle** is the processed image output
4. **Connect the TOP output** to your PreviewImage or SaveImage node

## What Each Output Looks Like

### Output 0 (image) - CORRECT
- Shows your original image with faces/hands enhanced via inpainting
- Faces should look more detailed/corrected
- No bounding boxes visible

### Output 1 (detection_masks) - WRONG for viewing
- Shows gray/white rectangles on black background
- Or dark semitransparent boxes over the image
- This is for debugging detection, not the final result

## Console Log Check

Look for these messages in your ComfyUI console:

**Good signs** (inpainting is working):
```
Found 2 detections
Generating masks for 2 detections
Processing inpainting for detected regions
Starting ComfyUI inpainting process
Running 20 sampling steps with euler
ComfyUI native sampling completed successfully
Step 6: Decoding latents to image
Step 7: Final image blending
ComfyUI inpainting process completed successfully
```

**If you see this instead** (wrong connection):
- You'll still see all the above messages
- But you're viewing the wrong output socket
- Solution: Reconnect to Output 0

## Quick Test

Try this workflow:

1. Universal Detailer node
2. **Connect TOP output (image)** to PreviewImage
3. Run

You should see your enhanced image, NOT bounding boxes.

## Still Seeing Boxes?

If you're DEFINITELY connected to Output 0 and still seeing boxes:

1. **Check if there's a MaskToImage or MaskComposite node** in your workflow
2. **Try Save Image** instead of Preview Image
3. **Share your workflow JSON** so we can debug

## Progress Bar Issue

ComfyUI's native progress bar should show during sampling. If you don't see one:
- This is normal for some ComfyUI versions
- The console logs will show progress ("Sampling step X/20")
- Processing time is expected (5-30 seconds depending on settings)

## Expected Results

**With proper connection to Output 0:**
- Processing time: 5-30 seconds (depending on image size and steps)
- Result: Original image with detected faces/hands enhanced
- No visible bounding boxes
- Faces should look more detailed/corrected per your positive prompt

**If seeing masks:**
- You're connected to Output 1, 2, or 3
- Reconnect to Output 0 (top circle)
