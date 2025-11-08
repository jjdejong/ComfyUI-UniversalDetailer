# MeshGraphormer Hand Fix Workflows

Example ComfyUI workflows for fixing hand anatomy issues using MeshGraphormer + ControlNet.

---

## Workflows Included

### 1. `meshgraphormer_hand_fix_simple.json` ⭐ **RECOMMENDED FOR BEGINNERS**

**Best for:** Quick fixes with minimal setup

**What it does:**
- Uses the all-in-one `MeshGraphormer-ImpactDetector-DepthMapPreprocessor` node
- Automatically detects hands and generates depth maps
- Simpler workflow with fewer nodes

**Key settings:**
- Steps: 35
- CFG: 8.0
- Denoise: 0.85
- ControlNet strength: 0.9

**Use when:**
- You want the easiest setup
- You're new to MeshGraphormer
- You want to quickly test if it works for your image

---

### 2. `meshgraphormer_hand_fix_workflow.json` **ADVANCED**

**Best for:** Maximum control and quality

**What it does:**
- Separate nodes for each step
- More control over each stage
- Better for troubleshooting
- Shows the full pipeline clearly

**Key settings:**
- Steps: 40
- CFG: 8.5
- Denoise: 0.9
- ControlNet strength: 0.9

**Use when:**
- You need to fine-tune each step
- Simple workflow isn't working
- You want to understand the full process
- You need maximum quality

---

## Prerequisites

Before using these workflows, you must install:

### Required Custom Nodes

1. **ComfyUI Impact Pack**
   - Contains: `UltralyticsDetectorProvider`, `BBoxDetectorForEach`
   - Install via ComfyUI Manager: Search "Impact Pack"

2. **ComfyUI ControlNet Auxiliary Preprocessors**
   - Contains: `MeshGraphormer-DepthMapPreprocessor`, `MeshGraphormer-ImpactDetector-DepthMapPreprocessor`
   - Install via ComfyUI Manager: Search "ControlNet Auxiliary" or "controlnet aux"

### Required Models

1. **Hand Detection Model**
   - File: `hand_yolov8s.pt`
   - Location: `ComfyUI/models/ultralytics/bbox/hand_yolov8s.pt`
   - Download: https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8s.pt

2. **ControlNet Depth Model**

   **For SD1.5:**
   - File: `control_v11f1p_sd15_depth.pth`
   - Location: `ComfyUI/models/controlnet/`
   - Download: https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth

   **For SDXL:**
   - File: `diffusers_xl_depth_full.safetensors`
   - Location: `ComfyUI/models/controlnet/`
   - Download: https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusers_xl_depth_full.safetensors

3. **Checkpoint Model**
   - Any SD1.5 or SDXL checkpoint (the workflow uses Realistic Vision as example)
   - Must be photorealistic model for best results with hands
   - Location: `ComfyUI/models/checkpoints/`

4. **MeshGraphormer Model** (Auto-downloads)
   - Downloads automatically on first use (~200MB)
   - Location: `ComfyUI/models/ControlNetPreprocessor/` (auto-created)

---

## How to Use

### Step 1: Load the Workflow

1. Open ComfyUI in your browser
2. Click **"Load"** button
3. Navigate to: `ComfyUI/custom_nodes/ComfyUI-UniversalDetailer/workflows/`
4. Select: `meshgraphormer_hand_fix_simple.json` (recommended for first try)
5. Click **"Open"**

### Step 2: Configure the Workflow

#### Update These Nodes:

**1. LoadImage (Node #1)**
- Click on the node
- Upload or select your image with hand problems
- Image should have hands clearly visible (not tiny)

**2. CheckpointLoaderSimple (Node #4 or #5)**
- Select your checkpoint model
- **Recommended**: Use photorealistic models like:
  - Realistic Vision
  - Deliberate
  - DreamShaper
- **Avoid**: Anime or illustration models (poor hand anatomy understanding)

**3. ControlNetLoader (Node #5 or #6)**
- Verify the correct ControlNet model is selected:
  - SD1.5: `control_v11f1p_sd15_depth.pth`
  - SDXL: `diffusers_xl_depth_full.safetensors`
- Must match your checkpoint version!

**4. UltralyticsDetectorProvider (Node #2)**
- Should show: `bbox/hand_yolov8s.pt`
- If red/error: Install hand detection model (see Prerequisites)

### Step 3: Adjust Settings (Optional)

#### If hands still have wrong finger count after first run:

**Increase ControlNet Strength:**
- Find `ControlNetApply` or `ControlNetApplyAdvanced` node
- Change strength from `0.9` to `0.95`
- This forces stronger anatomical correction

**Increase CFG:**
- Find `KSampler` node
- Change `cfg` from `8.0` to `9.0` or `9.5`
- Makes it follow prompts more strictly

**Increase Denoise:**
- Find `KSampler` node
- Change `denoise` from `0.85` to `0.9` or `0.95`
- Allows more drastic changes

**Change Seed:**
- Find `KSampler` node
- Click the dice icon next to `seed` to randomize
- Some seeds work better than others

#### If hands look too artificial/CGI:

**Decrease Denoise:**
- Find `KSampler` node
- Change `denoise` from `0.85` to `0.75` or `0.7`
- Preserves more original detail

**Decrease CFG:**
- Find `KSampler` node
- Change `cfg` from `8.0` to `7.0` or `7.5`
- Less strict guidance

### Step 4: Run the Workflow

1. Click **"Queue Prompt"** button (bottom right)
2. Watch the progress in the terminal/console
3. First run will download MeshGraphormer model (~200MB) - be patient!
4. Check preview images:
   - Depth map preview shows the anatomically correct hand structure
   - Should show 5 clear fingers in proper positions
5. Check final output in SaveImage node

### Step 5: Verify Results

**Good signs:**
- ✅ Finger count is now correct (5 fingers)
- ✅ Thumb is at proper angle (not parallel to fingers)
- ✅ Hand looks natural and proportional
- ✅ Depth map shows clear hand structure

**If results aren't good:**
- Check depth map preview - if depth map is wrong, MeshGraphormer couldn't detect hand properly
- Try increasing detection threshold in `BBoxDetectorForEach` (0.5 → 0.6)
- Try different seed values
- Increase steps (35 → 40 or 45)
- See Troubleshooting section below

---

## Understanding the Workflow

### Simple Workflow Flow:

```
Load Image
    ↓
MeshGraphormer-ImpactDetector (Detect hands + Generate depth)
    ↓
ControlNet (Apply anatomical guidance)
    ↓
Inpainting Sampler (Regenerate hand)
    ↓
Save Image
```

### Advanced Workflow Flow:

```
Load Image
    ↓
YOLO Hand Detection → Find hand bounding boxes
    ↓
Crop Hand Regions → Isolate each hand
    ↓
MeshGraphormer → Generate anatomically correct depth map
    ↓
ControlNet + Conditioning → Guide with correct anatomy
    ↓
Inpainting → Regenerate hand within mask
    ↓
Composite Back → Blend into original image
    ↓
Save Image
```

---

## Parameter Guide

### Critical Parameters

| Parameter | Location | Recommended | Effect |
|-----------|----------|-------------|--------|
| **ControlNet Strength** | ControlNetApply | 0.85-0.95 | How strongly to follow anatomy guidance |
| **Denoise** | KSampler | 0.8-0.95 | How much to change (higher = more change) |
| **CFG Scale** | KSampler | 7.5-9.0 | How strictly to follow prompts |
| **Steps** | KSampler | 30-45 | Quality vs speed tradeoff |
| **Detection Threshold** | BBoxDetector | 0.4-0.6 | Hand detection sensitivity |
| **Mask Dilation** | BBoxDetector | 10-20 | Mask expansion around hand |

### Parameter Adjustment Guide

**For stubborn wrong finger count:**
```
ControlNet Strength: 0.95
CFG: 9.0-9.5
Denoise: 0.9-0.95
Steps: 40-45
```

**For natural-looking results:**
```
ControlNet Strength: 0.85-0.9
CFG: 7.5-8.0
Denoise: 0.75-0.85
Steps: 30-35
```

**For subtle fixes:**
```
ControlNet Strength: 0.8
CFG: 7.0
Denoise: 0.6-0.7
Steps: 25-30
```

---

## Troubleshooting

### Issue: No hands detected

**Symptoms:** Workflow completes but image unchanged

**Solutions:**
1. Lower `threshold` in BBoxDetectorForEach (0.5 → 0.3)
2. Check hand is visible and not tiny (<100px)
3. Verify `hand_yolov8s.pt` is in correct location
4. Check ComfyUI console for detection errors

### Issue: Depth map looks wrong

**Symptoms:** MeshGraphormer depth preview doesn't show clear hand

**Solutions:**
1. Hand might be too small - crop/zoom the input image
2. Hand might be obscured - ensure hand is clearly visible
3. Unusual hand pose - MeshGraphormer works best with natural poses
4. Increase `dilation` to include more context around hand

### Issue: Still has 6 fingers

**Symptoms:** Finger count still wrong after processing

**Solutions:**
1. **Increase ControlNet strength to 0.95**
2. **Increase CFG to 9.0 or higher**
3. **Increase denoise to 0.95**
4. Add emphasis to prompts:
   - Positive: `(exactly five fingers:1.4)`, `(one thumb four fingers:1.3)`
   - Negative: `(6 fingers:1.6)`, `(extra finger:1.5)`
5. Try multiple seeds - some work better than others
6. Increase steps to 45-50

### Issue: Thumb still looks like finger

**Symptoms:** Thumb parallel to fingers or wrong angle

**Solutions:**
1. Check MeshGraphormer depth preview - thumb should be angled
2. If depth map shows correct thumb but output doesn't:
   - Increase ControlNet strength to 0.95
   - Add to negative: `(thumb parallel to fingers:1.5)`
   - Add to positive: `(opposable thumb:1.3)`
3. Try different seed

### Issue: Hand looks artificial/CGI

**Symptoms:** Hand is anatomically correct but looks fake

**Solutions:**
1. **Lower denoise to 0.7-0.8**
2. **Lower CFG to 7.0-7.5**
3. Add to prompts:
   - Positive: `natural skin texture`, `realistic lighting`, `photorealistic`
4. Check checkpoint model - must be photorealistic, not anime
5. Increase crop_factor to include more surrounding context

### Issue: Background around hand changes

**Symptoms:** Area around hand is different from original

**Solutions:**
1. Reduce `dilation` in BBoxDetector (20 → 10)
2. Lower `denoise` (0.85 → 0.75)
3. Reduce `grow_mask_by` in VAEEncodeForInpaint (6 → 3)
4. Use mask blur/feather (add GrowMask node with negative value)

### Issue: "Error loading node" or missing nodes

**Symptoms:** Red nodes, workflow won't load

**Solutions:**
1. Install missing custom nodes via ComfyUI Manager
2. Check Prerequisites section - install all required nodes
3. Restart ComfyUI after installing nodes
4. Check console for specific missing node errors

### Issue: Out of memory

**Symptoms:** CUDA out of memory error

**Solutions:**
1. Reduce resolution in MeshGraphormer preprocessor (512 → 384)
2. Close other programs using GPU
3. Enable model offloading in ComfyUI settings
4. Reduce image size before processing
5. Use fp16 checkpoint models instead of fp32

---

## Prompt Templates

### For Extra Fingers (6→5)

**Positive:**
```
masterpiece, best quality, realistic human hand, (exactly five fingers:1.3),
detailed hand anatomy, (one thumb four fingers:1.2), proper finger count,
natural proportions, photorealistic skin, well-defined knuckles
```

**Negative:**
```
(6 fingers:1.6), (extra finger:1.5), (seven fingers:1.4), (six digits:1.4),
deformed hand, bad anatomy, extra digit, fewer digits, fused fingers,
mutated hand, disfigured
```

### For Missing Fingers (4→5)

**Positive:**
```
complete hand, (five fingers:1.4), (full set of fingers:1.3), all fingers visible,
detailed hand anatomy, one thumb and four fingers, no missing digits,
complete hand structure, natural proportions
```

**Negative:**
```
(missing fingers:1.6), (4 fingers:1.5), (three fingers:1.4), (incomplete hand:1.4),
fewer digits, cut off fingers, partial hand, amputated, deformed
```

### For Wrong Thumb Position

**Positive:**
```
detailed hand, (proper thumb anatomy:1.3), (opposable thumb:1.3),
thumb at natural angle, correct thumb position, thumb distinct from fingers,
realistic hand structure, five digits with proper thumb placement
```

**Negative:**
```
(thumb parallel to fingers:1.6), (thumb like finger:1.5), (five identical fingers:1.4),
wrong thumb position, thumb in line with fingers, incorrect thumb angle,
bad hand anatomy
```

---

## Success Tips

1. **Use photorealistic checkpoints** - Anime models don't understand hand anatomy well
2. **Hands should be clearly visible** - At least 150x150px in the original image
3. **Try multiple seeds** - Results vary significantly with different seeds
4. **Start with simple workflow** - Master it before moving to advanced
5. **Check depth map preview** - If depth is wrong, result will be wrong
6. **Be patient** - First run downloads models (~200MB)
7. **Iterate** - Adjust one parameter at a time to see effect
8. **Save working settings** - When you find settings that work, save the workflow

---

## Expected Results

### Success Rates (Based on Community Reports)

| Issue | Success Rate | Notes |
|-------|--------------|-------|
| 6 fingers → 5 fingers | 85-90% | High success if hand clearly visible |
| 4 fingers → 5 fingers | 80-85% | May need multiple attempts |
| Thumb like finger → proper thumb | 90-95% | MeshGraphormer excels at this |
| Fused fingers → separated | 70-80% | Harder, may need manual touch-up |
| Multiple issues | 60-75% | May need 2-3 iterations |

### Processing Time

- **First run**: 2-4 minutes (model download + inference)
- **Subsequent runs**: 30-90 seconds per image
- **GPU**: RTX 3060 or better recommended
- **VRAM**: 8GB minimum, 10GB+ recommended

---

## Combining with Face Detailing

To process both faces and hands in one workflow:

1. Add FaceDetailer node before the hand detection
2. Connect FaceDetailer output to the hand detection input
3. Process faces first, then hands
4. See main FIXING_HAND_ANATOMY.md guide for detailed example

---

## Next Steps

Once you've mastered these workflows:

1. **Experiment with settings** - Find optimal values for your images
2. **Try different checkpoints** - Some models work better than others
3. **Combine techniques** - Use FaceDetailer for faces, MeshGraphormer for hands
4. **Create variations** - Modify workflows for your specific needs
5. **Share results** - Help the community by sharing what works

---

## Getting Help

If you're stuck:

1. **Check the depth map preview** - Is MeshGraphormer detecting the hand?
2. **Check console output** - Look for error messages
3. **Review Prerequisites** - Are all models and nodes installed?
4. **Try the simple workflow** - Easier to troubleshoot
5. **Adjust one parameter at a time** - Systematic debugging
6. **See main guides**:
   - `FIXING_HAND_ANATOMY.md` - Complete guide
   - `INSTALLATION_TROUBLESHOOTING.md` - Installation help
   - `HAND_FIXING_GUIDE.md` - Alternative methods

---

## Additional Resources

- **Main Guide**: `../FIXING_HAND_ANATOMY.md`
- **Installation Help**: `../INSTALLATION_TROUBLESHOOTING.md`
- **ControlNet Aux GitHub**: https://github.com/Fannovel16/comfyui_controlnet_aux
- **Impact Pack GitHub**: https://github.com/ltdrdata/ComfyUI-Impact-Pack
- **ComfyUI Workflows**: https://comfyworkflows.com (search "hand fix")
- **Civitai**: https://civitai.com/models (search "hand detailer workflow")

---

Good luck fixing those hands! 🖐️
