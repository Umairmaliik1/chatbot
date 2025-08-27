# Widget Build Instructions

The Salesbot widget manifest uses a configurable API base URL.

## Generating `manifest.json`

Set the `PRODUCTION_API_BASE` environment variable and run the build script:

```bash
PRODUCTION_API_BASE=https://api.example.com python widgets/build_manifest.py
```

This replaces the `${API_BASE}` token in `shared/manifest.json` with your
production API domain.

## Integration Key Placeholder

The webhook URL in the manifest contains a `{integration_key}` token:

```
${API_BASE}/api/kommo/kommo/widget-request/{integration_key}
```

Keep this placeholder in the final URL. At runtime it must be replaced with
an actual integration key so the request is routed to the correct account.
