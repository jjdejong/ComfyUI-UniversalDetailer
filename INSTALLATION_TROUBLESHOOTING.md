# Installation Troubleshooting Guide

**Common installation issues and their solutions**

---

## Quick Fix for Common Errors

### Error 1: "This action is not allowed with this security level configuration"
**Where:** ComfyUI Manager when trying to enter git URL

**Solution:**
- ✅ **Use the search box** in ComfyUI Manager instead of entering URLs
- ✅ Search for "controlnet aux" to find MeshGraphormer
- ✅ Or use Manual Download method (see Solution 2 below)

### Error 2: Git Clone Asks for Username/Password
**Where:** Terminal/command line when running `git clone`

**Solution:**
- ✅ **Use ComfyUI Manager search** (easiest - see Solution 1)
- ✅ **Download ZIP manually** from GitHub (see Solution 2)
- ✅ Skip git entirely (see Solutions 1 & 2)

---

## Problem 1: ComfyUI Manager Security Restriction

When trying to install custom nodes by entering a git URL in ComfyUI Manager, you see:
```
"This action is not allowed with this security level configuration."
```

**This is a security feature** that restricts manual URL entry. You can only install nodes from the Manager's official trusted list.

**Solution:** Jump to [Solution 1](#solution-1-use-comfyui-manager-easiest---recommended) and use the **search function** instead of entering URLs.

---

## Problem 2: Git Clone Requests Authentication

When running commands like:
```bash
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

You may be prompted for username and password. This can happen due to:
- Git configuration on your system
- Corporate/network proxies
- Git credential helpers

---

## Solution 1: Use ComfyUI Manager (Easiest - Recommended)

**This is the easiest method - no command line needed!**

### Step 1: Install ComfyUI Manager (if not already installed)

1. Navigate to `ComfyUI/custom_nodes/`
2. Download ComfyUI Manager:
   - Visit: https://github.com/ltdrdata/ComfyUI-Manager
   - Click "Code" → "Download ZIP"
   - Extract to `ComfyUI/custom_nodes/ComfyUI-Manager/`
3. Restart ComfyUI

### Step 2: Install Nodes Through Manager

**IMPORTANT: Use the search function, don't enter git URLs directly!**

1. **In ComfyUI web interface**, click the **Manager** button
2. Click **"Install Custom Nodes"**
3. **Use the search box** to find nodes:
   - Search "**ControlNet Auxiliary**" or "**controlnet aux**" → Find "ComfyUI's ControlNet Auxiliary Preprocessors" → Click "Install"
   - Search "**BMAB**" → Click "Install"
   - Search "**SAM2**" → Click "Install"
   - etc.
4. Restart ComfyUI when prompted

**⚠️ Security Restriction Warning**

If you try to **manually enter a git URL** in ComfyUI Manager, you may see:
```
"This action is not allowed with this security level configuration."
```

**Solution:**
- ✅ **Use the search function** instead of entering URLs
- ✅ The node must be in Manager's official list to install this way
- ✅ If not found in search, use **Manual Download** (Solution 2 below)

**How to search effectively:**
- For MeshGraphormer: Search "**controlnet aux**" or "**auxiliary**"
- For Impact Pack nodes: Search "**impact**"
- Use partial names if full name doesn't work

**Advantages:**
- ✅ No git commands needed
- ✅ No authentication issues
- ✅ Automatic dependency installation
- ✅ Easy updates through GUI
- ✅ Only nodes from trusted sources

---

## Solution 2: Manual Download from GitHub (No Git Required)

For any custom node that's giving git authentication errors:

### Example: Installing ControlNet Auxiliary Preprocessors (includes MeshGraphormer)

1. **Open browser** and go to: https://github.com/Fannovel16/comfyui_controlnet_aux

2. **Download as ZIP**:
   - Click the green "Code" button
   - Click "Download ZIP"
   - Save to your Downloads folder

3. **Extract ZIP**:
   - Extract the downloaded ZIP file
   - You'll get a folder named `comfyui_controlnet_aux-main`

4. **Move to ComfyUI**:
   - Rename folder to remove `-main`: `comfyui_controlnet_aux`
   - Move the folder to: `ComfyUI/custom_nodes/comfyui_controlnet_aux/`

5. **Install dependencies**:
   ```bash
   cd ComfyUI/custom_nodes/comfyui_controlnet_aux/
   pip install -r requirements.txt
   ```

6. **Restart ComfyUI**

### Apply This Method to Any Custom Node

Replace the repository URL with any of these:
- **BMAB**: https://github.com/portu-sim/comfyui_bmab
- **SAM2**: https://github.com/neverbiasu/ComfyUI-SAM2
- **FluxFill**: https://github.com/kijai/ComfyUI-FluxFill
- **ControlNet Aux (MeshGraphormer)**: https://github.com/Fannovel16/comfyui_controlnet_aux

---

## Solution 3: Use Git Without Authentication

### Option A: Configure Git to Skip Authentication (for public repos)

```bash
# Configure git to use HTTPS without credentials for this session
git config --global credential.helper ""

# Then try the clone again
cd ComfyUI/custom_nodes/
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

### Option B: Use Git with Different Protocol

Some networks block HTTPS git but allow HTTP:

```bash
# Try with explicit HTTP (less secure but works on some networks)
git clone http://github.com/Fannovel16/comfyui_controlnet_aux.git
```

---

## Solution 4: Downloading Models Without wget

If `wget` commands also ask for authentication or don't work:

### For ControlNet Models

**Instead of:**
```bash
wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth
```

**Do this:**

1. **Open browser** and visit: https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main

2. **Find the file**: `control_v11f1p_sd15_depth.pth`

3. **Click the file name**, then click the **download icon** (↓)

4. **Save to**: `ComfyUI/models/controlnet/`

### For Hand Detection Models

**Instead of:**
```bash
wget https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8s.pt
```

**Do this:**

1. Visit: https://huggingface.co/Bingsu/adetailer/tree/main

2. Find and download: `hand_yolov8s.pt`

3. Save to: `ComfyUI/models/ultralytics/bbox/`

### For SAM Models

**Instead of:**
```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

**Do this:**

1. Open browser and visit: https://github.com/facebookresearch/segment-anything#model-checkpoints

2. Click the **ViT-H SAM model** download link

3. Save to: `ComfyUI/models/sams/`

---

## Quick Reference: Manual Installation Steps

For **any** custom node installation issue:

### Method 1: ComfyUI Manager (Recommended)
```
1. Open ComfyUI
2. Click "Manager" button
3. "Install Custom Nodes"
4. Search and click "Install"
5. Restart ComfyUI
```

### Method 2: Manual Download
```
1. Visit GitHub repository in browser
2. Click "Code" → "Download ZIP"
3. Extract ZIP file
4. Move to ComfyUI/custom_nodes/[node-name]/
5. Run: pip install -r requirements.txt
6. Restart ComfyUI
```

### Method 3: Download Models Manually
```
1. Visit model repository in browser
2. Find and download the model file
3. Move to appropriate ComfyUI/models/ subfolder
4. Verify file is in correct location
```

---

## Common Model Locations

Make sure downloaded files go to the correct folders:

| Model Type | Location |
|------------|----------|
| ControlNet models | `ComfyUI/models/controlnet/` |
| Hand YOLO models | `ComfyUI/models/ultralytics/bbox/` |
| Face YOLO models | `ComfyUI/models/ultralytics/bbox/` |
| SAM models | `ComfyUI/models/sams/` |
| Flux Fill models | `ComfyUI/models/unet/` |
| Checkpoints | `ComfyUI/models/checkpoints/` |
| VAE models | `ComfyUI/models/vae/` |

---

## Verification Steps

After installation, verify everything is in place:

### Check Custom Nodes
```bash
ls ComfyUI/custom_nodes/
```
Should see folders like:
- ComfyUI-Impact-Pack
- ComfyUI-MeshGraphormer
- ComfyUI-SAM2
- etc.

### Check Models
```bash
# Check hand detection model
ls ComfyUI/models/ultralytics/bbox/hand_yolov8s.pt

# Check ControlNet model
ls ComfyUI/models/controlnet/control_v11f1p_sd15_depth.pth

# Check SAM model
ls ComfyUI/models/sams/sam_vit_h_4b8939.pth
```

### Test in ComfyUI

1. **Start ComfyUI**
2. **Right-click on canvas** → "Add Node"
3. **Look for the nodes**:
   - Search "MeshGraphormer" (should appear if installed)
   - Search "BMAB" (should appear if installed)
   - etc.

If nodes don't appear, check the ComfyUI console/terminal for error messages.

---

## Still Having Issues?

### Check ComfyUI Console

When you start ComfyUI, the terminal/console shows:
- ✅ Successfully loaded custom nodes
- ❌ Errors loading nodes (missing dependencies, etc.)

**Look for lines like:**
```
[ComfyUI-MeshGraphormer] Loaded successfully
```
or errors like:
```
Cannot import module 'xyz' - install required packages
```

### Common Error: Missing Dependencies

If you see import errors after manual installation:

```bash
cd ComfyUI/custom_nodes/[problematic-node]/
pip install -r requirements.txt --upgrade
```

### ComfyUI Manager Shows "Import Failed"

1. Click on the failed node in Manager
2. Check the error message
3. Usually means missing Python packages
4. Install packages manually: `pip install [package-name]`

---

## Alternative: Use Pre-Configured ComfyUI

If installation is too complex, consider using a pre-configured ComfyUI distribution:

- **ComfyUI Portable** (Windows): https://github.com/comfyanonymous/ComfyUI/releases
- **Pinokio** (All platforms): https://pinokio.computer/ - One-click installer with many nodes pre-installed
- **Docker ComfyUI**: Pre-configured Docker containers with common nodes

These come with many custom nodes pre-installed, avoiding git clone issues entirely.

---

## Summary

**Recommended approach for beginners:**

1. ✅ **First try: ComfyUI Manager** (GUI-based, easiest)
2. ✅ **If that fails: Manual ZIP download** (no git needed)
3. ✅ **Download models through browser** (no wget needed)
4. ✅ **Verify files are in correct locations**
5. ✅ **Check console for errors on startup**

**You don't need git or command line expertise to use ComfyUI!** The Manager makes it beginner-friendly.

---

## Need More Help?

- **ComfyUI Discord**: https://discord.gg/comfyui
- **ComfyUI Reddit**: r/comfyui
- **GitHub Issues**: Check the custom node's GitHub page for installation help

Include in your help request:
- Your operating system (Windows/Mac/Linux)
- The exact error message
- What you've already tried
- ComfyUI console output (copy the error text)
