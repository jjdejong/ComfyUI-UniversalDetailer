#!/usr/bin/env python3
"""
Model Setup Script for ComfyUI Universal Detailer

This script downloads all required YOLOv models for face and hand detection.
Run this script to manually download models if automatic download fails.

Usage:
    python setup_models.py [--model MODEL_NAME]

Examples:
    python setup_models.py                    # Download all models
    python setup_models.py --model yolov8n-face  # Download specific model
"""

import os
import sys
import argparse
import requests
from pathlib import Path

# Try to import tqdm, use fallback if not available
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: tqdm not installed, progress bars will be simpler")
    print("Install with: pip install tqdm")
    print()

# Model configurations
# Models are sourced from Hugging Face (Bingsu/adetailer) for reliability
MODELS = {
    "yolov8n-face": {
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt",
        "filename": "yolov8n-face.pt",
        "size_mb": 6.2,
        "description": "YOLOv8 Nano Face Detection (Fast, recommended)"
    },
    "yolov8s-face": {
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8s.pt",
        "filename": "yolov8s-face.pt",
        "size_mb": 22.5,
        "description": "YOLOv8 Small Face Detection (High accuracy)"
    },
    "yolov8m-face": {
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt",
        "filename": "yolov8m-face.pt",
        "size_mb": 52.0,
        "description": "YOLOv8 Medium Face Detection (Highest accuracy)"
    },
    "hand_yolov8n": {
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8n.pt",
        "filename": "hand_yolov8n.pt",
        "size_mb": 6.2,
        "description": "YOLOv8 Nano Hand Detection (Fast)"
    },
    "hand_yolov8s": {
        "url": "https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8s.pt",
        "filename": "hand_yolov8s.pt",
        "size_mb": 21.5,
        "description": "YOLOv8 Small Hand Detection (High accuracy)"
    },
    "yolov8n": {
        "url": "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt",
        "filename": "yolov8n.pt",
        "size_mb": 6.2,
        "description": "YOLOv8 Nano General Object Detection"
    }
}

def download_model(model_name: str, models_dir: Path, force: bool = False) -> bool:
    """
    Download a specific model.

    Args:
        model_name: Name of the model to download
        models_dir: Directory to save the model
        force: Force re-download even if file exists

    Returns:
        True if successful, False otherwise
    """
    if model_name not in MODELS:
        print(f"❌ Unknown model: {model_name}")
        print(f"Available models: {', '.join(MODELS.keys())}")
        return False

    model_info = MODELS[model_name]
    url = model_info["url"]
    filename = model_info["filename"]
    model_path = models_dir / filename

    # Check if already exists
    if model_path.exists() and not force:
        file_size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✓ {model_name} already exists ({file_size_mb:.1f} MB)")
        return True

    print(f"\n📥 Downloading {model_name}")
    print(f"   Description: {model_info['description']}")
    print(f"   Size: ~{model_info['size_mb']} MB")
    print(f"   URL: {url}")
    print(f"   Destination: {model_path}")

    try:
        # Set headers for Hugging Face compatibility
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Download with progress bar
        response = requests.get(url, stream=True, timeout=300, headers=headers, allow_redirects=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(model_path, 'wb') as f:
            if HAS_TQDM and total_size > 0:
                # Use tqdm progress bar if available
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=filename,
                    ncols=80
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                # Simple fallback progress
                last_percent = -1
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = int(downloaded * 100 / total_size)
                            if percent != last_percent and percent % 10 == 0:
                                print(f"   Progress: {percent}% ({downloaded}/{total_size} bytes)")
                                last_percent = percent

        # Verify download
        if model_path.exists() and model_path.stat().st_size > 0:
            downloaded_size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"✓ Successfully downloaded {model_name} ({downloaded_size_mb:.1f} MB)")
            return True
        else:
            print(f"❌ Download verification failed for {model_name}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed for {model_name}: {e}")
        if model_path.exists():
            model_path.unlink()  # Remove partial download
        return False
    except Exception as e:
        print(f"❌ Unexpected error downloading {model_name}: {e}")
        if model_path.exists():
            model_path.unlink()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YOLOv models for ComfyUI Universal Detailer"
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=list(MODELS.keys()) + ["all"],
        default="all",
        help="Model to download: yolov8n-face (fast), yolov8s-face (balanced), yolov8m-face (accurate), yolov8n (general), or all (default: all)"
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default="models",
        help="Directory to save models (default: models)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if file exists"
    )

    args = parser.parse_args()

    # Determine script location and models directory
    script_dir = Path(__file__).parent
    models_dir = script_dir / args.models_dir
    models_dir.mkdir(exist_ok=True, parents=True)

    print("=" * 70)
    print("ComfyUI Universal Detailer - Model Setup")
    print("=" * 70)
    print(f"Models directory: {models_dir.absolute()}")
    print()

    # Download models
    if args.model == "all":
        print(f"Downloading all {len(MODELS)} models...")
        print()

        success_count = 0
        for model_name in MODELS.keys():
            if download_model(model_name, models_dir, args.force):
                success_count += 1

        print()
        print("=" * 70)
        print(f"Download Summary: {success_count}/{len(MODELS)} models successful")
        print("=" * 70)

        if success_count == len(MODELS):
            print("✓ All models downloaded successfully!")
            print()
            print("Next steps:")
            print("1. Restart ComfyUI if it's running")
            print("2. Add the Universal Detailer node to your workflow")
            print("3. Select a detection model from the dropdown")
            return 0
        else:
            print("⚠ Some models failed to download. Check errors above.")
            return 1
    else:
        if download_model(args.model, models_dir, args.force):
            print()
            print("=" * 70)
            print(f"✓ {args.model} downloaded successfully!")
            print("=" * 70)
            return 0
        else:
            return 1


if __name__ == "__main__":
    sys.exit(main())
