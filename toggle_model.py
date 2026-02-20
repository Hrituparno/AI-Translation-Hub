"""
Toggle between NLLB (high quality) and MarianMT (lightweight) models.
"""

import sys

def toggle_model(use_nllb: bool):
    """Toggle the translation model in config.py"""
    
    config_path = "core/config.py"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if use_nllb:
        # Enable NLLB
        content = content.replace(
            "USE_NLLB_MODEL = False",
            "USE_NLLB_MODEL = True"
        )
        model_name = "NLLB-200 (High Quality, Google Translate-like)"
        memory = "~1.2 GB"
    else:
        # Enable MarianMT
        content = content.replace(
            "USE_NLLB_MODEL = True",
            "USE_NLLB_MODEL = False"
        )
        model_name = "MarianMT (Lightweight)"
        memory = "~300-500 MB"
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 60)
    print(f"Model Configuration Updated!")
    print("=" * 60)
    print(f"Active Model: {model_name}")
    print(f"Memory Usage: {memory}")
    print(f"\nRestart the API and UI servers for changes to take effect.")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode in ['nllb', 'high', 'quality']:
            toggle_model(True)
        elif mode in ['marian', 'light', 'lightweight']:
            toggle_model(False)
        else:
            print("Usage: python toggle_model.py [nllb|marian]")
            print("  nllb    - Use NLLB model (high quality, more memory)")
            print("  marian  - Use MarianMT model (lightweight, less memory)")
    else:
        print("Current configuration:")
        with open("core/config.py", 'r') as f:
            for line in f:
                if "USE_NLLB_MODEL" in line and not line.strip().startswith("#"):
                    print(f"  {line.strip()}")
                    break
        print("\nUsage: python toggle_model.py [nllb|marian]")
