# Parameter Guide - Universal Detailer

> **Complete guide to all parameters with recommendations and explanations**

## Quick Reference

| Parameter | Type | Default | Range | Recommended | Purpose |
|-----------|------|---------|-------|-------------|---------|
| target_parts | STRING | "face,hand" | - | "face" or "face,hand" | Which body parts to detect |
| model_quality | CHOICE | "fast" | fast/balanced/quality | "fast" for testing, "quality" for final | Detection accuracy vs speed |
| confidence_threshold | FLOAT | 0.5 | 0.1-0.95 | 0.3-0.5 | How confident detection must be |
| mask_padding | INT | 32 | 0-128 | 24-48 | Extra pixels around detection |
| mask_blur | INT | 8 | 0-50 | 8-15 (auto-scales) | Edge softness |
| inpaint_strength | FLOAT | 0.75 | 0.1-1.0 | 0.6-0.85 | How much to change detected area |
| steps | INT | 20 | 1-100 | 15-30 | Sampling quality |
| cfg_scale | FLOAT | 7.0 | 1.0-30.0 | 3.0-8.0 | Prompt adherence strength |
| seed | INT | -1 | -1 or positive | -1 (random) | Reproducibility |
| sampler_name | CHOICE | "euler" | various | "euler" or "dpm_2" | Sampling algorithm |
| scheduler | CHOICE | "normal" | various | "normal" or "karras" | Noise schedule |
| auto_face_fix | BOOL | True | True/False | True | Process detected faces |
| auto_hand_fix | BOOL | True | True/False | True | Process detected hands |

---

## Detection Parameters

### target_parts
**What it does**: Comma-separated list of body parts to detect and enhance.

**Valid values**:
- `"face"` - Detect only faces
- `"hand"` - Detect only hands
- `"face,hand"` - Detect both faces and hands (most common)

**Recommendations**:
- ✅ **Use "face"** for portrait fixes, headshots
- ✅ **Use "face,hand"** for full-body images, character art
- ✅ **Use "hand"** when only fixing hand issues
- ⚠️ More parts = longer processing time (multiple models run)

**How it works**: The node automatically loads the appropriate detection models:
- `face` → YOLOv8-face model
- `hand` → YOLOv8-hand model
- Both parts run separate detections and combine results

---

### model_quality
**What it does**: Controls which detection model variant to use - faster but less accurate, or slower but more accurate.

**Options**:
- `"fast"` - YOLOv8n models (6MB each, fastest)
- `"balanced"` - YOLOv8n models (same as fast currently)
- `"quality"` - YOLOv8s models (22MB each, higher accuracy)

**Recommendations**:
- ✅ **Use "fast"** for: Testing, iterations, lower resolution images (<1024px)
- ✅ **Use "quality"** for: Final renders, high-res images (>2048px), difficult detections
- 📊 **Speed difference**: ~30-50% slower for quality mode
- 📊 **Accuracy difference**: ~5-10% better detection rate for quality mode

**Trade-offs**:
- Fast mode might miss small/obscured faces or hands
- Quality mode better for side profiles, partially hidden hands
- Memory: Quality uses ~3x more VRAM per model

---

### confidence_threshold
**What it does**: Minimum confidence score (0-1) for accepting a detection. Lower = more detections (including false positives), higher = fewer detections (only very confident).

**Range**: 0.1 to 0.95 (step 0.05)
**Default**: 0.5

**Recommendations by use case**:
- **0.3-0.4**: "Find everything possible"
  - Good for: Finding small/distant faces, partially occluded hands
  - Risk: May detect background objects as faces/hands
  - Use when: You're getting missed detections at higher thresholds

- **0.5-0.6**: "Balanced" (DEFAULT)
  - Good for: Most images, general use
  - Filters out obvious false positives
  - Reliable for clear, well-lit subjects

- **0.7-0.8**: "Only obvious ones"
  - Good for: Reducing false positives in complex scenes
  - Use when: Getting unwanted detections on objects
  - Risk: May miss legitimate but difficult faces/hands

**Diagnostic tip**: If you're not getting detections:
1. First check detection_info output to see if anything was found
2. Try lowering to 0.3 temporarily
3. If still nothing, detection model might not recognize the style (anime, abstract art, etc.)

---

## Mask Parameters

### mask_padding
**What it does**: Expands the detection bounding box by N pixels in all directions before creating the mask.

**Range**: 0 to 128 pixels (step 4)
**Default**: 32

**Recommendations**:
- ✅ **24-32px**: Standard for faces, includes hair/ears
- ✅ **40-64px**: For hands, includes wrists/arms
- ✅ **16-24px**: Tight crops, when you want minimal change
- ❌ **Avoid 0px**: No context for inpainting = harsh edges

**Visual guide**:
```
Padding 0px:  ┌─────┐        (just the detected box)
Padding 32px: ┌─────────┐    (includes surrounding context)
Padding 64px: ┌───────────┐  (larger context area)
```

**Why it matters**: Padding provides surrounding context for the inpainting model:
- Too little: Model has no context, creates disconnected-looking fixes
- Too much: Changes more of the image than needed, slower processing
- For faces: Include hair, neck, part of shoulders
- For hands: Include wrist, part of forearm

---

### mask_blur
**What it does**: Applies Gaussian blur to mask edges to create smooth transitions. Higher values = softer edges.

**Range**: 0 to 50 pixels (step 1)
**Default**: 8

**⚠️ IMPORTANT**: This value is **automatically scaled** based on image resolution!
- Small images (<1024px): Uses blur value as-is
- Large images (1024-2048px): 2-3x multiplier
- Very large images (>2048px): 3-4x multiplier

**Recommendations**:
- ✅ **8-12**: Default range, works for most images
- ✅ **15-20**: Extra soft blending for high-res images
- ✅ **4-6**: Sharper transitions, technical accuracy over aesthetics
- ❌ **0**: Hard edges, visible box outlines (not recommended)

**Examples** (for a 3456px wide image):
- Input `mask_blur=8` → Effective blur ~27px (3.4x scaling)
- Input `mask_blur=15` → Effective blur ~51px (3.4x scaling)

**Why adaptive scaling?**:
A 4px blur is barely visible on a 4K image but very soft on a 512px image. Adaptive scaling ensures consistent visual results across resolutions.

---

## Inpainting Parameters

### inpaint_strength
**What it does**: Controls how much the inpainting can change the masked area. Similar to "denoising strength" in standard inpainting.

**Range**: 0.1 to 1.0 (step 0.05)
**Default**: 0.75

**Recommendations by goal**:
- **0.6-0.7**: "Subtle enhancement"
  - Keeps most original detail
  - Good for: Minor fixes, skin texture, slight corrections
  - Example: "Fix this finger angle slightly"

- **0.75-0.85**: "Balanced regeneration" (RECOMMENDED)
  - Good mix of original and new
  - Good for: Face improvements, hand corrections
  - Example: "Make this face prettier while keeping likeness"

- **0.85-0.95**: "Heavy regeneration"
  - Almost completely new content
  - Good for: Badly malformed hands, very low quality faces
  - Risk: May change identity/style significantly

- **1.0**: "Complete replacement"
  - Fully regenerates from noise
  - Use rarely: When original is completely unusable
  - Risk: May not match surrounding image

**Interaction with steps**: Higher strength needs more steps (20-30) for quality. Lower strength can use fewer steps (15-20).

---

### steps
**What it does**: Number of denoising steps during sampling. More steps = higher quality but slower processing.

**Range**: 1 to 100 (step 1)
**Default**: 20

**Recommendations by sampler**:
- **Euler**: 15-25 steps (default sampler)
  - 15: Fast preview, acceptable quality
  - 20: **Recommended balance**
  - 25-30: Diminishing returns, marginal quality gain

- **DPM_2**: 10-20 steps (more efficient)
  - Generally needs fewer steps than Euler
  - 15-20 is usually sufficient

- **Euler Ancestral**: 20-30 steps
  - More stochastic, benefits from extra steps
  - Can produce more varied results

**Performance impact**:
- 10 steps: ~8 seconds (rough/fast)
- 20 steps: ~15 seconds (balanced)
- 30 steps: ~22 seconds (quality)
- 50 steps: ~37 seconds (overkill for most uses)

**Recommendation**: Start at 20, only increase if you see quality issues.

---

### cfg_scale
**What it does**: Classifier-Free Guidance scale - controls how strongly the model follows your prompt versus generating naturally.

**Range**: 1.0 to 30.0 (step 0.5)
**Default**: 7.0

**⚠️ IMPORTANT**: For inpainting, lower CFG is often better than for regular generation!

**Recommendations by use case**:
- **3.0-5.0**: "Natural blending"
  - Model focuses on matching surrounding image
  - Good for: Photorealistic images, subtle fixes
  - Less "prompt-driven", more "context-driven"
  - **Recommended for faces in photos**

- **5.0-7.0**: "Balanced adherence"
  - Good mix of prompt following and natural blending
  - Good for: General use, artistic images
  - Works well with detailed positive prompts

- **7.0-10.0**: "Strong prompt following"
  - Model strongly follows your prompt
  - Good for: Stylized changes, specific features
  - Risk: May clash with surrounding style

- **10.0-15.0**: "Very strong guidance"
  - Heavy prompt influence
  - Use when: You need specific features at any cost
  - Risk: Artifacts, over-saturation, clashing styles

- **>15.0**: "Extreme" (rarely needed)
  - Can cause artifacts, over-sharpening
  - Only use if absolutely necessary

**Modern recommendation**: The old "7.0 for everything" advice is outdated. For **inpainting specifically**, 3.0-6.0 often produces more natural results.

**Pro tip**: If enhanced areas look "different" from the rest of the image, try lowering CFG to 4.0-5.0.

---

### seed
**What it does**: Random seed for reproducible results. Same seed + same settings = same output.

**Range**: -1 (random) or any positive integer
**Default**: -1

**Recommendations**:
- ✅ **-1 (random)**: For exploration, trying different variations
- ✅ **Fixed value**: When you found a good result and want to tweak other parameters
- ✅ **Batch processing**: Use same seed for consistency across multiple images

**Workflow tip**:
1. Start with seed=-1, run several times
2. When you get a good result, copy the seed from detection_info
3. Lock that seed, adjust other parameters
4. If result gets worse, try a new seed

---

### sampler_name
**What it does**: The mathematical algorithm used for denoising during sampling.

**Options**: `euler`, `euler_ancestral`, `heun`, `dpm_2`, `dpm_2_ancestral`
**Default**: `euler`

**Recommendations**:
- ✅ **euler**: Fast, deterministic, reliable (RECOMMENDED)
  - Use for: Most cases, reproducible results
  - Pros: Fast, consistent, predictable
  - Cons: Less "creative" than ancestral samplers

- ✅ **dpm_2**: Slightly slower, often higher quality
  - Use for: When you want best quality
  - Pros: Often better detail preservation
  - Needs fewer steps (15-20 vs 20-25)

- ⚠️ **euler_ancestral**: Stochastic (random element)
  - Use for: More variation, creative results
  - Pros: Can produce more "interesting" results
  - Cons: Less predictable, harder to control

- ℹ️ **heun**: High quality but slower (2x steps)
  - Each step = 2 evaluations
  - Use rarely: When quality is critical and speed doesn't matter

**Most users should stick with `euler` (default) or try `dpm_2` for quality.**

---

### scheduler
**What it does**: Controls how noise is scheduled during denoising - how aggressively noise is removed at each step.

**Options**: `normal`, `karras`, `exponential`, `sgm_uniform`
**Default**: `normal`

**Recommendations**:
- ✅ **normal**: Standard linear schedule (RECOMMENDED)
  - Works well for most cases
  - Predictable behavior

- ✅ **karras**: Popular for quality
  - Often produces slightly better results
  - Good for: Final renders, when quality matters
  - Slightly slower than normal

- ℹ️ **exponential**: Different noise distribution
  - More aggressive early denoising
  - Try if normal/karras aren't working

- ℹ️ **sgm_uniform**: Specialized schedule
  - Use rarely: Specific model requirements

**Most users should use `normal` (default) or `karras` for slightly better quality.**

---

## Auto-Fix Toggles

### auto_face_fix
**What it does**: When True, automatically processes detected faces with inpainting. When False, detects faces but doesn't process them.

**Default**: True

**Use cases for False**:
- You only want the detection masks, not the inpainting
- You want to detect faces but only process hands
- Debugging: Check what's being detected without waiting for inpainting

### auto_hand_fix
**What it does**: When True, automatically processes detected hands with inpainting. When False, detects hands but doesn't process them.

**Default**: True

**Use cases for False**:
- You only want the detection masks, not the inpainting
- You want to detect hands but only process faces
- Debugging: Check detection without inpainting

**Note**: Even with auto_fix disabled, masks are still generated and output.

---

## Recommended Combinations

### Fast Preview / Testing
```python
{
    "target_parts": "face",
    "model_quality": "fast",
    "confidence_threshold": 0.4,
    "mask_padding": 32,
    "mask_blur": 8,
    "inpaint_strength": 0.75,
    "steps": 15,
    "cfg_scale": 5.0,
    "seed": -1,
    "sampler_name": "euler",
    "scheduler": "normal"
}
```
**Use for**: Quick iterations, testing prompts, finding good settings

---

### Photorealistic Face Enhancement
```python
{
    "target_parts": "face",
    "model_quality": "quality",
    "confidence_threshold": 0.5,
    "mask_padding": 40,
    "mask_blur": 12,
    "inpaint_strength": 0.7,
    "steps": 20,
    "cfg_scale": 4.0,  # Lower CFG for natural blending!
    "seed": -1,
    "sampler_name": "dpm_2",
    "scheduler": "karras"
}
```
**Use for**: Photo editing, realistic portraits, natural results
**Key**: Lower CFG (4.0) makes faces blend naturally

---

### Artistic/Stylized Images
```python
{
    "target_parts": "face,hand",
    "model_quality": "balanced",
    "confidence_threshold": 0.5,
    "mask_padding": 32,
    "mask_blur": 10,
    "inpaint_strength": 0.8,
    "steps": 25,
    "cfg_scale": 7.0,  # Higher CFG for stylistic control
    "seed": -1,
    "sampler_name": "euler",
    "scheduler": "normal"
}
```
**Use for**: Anime, illustrations, artistic styles
**Key**: Higher CFG maintains artistic style from prompt

---

### High-Resolution Final Render
```python
{
    "target_parts": "face,hand",
    "model_quality": "quality",
    "confidence_threshold": 0.5,
    "mask_padding": 48,
    "mask_blur": 15,
    "inpaint_strength": 0.75,
    "steps": 30,
    "cfg_scale": 5.0,
    "seed": 12345,  # Fixed seed for consistency
    "sampler_name": "dpm_2",
    "scheduler": "karras"
}
```
**Use for**: Final output, print quality, professional work
**Key**: Quality models, higher steps, fixed seed for reproducibility

---

### Hand Correction Focus
```python
{
    "target_parts": "hand",
    "model_quality": "quality",
    "confidence_threshold": 0.4,  # Lower to catch difficult hands
    "mask_padding": 64,  # Larger for hand context
    "mask_blur": 12,
    "inpaint_strength": 0.85,  # Higher to fix deformities
    "steps": 25,
    "cfg_scale": 6.0,
    "seed": -1,
    "sampler_name": "euler",
    "scheduler": "normal"
}
```
**Use for**: Fixing malformed hands, finger corrections
**Key**: Lower confidence to catch difficult hands, higher strength to fix deformities

---

## Parameter Interactions

### CFG Scale ↔ Steps
- **Higher CFG needs more steps** to avoid artifacts
- CFG 10+ → Use 25-30 steps minimum
- CFG 3-6 → Can use fewer steps (15-20)

### Inpaint Strength ↔ Steps
- **Higher strength needs more steps** for quality
- Strength 0.9+ → Use 25-30 steps
- Strength 0.6 → Can use 15-20 steps

### Mask Blur ↔ Image Resolution
- **Automatically handled!** Blur scales with resolution
- Don't increase blur manually for large images
- The 8-15 range works across all resolutions

### Model Quality ↔ Confidence Threshold
- **Quality models** → Can use higher threshold (0.5-0.6)
- **Fast models** → May need lower threshold (0.4-0.5) for difficult detections

---

## Troubleshooting Parameter Issues

### "Enhancement looks artificial/different from rest of image"
**Fix**: Lower CFG scale to 3.0-5.0
- High CFG makes inpainted areas too "prompt-driven"
- Lower CFG helps blend with surrounding image

### "Visible box edges around enhanced areas"
**Fix**: Increase mask_blur to 12-20
- If still visible on very large images, already auto-scaled
- Check that inpaint_strength isn't too high (try 0.7)

### "Not detecting faces/hands"
**Fix sequence**:
1. Lower confidence_threshold to 0.3
2. Try model_quality="quality"
3. Check detection_info output to see actual confidence scores
4. Verify target style is compatible (realistic photos work best)

### "Changes too subtle / no visible improvement"
**Fix**: Increase inpaint_strength to 0.8-0.9
- Make sure positive prompt is descriptive
- Try higher CFG (6.0-8.0) for more dramatic changes

### "Processing too slow"
**Fix combination**:
- model_quality="fast"
- steps=15
- target_parts="face" (not "face,hand")
- sampler_name="euler"

### "Results inconsistent / keep changing"
**Fix**: Use fixed seed
1. Run once with seed=-1
2. Find good result in detection_info
3. Copy that seed value
4. Use that seed for consistency

---

## Advanced Tips

1. **Prompt Quality Matters**: Your positive/negative prompts affect results more than most parameters. Be specific!

2. **Start Conservative**: Begin with default values, only adjust if there's a specific issue.

3. **CFG is Not "Quality"**: Higher CFG ≠ better quality. For inpainting, 3-6 is often ideal.

4. **Steps Have Diminishing Returns**: Going from 20→30 steps adds ~30% time for ~5% quality gain.

5. **Batch Test Parameters**: Use same seed, vary one parameter at a time to see its effect.

6. **Resolution Aware**: Large images (>2K) benefit from quality models and may need higher inpaint_strength.

7. **Style Matching**: If inpainted areas don't match image style, lower CFG and/or strength first before tweaking other parameters.

---

## Quick Start Checklist

Starting with a new image? Follow this sequence:

1. ✅ Run with defaults first
2. ✅ Check detection_info - are parts being detected?
   - If no: Lower confidence_threshold
3. ✅ Look at detection_masks - are areas reasonable?
   - If too small: Increase mask_padding
4. ✅ Look at result - is quality acceptable?
   - If visible edges: Already auto-handled (check mask_blur if needed)
   - If artificial looking: Lower CFG to 4-5
   - If too subtle: Increase inpaint_strength
5. ✅ Adjust steps only if quality issues persist
6. ✅ Lock seed when you find a good result

**Don't overcomplicate it!** The defaults work well for most images.
