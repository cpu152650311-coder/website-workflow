#!/usr/bin/env python3
"""
Generate multiple product images from reference photos using GPT Image 2 image-to-image.

Two modes:
  1. Quick mode: --reference + --angles/--scenes/--lighting presets
  2. Config mode: --config product-shots.json

Examples:
  # Quick: generate 2 angles x 2 scenes = 4 images from one reference photo
  python gen-product-shots.py --reference ./product.webp \
      --angles front,45deg --scenes studio,office --out ./shots

  # Full config mode
  python gen-product-shots.py --config product-shots.json --out ./shots

Presets:
  Angles: front, 45deg, side, back, topdown, macro
  Scenes: studio, office, hotel, retail, industrial, outdoor
  Lighting: daylight, softbox, rim, ambient
"""
import requests, base64, json, argparse, sys, time, io, os
from pathlib import Path
from urllib.parse import urlparse

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

EDITS_URL = "https://api.inferera.com/v1/images/edits"

# ── Preset templates ─────────────────────────────────────────────────
ANGLE_TEMPLATES = {
    "front":   "Same product, front view, white studio background, professional product photography",
    "45deg":   "Same product, 45-degree three-quarter angle view, clean studio lighting",
    "side":    "Same product, clean side profile view, studio lighting",
    "back":    "Same product, rear view showing all connections and details, studio lighting",
    "topdown": "Same product, top-down overhead flat lay view, white surface",
    "macro":   "Close-up macro shot of product details and textures, shallow depth of field",
}

SCENE_TEMPLATES = {
    "studio":     "Same product, white seamless background, professional product photography, Apple aesthetic, clean minimal",
    "office":     "Same product, modern open-plan office setting, natural daylight through windows, professional atmosphere",
    "hotel":      "Same product, luxury hotel lobby, warm ambient lighting, marble floors, elegant interior design",
    "retail":     "Same product, modern retail store display, bright commercial lighting, attractive presentation",
    "industrial": "Same product, clean factory or warehouse setting, professional industrial photography, organized workspace",
    "outdoor":    "Same product, outdoor urban plaza, natural daylight, modern architecture background, blue sky",
}

LIGHTING_TEMPLATES = {
    "daylight": "natural daylight illumination, soft shadows, bright and airy feel",
    "softbox":  "professional studio softbox lighting, even diffused illumination, no harsh shadows, clean look",
    "rim":      "dramatic rim edge lighting, dark background, product edges highlighted with light, cinematic",
    "ambient":  "warm ambient interior lighting, cozy atmosphere, golden tones, inviting mood",
}


# ── Core functions ───────────────────────────────────────────────────
def load_reference_image(path, base_url=None):
    """Load reference image from URL or local path. Returns bytes."""
    ref_str = str(path).strip()
    if not ref_str:
        raise ValueError("Reference path is empty")

    if urlparse(ref_str).scheme in ("http", "https"):
        print(f"  Downloading: {ref_str[:120]}...")
        resp = requests.get(ref_str, timeout=30)
        resp.raise_for_status()
        return resp.content

    ref_path = Path(ref_str)
    if ref_path.is_absolute() and ref_path.exists():
        return ref_path.read_bytes()

    if base_url:
        full_url = base_url.rstrip("/") + "/" + ref_str.lstrip("/")
        if urlparse(full_url).scheme in ("http", "https"):
            resp = requests.get(full_url, timeout=30)
            resp.raise_for_status()
            return resp.content

    if ref_path.exists():
        return ref_path.read_bytes()

    raise FileNotFoundError(f"Cannot load reference: {path}")


def generate_one_shot(prompt, reference_bytes, api_key):
    """Generate one image via image-to-image. Returns raw bytes."""
    ref_b64 = base64.b64encode(reference_bytes).decode("utf-8")
    data_uri = f"data:image/webp;base64,{ref_b64}"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "images": [{"image_url": data_uri}],
        "size": "1024x1024",
    }
    resp = requests.post(EDITS_URL, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()["data"][0]
    if "url" in data:
        return requests.get(data["url"], timeout=30).content
    elif "b64_json" in data:
        return base64.b64decode(data["b64_json"])
    raise ValueError(f"No image in response: {list(data.keys())}")


def save_image(raw_bytes, output_path):
    """Save raw bytes as WebP image."""
    output_path = Path(output_path)
    if HAS_PIL:
        try:
            img = Image.open(io.BytesIO(raw_bytes))
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
            img = img.convert("RGB")
            img.save(output_path, "WEBP", quality=85)
            return
        except Exception:
            pass
    output_path.write_bytes(raw_bytes)


def load_api_key(cli_key=None):
    if cli_key:
        return cli_key
    if os.environ.get("AIHUBMIX_API_KEY"):
        return os.environ["AIHUBMIX_API_KEY"]
    for search_dir in [Path("."), Path(__file__).parent.parent]:
        env_file = search_dir / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("AIHUBMIX_API_KEY="):
                        return line.split("=", 1)[1].strip()
    return None


# ── Modes ────────────────────────────────────────────────────────────
def run_quick_mode(reference_path, angles, scenes, lightings, api_key, out_dir, base_url):
    """Quick mode: generate combinations of angle + scene + lighting from presets."""
    ref_bytes = load_reference_image(reference_path, base_url)
    print(f"Reference loaded: {len(ref_bytes):,} bytes")

    # Build shot list from preset combinations
    shots = []
    for angle_name in (angles or ["front"]):
        angle_prompt = ANGLE_TEMPLATES.get(angle_name, angle_name)
        for scene_name in (scenes or ["studio"]):
            scene_prompt = SCENE_TEMPLATES.get(scene_name, scene_name)
            for light_name in (lightings or ["softbox"]):
                light_prompt = LIGHTING_TEMPLATES.get(light_name, light_name)
                full_prompt = f"{angle_prompt}, {scene_prompt}, {light_prompt}"
                shot_id = f"{angle_name}-{scene_name}-{light_name}"
                shots.append({"id": shot_id, "prompt": full_prompt})

    print(f"Shots to generate: {len(shots)} "
          f"({len(angles or ['front'])} angles x {len(scenes or ['studio'])} scenes x {len(lightings or ['softbox'])} lightings)")
    print("=" * 60)

    return run_shots(shots, ref_bytes, api_key, out_dir)


def run_config_mode(config_path, api_key, out_dir):
    """Config mode: read product-shots.json for full control."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    ref_images = config.get("reference_images", [])
    shots = config.get("shots", [])
    base_url = config.get("meta", {}).get("baseUrl")

    if not ref_images:
        print("ERROR: No reference_images in config")
        sys.exit(1)
    if not shots:
        print("ERROR: No shots in config")
        sys.exit(1)

    # Use first reference image as primary
    primary_ref = ref_images[0]
    ref_path = primary_ref.get("path") or primary_ref.get("url")
    if not ref_path:
        print("ERROR: reference_images[0] must have 'path' or 'url'")
        sys.exit(1)

    ref_bytes = load_reference_image(ref_path, base_url)
    print(f"Reference loaded: {len(ref_bytes):,} bytes ({primary_ref.get('label', 'unnamed')})")
    print(f"Shots to generate: {len(shots)}")
    print("=" * 60)

    return run_shots(shots, ref_bytes, api_key, out_dir)


def run_shots(shots, ref_bytes, api_key, out_dir):
    """Execute a list of shots against one reference image."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = []
    manifest = {}

    for i, shot in enumerate(shots):
        shot_id = shot["id"]
        prompt = shot["prompt"]
        output_path = out_dir / f"{shot_id}.webp"

        if output_path.exists():
            print(f"[{i+1}/{len(shots)}] SKIP {shot_id} (exists)")
            manifest[shot_id] = {"file": f"{shot_id}.webp", "prompt": prompt}
            success += 1
            continue

        print(f"[{i+1}/{len(shots)}] {shot_id}")
        print(f"  Prompt: {prompt[:150]}...")

        try:
            raw_bytes = generate_one_shot(prompt, ref_bytes, api_key)
            save_image(raw_bytes, output_path)
            fsize = output_path.stat().st_size
            manifest[shot_id] = {"file": f"{shot_id}.webp", "prompt": prompt, "size_bytes": fsize}
            print(f"  => OK ({fsize:,} bytes)")
            success += 1
        except Exception as e:
            print(f"  => FAIL: {e}")
            failed.append({"id": shot_id, "error": str(e)})
            time.sleep(2)

        if i < len(shots) - 1:
            time.sleep(1)

    # Save manifest
    manifest_path = out_dir / "product-shots-manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"Done. Success: {success}  Failed: {len(failed)}")
    print(f"Manifest: {manifest_path}")
    if failed:
        fail_path = out_dir / "failed-shots.json"
        with open(fail_path, "w", encoding="utf-8") as f:
            json.dump(failed, f, indent=2, ensure_ascii=False)
        print(f"Failed: {fail_path}")
        sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate multiple product images from a reference photo using GPT Image 2"
    )
    # Config mode
    parser.add_argument("--config", help="Path to product-shots.json (full config mode)")

    # Quick mode
    parser.add_argument("--reference", help="Path or URL to reference product image")
    parser.add_argument("--angles", help="Comma-separated angle names: front,45deg,side,back,topdown,macro")
    parser.add_argument("--scenes", help="Comma-separated scene names: studio,office,hotel,retail,industrial,outdoor")
    parser.add_argument("--lighting", help="Comma-separated lighting names: daylight,softbox,rim,ambient")
    parser.add_argument("--base-url", help="Base URL for resolving relative reference paths")

    # Common
    parser.add_argument("--out", default="./product-shots", help="Output directory")
    parser.add_argument("--api-key", help="API key (or set AIHUBMIX_API_KEY env)")

    # List presets
    parser.add_argument("--list-presets", action="store_true", help="Show available angle/scene/lighting presets")

    args = parser.parse_args()

    if args.list_presets:
        print("Angle presets:", ", ".join(ANGLE_TEMPLATES.keys()))
        print("Scene presets:", ", ".join(SCENE_TEMPLATES.keys()))
        print("Lighting presets:", ", ".join(LIGHTING_TEMPLATES.keys()))
        return

    api_key = load_api_key(args.api_key)
    if not api_key:
        print("ERROR: No API key. Set AIHUBMIX_API_KEY or use --api-key")
        sys.exit(1)

    if args.config:
        run_config_mode(args.config, api_key, args.out)
    elif args.reference:
        angles_list = [a.strip() for a in args.angles.split(",")] if args.angles else []
        scenes_list = [s.strip() for s in args.scenes.split(",")] if args.scenes else []
        light_list = [l.strip() for l in args.lighting.split(",")] if args.lighting else []
        run_quick_mode(args.reference, angles_list, scenes_list, light_list,
                       api_key, args.out, args.base_url)
    else:
        print("ERROR: Specify --config for config mode or --reference for quick mode.")
        print("Use --list-presets to see available angle/scene/lighting names.")
        sys.exit(1)


if __name__ == "__main__":
    main()
