#!/usr/bin/env python3
"""Inject production API base into widget manifest.

Reads widgets/shared/manifest.json and replaces the ${API_BASE} token with
PRODUCTION_API_BASE environment variable. The {integration_key} placeholder
is preserved so the runtime can substitute the user's key.
"""

import json
import os
from pathlib import Path

API_BASE = os.environ.get("PRODUCTION_API_BASE")
if not API_BASE:
    raise SystemExit("PRODUCTION_API_BASE environment variable is required")

manifest_path = Path(__file__).parent / "shared" / "manifest.json"
manifest = json.loads(manifest_path.read_text())

# Replace placeholder token
placeholder = manifest["salesbot_designer"]["handler_name"]["settings"]["text"]["default_value"]
manifest["salesbot_designer"]["handler_name"]["settings"]["text"]["default_value"] = (
    placeholder.replace("${API_BASE}", API_BASE.rstrip("/"))
)

manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Updated manifest default_value to use {API_BASE.rstrip('/')}")
