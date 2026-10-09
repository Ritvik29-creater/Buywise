#!/usr/bin/env python3
"""
setup.py — SmartShop Elite one-shot setup script.
Run this after cloning the repo to get everything ready.
"""

import os
import subprocess
import sys
from pathlib import Path


def run(cmd: str, check: bool = True):
    print(f"\n{'='*60}\n▶ {cmd}\n{'='*60}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0


def check_python_version():
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 10):
        print(f"❌ Python 3.10+ required. Found {major}.{minor}")
        sys.exit(1)
    print(f"✅ Python {major}.{minor} detected")


def check_env_file():
    env_path = Path(".env")
    if not env_path.exists():
        example = Path(".env.example")
        if example.exists():
            import shutil
            shutil.copy(example, env_path)
            print("📝 Created .env from .env.example — please add your GOOGLE_API_KEY!")
        else:
            print("⚠️  No .env file found. Create one with GOOGLE_API_KEY=...")
        return False
    # Check for required key
    content = env_path.read_text()
    if "GOOGLE_API_KEY" not in content or "AIzaSy..." in content:
        print("⚠️  Please set your GOOGLE_API_KEY in .env before running the app.")
        return False
    print("✅ .env file looks good")
    return True


def install_dependencies():
    print("\n📦 Installing dependencies...")
    return run(f"{sys.executable} -m pip install -r requirements.txt")


def download_dataset():
    dataset_dir = Path("./dataset")
    if dataset_dir.exists() and any(dataset_dir.iterdir()):
        print("✅ Dataset already present, skipping download.")
        return True
    print("\n📥 Downloading dataset...")
    return run(f"{sys.executable} download_dataset.py")


def build_vector_db():
    vector_db_dir = Path("./vector_db")
    if vector_db_dir.exists() and any(vector_db_dir.iterdir()):
        print("✅ Vector DB already present, skipping build.")
        return True
    print("\n🧠 Building vector database (this may take a few minutes)...")
    return run(f"{sys.executable} src/build_vector_db.py")


def run_tests():
    print("\n🧪 Running test suite...")
    ok = run("pytest tests/ -v --tb=short -q", check=False)
    if ok:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed — check output above.")
    return ok


def main():
    print("🛒 SmartShop Elite — Setup Script")
    print("=" * 60)

    check_python_version()

    steps = [
        ("Install dependencies", install_dependencies),
        ("Download dataset", download_dataset),
        ("Build vector DB", build_vector_db),
    ]

    for name, fn in steps:
        print(f"\n📌 Step: {name}")
        success = fn()
        if not success:
            print(f"❌ Failed at: {name}")
            sys.exit(1)

    env_ok = check_env_file()
    run_tests()

    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    if env_ok:
        print("\n🚀 Start the app with:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Before running:")
        print("   1. Edit .env and add your GOOGLE_API_KEY")
        print("   2. Then run: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
