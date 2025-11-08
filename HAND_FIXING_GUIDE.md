# Complete Guide to Hand Fixing in ComfyUI

**For beginners: Step-by-step guide to fixing distorted hands alongside your FaceDetailer workflow**

---

## Table of Contents
1. [Understanding the Options](#understanding-the-options)
2. [Method 1: Impact Pack Hand Detection (Easiest)](#method-1-impact-pack-hand-detection-easiest)
3. [Method 2: BMAB Simple Hand Detailer](#method-2-bmab-simple-hand-detailer)
4. [Method 3: Flux Fill + SegmentAnything (2025 State-of-the-Art)](#method-3-flux-fill--segmentanything-2025-state-of-the-art)
5. [Method 4: MeshGraphormer + ControlNet (For Severe Distortions)](#method-4-meshgraphormer--controlnet-for-severe-distortions)
6. [Comparison Chart](#comparison-chart)
7. [Troubleshooting](#troubleshooting)

---

## Understanding the Options

Before we dive in, here's what each method does:

| Method | Best For | Difficulty | GPU Required | Success Rate |
|--------|----------|------------|--------------|--------------|
| Impact Pack | Quick fixes, same workflow as FaceDetailer | Easy | 6GB+ | 70-80% |
| BMAB Hand Detailer | Automated hand enhancement | Easy | 6GB+ | 75-85% |
| Flux Fill + SegmentAnything | High-quality hand reconstruction | Medium | 8GB+ | 85-90% |
| MeshGraphormer + ControlNet | Fixing wrong geometry (extra/missing fingers) | Advanced | 8GB+ | 90% (for geometry) |

---

## Method 1: Impact Pack Hand Detection (Easiest)

**This is the simplest approach - use the same FaceDetailer node you already have, just with a different detector!**

### What You Need
- ComfyUI Impact Pack (you already have this if you're using FaceDetailer)
- Hand detection model: `hand_yolov8s.pt`

### Step 1: Download the Hand Detection Model

The hand detection model should be available through Impact Pack's model manager, or download manually:

```bash
# Navigate to your ComfyUI directory
cd ComfyUI/models/ultralytics/bbox/

# Download the hand detection model
# Option 1: Use Impact Pack's model downloader (recommended)
# In ComfyUI: Manager > Install Models > Search "hand_yolov8s"

# Option 2: Manual download
wget https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8s.pt
```

### Step 2: Basic Workflow (Add to Your Existing FaceDetailer Setup)

Here's how to add hand detection to your workflow:

```
[Your Image Source]
    |
    ├─> FaceDetailer (for faces) ──> [Output]
    |      ↑
    |      └─ UltralyticsDetectorProvider (bbox/face_yolov8s.pt)
    |
    └─> FaceDetailer (for hands) ──> [Output]
           ↑
           └─ UltralyticsDetectorProvider (bbox/hand_yolov8s.pt)
```

### Step 3: Node Configuration

**For the Hand FaceDetailer node:**
- **bbox_detector**: Connect UltralyticsDetectorProvider with `hand_yolov8s.pt`
- **bbox_threshold**: 0.5 (increase to 0.6-0.7 if detecting too many false positives)
- **bbox_dilation**: 10-20 (expands the detection box around hands)
- **crop_factor**: 2.0-3.0 (how much context around the hand to include)
- **guide_size**: 512 or 768 (resolution for inpainting)
- **guide_size_for**: true (maintains aspect ratio)
- **max_size**: 1024
- **denoise**: 0.4-0.6 (lower = preserve more original, higher = more changes)

### Step 4: Complete Example Workflow

```
Load Image
    ├─> VAEEncode ──> [latents]
    |
    ├─> CLIP Text Encode (Positive) ──> "masterpiece, best quality, detailed hands, five fingers"
    |
    ├─> CLIP Text Encode (Negative) ──> "blurry, distorted, deformed hands, extra fingers, missing fingers"
    |
    └─> FaceDetailer (FACES)
           ├─ model: [Your checkpoint]
           ├─ clip: [Your CLIP]
           ├─ vae: [Your VAE]
           ├─ positive: [Face positive prompt]
           ├─ negative: [Face negative prompt]
           ├─ bbox_detector: UltralyticsDetectorProvider (face_yolov8s.pt)
           ├─ guide_size: 512
           ├─ denoise: 0.35
           |
           └──> FaceDetailer (HANDS)
                  ├─ model: [Your checkpoint]
                  ├─ clip: [Your CLIP]
                  ├─ vae: [Your VAE]
                  ├─ positive: "detailed hands, five fingers, natural hand pose"
                  ├─ negative: "deformed hands, extra fingers, missing fingers, fused fingers"
                  ├─ bbox_detector: UltralyticsDetectorProvider (hand_yolov8s.pt)
                  ├─ guide_size: 768
                  ├─ denoise: 0.5
                  ├─ crop_factor: 2.5
                  |
                  └──> Save Image / Preview
```

### Tips for Better Results
- **Prompts matter**: Include "five fingers", "detailed hands" in positive prompt
- **Denoise setting**: Start at 0.4, increase if hands are still broken, decrease if changing too much
- **Crop factor**: Larger values (2.5-3.0) give more context for natural-looking hands
- **Sequential processing**: Process faces first, then hands (chain the nodes)

---

## Method 2: BMAB Simple Hand Detailer

**A dedicated node specifically designed for hand enhancement**

### Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/portu-sim/comfyui_bmab.git
cd comfyui_bmab
pip install -r requirements.txt

# Restart ComfyUI
```

### What It Does
BMAB (Better Mask and Blur) Hand Detailer is a specialized node that:
- Automatically detects hands
- Creates precise masks around hand regions
- Applies targeted enhancement
- Handles multiple hands in one pass

### Basic Workflow

```
Load Image
    |
    └─> BMAB Simple Hand Detailer
           ├─ model: [Your checkpoint]
           ├─ clip: [Your CLIP]
           ├─ vae: [Your VAE]
           ├─ positive: "detailed hands, perfect fingers, natural pose"
           ├─ negative: "deformed hands, extra digits, fused fingers"
           ├─ seed: [random or fixed]
           ├─ steps: 20-30
           ├─ cfg: 7.0-8.0
           ├─ sampler_name: "euler_a" or "dpmpp_2m"
           ├─ scheduler: "normal" or "karras"
           ├─ denoise: 0.4-0.6
           ├─ dilation: 10-20 (mask expansion)
           |
           └──> Save Image
```

### Advanced: Combining Face and Hand Detailers

```
Load Image
    |
    ├─> FaceDetailer (process faces first)
    |      ├─ [standard face settings]
    |      |
    |      └──> BMAB Simple Hand Detailer (then hands)
    |             ├─ [hand settings from above]
    |             |
    |             └──> Save Image
```

### BMAB Node Parameters Explained

- **dilation**: How much to expand the mask around detected hands (10-20 pixels recommended)
- **denoise**: How much to change the hand (0.4 = subtle fix, 0.6 = major reconstruction)
- **steps**: More steps = better quality but slower (20-30 is good)
- **cfg**: Classifier Free Guidance - how closely to follow your prompt (7-8 recommended)

---

## Method 3: Flux Fill + SegmentAnything (2025 State-of-the-Art)

**The most advanced method for high-quality hand reconstruction**

### What You Need
- **Flux Fill model**: `flux1-fill-dev.safetensors` (~23GB)
- **SegmentAnythingUltra V2** custom node
- **SAM model**: `sam_vit_h_4b8939.pth` (~2.5GB)
- At least 8GB VRAM

### Installation

#### Step 1: Install Flux Fill

```bash
# Download Flux Fill model
cd ComfyUI/models/unet/

# Option 1: Use ComfyUI Manager
# Manager > Install Models > Search "Flux Fill"

# Option 2: Manual download from HuggingFace
# Visit: https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev
# Download: flux1-fill-dev.safetensors
```

#### Step 2: Install SegmentAnythingUltra V2

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/neverbiasu/ComfyUI-SAM2.git
cd ComfyUI-SAM2
pip install -r requirements.txt

# Download SAM model
cd ../../models/sams/
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

#### Step 3: Install Required Nodes

You'll also need:
- **ComfyUI-FluxFill** (for Flux Fill nodes)
- **ComfyUI-Essentials** (for mask operations)

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/kijai/ComfyUI-FluxFill.git
git clone https://github.com/cubiq/ComfyUI_essentials.git

# Install dependencies
cd ComfyUI-FluxFill && pip install -r requirements.txt
cd ../ComfyUI_essentials && pip install -r requirements.txt
```

### Basic Flux Fill + SAM Workflow

```
Load Image
    |
    ├──> SAM2AutoSegmentation (Detect hands)
    |       ├─ sam_model: SAMModelLoader (sam_vit_h_4b8939.pth)
    |       ├─ detection_prompt: "hand"
    |       ├─ threshold: 0.5
    |       |
    |       └──> [Mask Output]
    |               |
    |               └──> GrowMask (Expand mask by 30 pixels)
    |                       |
    |                       └──> [Expanded Mask]
    |
    └──> FluxFillNode
            ├─ image: [Original Image]
            ├─ mask: [Expanded Mask from SAM2]
            ├─ flux_model: [flux1-fill-dev]
            ├─ positive: "detailed human hand, five fingers, natural skin texture, proper anatomy"
            ├─ negative: "deformed, extra fingers, fused digits, unnatural"
            ├─ seed: [random]
            ├─ steps: 28-35
            ├─ cfg_scale: 3.5
            ├─ denoise: 0.85-1.0
            |
            └──> Save Image
```

### Complete Flux Fill Workflow Example

Here's a full workflow you can implement:

```
[1] Load Image ────────────┬──────────────────────────────────────────┐
                           │                                          │
                           │                                          │
[2] SAMModelLoader ────────┤                                          │
    (sam_vit_h_4b8939.pth) │                                          │
                           │                                          │
[3] SAM2AutoSegmentation ──┤                                          │
    ├─ sam_model: [2]      │                                          │
    ├─ image: [1]          │                                          │
    ├─ prompt: "hand"      │                                          │
    └─ threshold: 0.5      │                                          │
         │                 │                                          │
         v                 │                                          │
[4] GrowMask ──────────────┤                                          │
    ├─ mask: [3]           │                                          │
    └─ expand: 30          │                                          │
         │                 │                                          │
         v                 │                                          │
[5] MaskToImage ───────────┤ (optional - for preview)                │
    └─ mask: [4]           │                                          │
         │                 │                                          │
[6] Load Flux Fill ────────┤                                          │
    (flux1-fill-dev)       │                                          │
                           │                                          │
[7] CLIPTextEncode ────────┤                                          │
    (positive prompt)      │                                          │
    "detailed hand, 5      │                                          │
    fingers, natural"      │                                          │
                           │                                          │
[8] CLIPTextEncode ────────┤                                          │
    (negative prompt)      │                                          │
    "extra fingers,        │                                          │
    deformed"              │                                          │
                           │                                          │
[9] FluxFillSampler ───────┴──────────────────────────────────────────┤
    ├─ model: [6]                                                     │
    ├─ positive: [7]                                                  │
    ├─ negative: [8]                                                  │
    ├─ image: [1]                                                     │
    ├─ mask: [4]                                                      │
    ├─ steps: 30                                                      │
    ├─ cfg: 3.5                                                       │
    ├─ denoise: 0.9                                                   │
    └─ seed: random                                                   │
         │                                                            │
         v                                                            │
[10] Save Image ───────────────────────────────────────────────────────┘
```

### Recommended Settings for Flux Fill

**For subtle fixes (slightly distorted hands):**
- Steps: 28
- CFG Scale: 3.5
- Denoise: 0.75-0.85

**For major reconstruction (very broken hands):**
- Steps: 35
- CFG Scale: 4.0
- Denoise: 0.9-1.0

**Prompts:**
- Positive: "detailed human hand, five fingers, natural skin texture, proper hand anatomy, realistic lighting"
- Negative: "deformed hand, extra fingers, missing fingers, fused digits, mutated hand, extra limbs"

### Why Flux Fill is Better

1. **Architecture**: Flux Fill is specifically trained for inpainting/filling, not adapted from text-to-image
2. **Context awareness**: Better understands surrounding image context
3. **Anatomy understanding**: Better at generating correct hand anatomy
4. **Edge blending**: Seamless integration with the original image
5. **Consistency**: More consistent results across different hand poses

---

## Method 4: MeshGraphormer + ControlNet (For Severe Distortions)

**For fixing hands with wrong number of fingers, impossible poses, or severe geometric distortions**

### What This Method Does Differently

MeshGraphormer creates a 3D hand pose model, which guides the image generation to produce anatomically correct hands. This is crucial when:
- Hands have extra or missing fingers
- Fingers are in impossible positions
- The hand structure is fundamentally wrong

### What You Need
- **ComfyUI-MeshGraphormer** custom node
- **ControlNet Depth model** (compatible with your checkpoint version)
- **Hand detection** (YOLO or SAM)
- 8GB+ VRAM

### Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/ZHO-ZHO-ZHO/ComfyUI-MeshGraphormer.git
cd ComfyUI-MeshGraphormer
pip install -r requirements.txt

# Download ControlNet Depth model
cd ../../models/controlnet/

# For SD1.5:
wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth

# For SDXL:
wget https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusers_xl_depth_full.safetensors
```

### How It Works

```
Original Image
    │
    ├──> Detect Hands (YOLO or SAM)
    │       └──> Hand Bounding Boxes
    │
    ├──> MeshGraphormer Hand Detector
    │       ├─ Input: Cropped hand images
    │       ├─ Output: 3D hand mesh
    │       └──> Depth Map (anatomically correct hand structure)
    │
    └──> ControlNet + Inpainting
            ├─ Image: Original
            ├─ Mask: Hand region
            ├─ ControlNet: Depth map from MeshGraphormer
            ├─ Prompt: "detailed hand, five fingers"
            └──> Reconstructed image with correct hand geometry
```

### Complete MeshGraphormer Workflow

```
[1] Load Image
    │
    ├──> [2] UltralyticsDetector (hand_yolov8s)
    │       └──> [Hand Boxes]
    │
    ├──> [3] CropImageByMask
    │       ├─ image: [1]
    │       └─ mask: [2]
    │           └──> [Cropped Hand Images]
    │
    ├──> [4] MeshGraphormer Hand Refiner
    │       ├─ image: [3]
    │       └──> [Hand Depth Map]
    │           │
    │           └──> [5] Resize (to match original hand size)
    │                   └──> [Resized Depth]
    │
    ├──> [6] Load ControlNet Model
    │       (control_depth)
    │
    ├──> [7] Load Checkpoint
    │
    ├──> [8] CLIP Text Encode (Positive)
    │       "perfect hand, five fingers, natural hand pose, detailed skin texture"
    │
    ├──> [9] CLIP Text Encode (Negative)
    │       "deformed hand, extra fingers, missing fingers, wrong anatomy, mutated"
    │
    ├──> [10] Apply ControlNet
    │       ├─ positive: [8]
    │       ├─ controlnet: [6]
    │       ├─ image: [5] (depth map)
    │       └─ strength: 0.8-1.0
    │
    └──> [11] KSampler (Inpaint)
            ├─ model: [7]
            ├─ positive: [10]
            ├─ negative: [9]
            ├─ latent_image: [1] (encoded)
            ├─ mask: [2] (hand mask)
            ├─ steps: 30-40
            ├─ cfg: 7.5
            ├─ denoise: 0.75-0.9
            └──> [12] VAE Decode
                    └──> [13] Save Image
```

### MeshGraphormer Settings

**ControlNet Settings:**
- **strength**: 0.8-1.0 (higher = follow depth map more strictly)
- **start_percent**: 0.0
- **end_percent**: 0.9 (let the last 10% refine details)

**Sampling Settings:**
- **steps**: 30-40 (more steps for complex corrections)
- **cfg**: 7.5-8.5
- **denoise**: 0.75 for subtle fixes, 0.9 for major reconstruction

### When to Use MeshGraphormer

✅ **USE when:**
- Hand has 6+ fingers or less than 4 fingers
- Fingers are fused together
- Hand pose is anatomically impossible
- Hand proportions are severely wrong

❌ **DON'T USE when:**
- Hand is just slightly blurry (use simple detailer)
- Minor detail issues (use Flux Fill instead)
- Hand is mostly correct (overkill)

---

## Comparison Chart

### Quick Reference: Which Method to Use?

| Issue | Recommended Method | Why |
|-------|-------------------|-----|
| Slightly blurry hands | Impact Pack + Hand YOLO | Fastest, simplest |
| Hand proportions slightly off | BMAB Hand Detailer | Good automation |
| Distorted but recognizable hands | Flux Fill + SAM | Best quality reconstruction |
| 6 fingers or wrong geometry | MeshGraphormer + ControlNet | Fixes anatomy |
| Multiple hands in image | Flux Fill + SAM or BMAB | Handles multiple detections |
| Limited VRAM (<8GB) | Impact Pack + Hand YOLO | Most memory efficient |

### Performance Comparison

| Method | Speed | VRAM | Quality | Success Rate |
|--------|-------|------|---------|--------------|
| Impact Pack | Fast (5-10s) | 6GB | Good | 70-80% |
| BMAB | Fast (5-10s) | 6GB | Good | 75-85% |
| Flux Fill | Slow (30-60s) | 8-12GB | Excellent | 85-90% |
| MeshGraphormer | Very Slow (60-90s) | 8-12GB | Excellent (anatomy) | 90% (geometry) |

---

## Complete Example: Face + Hand Pipeline

Here's how to combine everything into one comprehensive workflow:

### Option A: Simple Pipeline (Impact Pack Only)

```
Load Image
    ↓
FaceDetailer (face_yolov8s) ← Fix faces first
    ↓
FaceDetailer (hand_yolov8s) ← Then fix hands
    ↓
Save Image
```

### Option B: Quality Pipeline (Flux Fill)

```
Load Image
    ├──> FaceDetailer (faces) ──┐
    │                            │
    └──> SAM2 (hands) ──────────┤
            ↓                    │
         GrowMask                │
            ↓                    │
         FluxFill ───────────────┘
            ↓
         Save Image
```

### Option C: Maximum Quality Pipeline (MeshGraphormer)

```
Load Image
    ├──> FaceDetailer (faces) ──┐
    │                            │
    ├──> YOLO (hands) ───────────┤
    │         ↓                  │
    │    MeshGraphormer          │
    │         ↓                  │
    │    ControlNet Depth        │
    │         ↓                  │
    └──> Inpaint (guided) ───────┘
            ↓
         Save Image
```

---

## Troubleshooting

### Issue: Hand detector finds faces instead of hands
**Solution:**
- Lower the `bbox_threshold` to 0.3-0.4 for more strict detection
- Ensure you're using `hand_yolov8s.pt`, not `face_yolov8s.pt`
- Check that the model file is in the correct directory

### Issue: Fixed hands look unnatural or blurry
**Solution:**
- Increase `guide_size` to 768 or 1024
- Lower `denoise` to 0.35-0.45 (preserve more original)
- Adjust `crop_factor` to 3.0-4.0 (more context)
- Improve your positive prompt: "detailed hands, natural skin, five fingers, realistic"

### Issue: Hands still have wrong number of fingers
**Solution:**
- Use MeshGraphormer method for anatomical correction
- Add strong negative prompts: "extra fingers, missing fingers, 6 fingers, 4 fingers"
- Increase denoise to 0.7-0.9 for more aggressive reconstruction
- Try multiple seeds (some work better than others)

### Issue: Flux Fill changes the background around hands
**Solution:**
- Reduce mask expansion in GrowMask (try 15-20 instead of 30)
- Lower denoise to 0.7-0.8
- Use MaskBlur to soften mask edges
- Add detail to positive prompt about preserving background

### Issue: Out of memory errors
**Solution:**
- Reduce `guide_size` to 384 or 512
- Enable model offloading in ComfyUI settings
- Use fp16 or bf16 models instead of fp32
- Process hands one at a time instead of batch
- Use Impact Pack method instead of Flux Fill

### Issue: Nothing happens / No hands detected
**Solution:**
- Check that hands are visible and not tiny in the image
- Lower `bbox_threshold` to 0.3
- Verify model downloaded correctly: `ComfyUI/models/ultralytics/bbox/hand_yolov8s.pt`
- For SAM: ensure `sam_vit_h_4b8939.pth` is in `models/sams/`
- Check console for error messages

### Issue: Results are inconsistent
**Solution:**
- Use a fixed seed instead of random
- Increase sampling steps (25-35)
- Adjust CFG scale (try 7.0, 7.5, 8.0)
- Ensure scheduler is set to "karras" or "normal"
- Use the same checkpoint/VAE consistently

---

## Recommended Prompts

### For Hands - Positive Prompts
```
"detailed human hand, five fingers, natural skin texture, proper hand anatomy, realistic lighting, natural hand pose"

"perfect hands, detailed fingers, natural skin, anatomically correct, well-defined knuckles"

"realistic hand, five digits, natural proportions, detailed palm lines, proper finger placement"
```

### For Hands - Negative Prompts
```
"deformed hands, extra fingers, missing fingers, fused fingers, mutated hands, malformed digits, extra limbs, poorly drawn hands, 6 fingers, 4 fingers, disconnected fingers, floating fingers, merged hands"

"bad hands, bad anatomy, extra digit, fewer digits, cropped hands, worst quality, low quality, jpeg artifacts"
```

### Combining Face and Hand Prompts
```
Positive: "masterpiece, best quality, detailed face, perfect hands, five fingers, natural skin, realistic proportions, detailed features"

Negative: "deformed, extra fingers, extra limbs, bad anatomy, bad hands, bad face, disfigured, poorly drawn, mutation, mutated"
```

---

## Next Steps

1. **Start simple**: Try Impact Pack method first (easiest to set up)
2. **Test on variety of images**: See which method works best for your use case
3. **Experiment with settings**: Denoise and crop_factor make the biggest difference
4. **Save working configurations**: When you find settings that work, save the workflow
5. **Upgrade when needed**: If simple methods don't work, move to Flux Fill or MeshGraphormer

---

## Additional Resources

### Model Downloads
- **Hand YOLO**: https://huggingface.co/Bingsu/adetailer
- **Flux Fill**: https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev
- **SAM models**: https://github.com/facebookresearch/segment-anything#model-checkpoints
- **ControlNet Depth**: https://huggingface.co/lllyasviel/ControlNet-v1-1

### Useful Custom Nodes
- **Impact Pack**: https://github.com/ltdrdata/ComfyUI-Impact-Pack
- **BMAB**: https://github.com/portu-sim/comfyui_bmab
- **Flux Fill**: https://github.com/kijai/ComfyUI-FluxFill
- **SAM2**: https://github.com/neverbiasu/ComfyUI-SAM2
- **MeshGraphormer**: https://github.com/ZHO-ZHO-ZHO/ComfyUI-MeshGraphormer

### Community Resources
- **ComfyUI Examples**: https://comfyworkflows.com (search "hand fix")
- **Civitai Workflows**: https://civitai.com/models (filter by "hand detailer")
- **Reddit**: r/comfyui (search "fixing hands")

---

## Conclusion

**For most users**, start with **Impact Pack + Hand YOLO** (Method 1) because:
- It's already installed if you use FaceDetailer
- Same workflow structure you know
- Fast and memory efficient
- Good results for 70-80% of cases

**Upgrade to Flux Fill** (Method 3) when:
- You need the highest quality
- You have 8GB+ VRAM
- Simple methods aren't working well enough
- You're doing professional/commercial work

**Use MeshGraphormer** (Method 4) only when:
- Hands have fundamentally wrong anatomy
- You're willing to invest time in setup and tweaking
- Other methods have failed

Good luck fixing those hands! 🖐️
