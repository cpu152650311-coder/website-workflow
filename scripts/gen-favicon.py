#!/usr/bin/env python3
"""
Generate favicon assets from a logo image (via GPT Image 2 text-to-image).
Outputs: favicon.ico, apple-touch-icon.png, logo-512.png, logo-192.png

Usage:
  python gen-favicon.py --prompt "minimalist abstract logo for a LED lighting brand, no text" --out ./generated
  python gen-favicon.py --source ./generated/logo.webp --out ./generated
"""
import requests, base64, argparse, sys, io, os
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("ERROR: Pillow required. pip install Pillow")
    sys.exit(1)

GENERATIONS_URL = "https://api.inferera.com/v1/images/generations"


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


def generate_logo(prompt, api_key):
    """Generate a logo image via GPT Image 2 text-to-image."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "low",
    }
    resp = requests.post(GENERATIONS_URL, headers=headers, json=payload, timeout=90)
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()["data"][0]
    if "url" in data:
        return requests.get(data["url"], timeout=30).content
    elif "b64_json" in data:
        return base64.b64decode(data["b64_json"])
    raise ValueError(f"No image in response: {list(data.keys())}")


def generate_favicons(source_bytes, out_dir):
    """Generate all favicon sizes from a source image."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(io.BytesIO(source_bytes))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    assets = {
        "favicon.ico": [(16, 16), (32, 32)],
        "apple-touch-icon.png": (180, 180),
        "icon-192.png": (192, 192),
        "icon-512.png": (512, 512),
    }

    results = {}
    for filename, sizes in assets.items():
        if filename == "favicon.ico":
            ico_path = out_dir / filename
            img_16 = img.resize((16, 16), Image.LANCZOS)
            img_32 = img.resize((32, 32), Image.LANCZOS)
            img_16.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32)])
            results[filename] = ico_path.stat().st_size
        elif isinstance(sizes, tuple):
            out_path = out_dir / filename
            resized = img.resize(sizes, Image.LANCZOS)
            resized.save(out_path, "PNG")
            results[filename] = out_path.stat().st_size

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate favicon assets from a logo image")
    parser.add_argument("--prompt", help="Text prompt to generate a logo via GPT Image 2")
    parser.add_argument("--source", help="Path to existing logo image (skip generation)")
    parser.add_argument("--out", default="./generated", help="Output directory")
    parser.add_argument("--api-key", help="API key (or set AIHUBMIX_API_KEY env)")
    args = parser.parse_args()

    if not args.prompt and not args.source:
        print("ERROR: Specify --prompt (to generate a logo) or --source (to use existing image)")
        sys.exit(1)

    api_key = load_api_key(args.api_key)
    if not api_key:
        print("ERROR: No API key. Set AIHUBMIX_API_KEY or use --api-key")
        sys.exit(1)

    if args.source:
        source_path = Path(args.source)
        if not source_path.exists():
            print(f"ERROR: {args.source} not found")
            sys.exit(1)
        source_bytes = source_path.read_bytes()
        print(f"Using existing logo: {args.source} ({len(source_bytes):,} bytes)")
    else:
        print(f"Generating logo: {args.prompt[:120]}...")
        source_bytes = generate_logo(args.prompt, api_key)
        # Save source logo
        logo_path = Path(args.out) / "logo.webp"
        logo_path.parent.mkdir(parents=True, exist_ok=True)
        logo_path.write_bytes(source_bytes)
        print(f"Logo saved: {logo_path} ({len(source_bytes):,} bytes)")

    print("Generating favicon assets...")
    results = generate_favicons(source_bytes, args.out)
    for name, size in results.items():
        print(f"  {name}: {size:,} bytes")

    # HTML snippet
    print("\n<!-- Add to <head> -->")
    print('<link rel="icon" type="image/x-icon" href="/generated/favicon.ico">')
    print('<link rel="apple-touch-icon" sizes="180x180" href="/generated/apple-touch-icon.png">')
    print('<link rel="icon" type="image/png" sizes="192x192" href="/generated/icon-192.png">')
    print('<link rel="icon" type="image/png" sizes="512x512" href="/generated/icon-512.png">')
    print("Done.")


if __name__ == "__main__":
    main()
