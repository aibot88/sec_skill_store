---
name: flet-aca-deploy
description: Deploy a Flet web app to Azure Container Apps — covers all pitfalls: container startup, WebSocket transport, GHCR auth, ACA provisioning, revision forcing, and health diagnosis
author: POWR-DATA
version: 1.0.0
license: MIT
---

# Flet ACA Deploy

This skill covers everything specific to running a Flet web app on Azure Container Apps (ACA). Use it alongside `flet-multiplatform-build` (which covers building the Docker image).

## When to use

After the Flet web Docker image is building and pushing to GHCR successfully (see `flet-multiplatform-build`). Apply when:

- Deploying the web app to Azure Container Apps for the first time
- An existing ACA deployment is broken — WebSocket timeout, ImagePullBackOff, or container crash on startup
- Setting up the CI/CD deploy job
- Debugging a container that starts but the Flet UI never connects

## Inputs expected

- Working Dockerfile with `python main.py` as CMD and `FLET_HOST=0.0.0.0` env var
- GitHub repository with GHCR image publishing configured (`build-web.yml` from `flet-multiplatform-build`)
- Azure subscription (free tier is sufficient for initial deployment)
- Preferred Azure region (e.g. `australiaeast`)
- App name — used for resource group, container app, and service principal naming

---

## Container startup — do not use `flet run --web`

`flet run --web main.py` crashes in a slim container:

```
ModuleNotFoundError: No module named 'flet_desktop'
```

Even in `--web` mode, the `flet` CLI imports `flet_desktop`, which requires native GUI libraries not present in `python:3.12-slim`.

**Fix: use `python main.py` and configure web mode in code.**

`ft.app()` is deprecated since Flet 0.80. Use `ft.run()`. Use a `FLET_HOST` env var so the bind address differs between local dev (`localhost`) and Docker (`0.0.0.0`):

```python
# main.py
if __name__ == "__main__":
    import os
    host = os.environ.get("FLET_HOST", "localhost")
    ft.run(main, host=host, port=8550, view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.CANVAS_KIT)
```

```dockerfile
# Dockerfile — set host and renderer for container
ENV FLET_HOST=0.0.0.0
CMD ["python", "main.py"]
```

`ft.AppView.WEB_BROWSER` starts the Flet HTTP + WebSocket server and skips opening a browser in headless environments. Locally, `flet run --web` works fine on Windows/Mac where `flet_desktop` is installed — the `__main__` block is not reached by `flet run`.

**`web_renderer` valid values in Flet 0.84:** `ft.WebRenderer.AUTO`, `ft.WebRenderer.CANVAS_KIT`, `ft.WebRenderer.SKWASM`. The `html` renderer was removed in Flutter 3+ — passing `"html"` raises a `ValueError`. The `web_renderer` parameter in `ft.run()` only applies when running `python main.py` directly; `flet run --web` ignores it.

---

## flet-web must be in requirements.txt for Dockerfile build steps

`flet_web` auto-installs at runtime when `python main.py` is run directly. However, Dockerfile `RUN python -c "import flet_web, ..."` steps that manipulate the package's web assets execute at **build time** — before the container starts. If `flet-web` is not explicitly listed in `requirements.txt`, these RUN steps will fail with `ModuleNotFoundError`.

```
# requirements.txt
flet==0.84.0
flet-web==0.84.0   # REQUIRED — used in Dockerfile RUN steps to patch web assets
```

Pin the same version as `flet` to avoid version mismatch.

---

## Favicon — overwrite the flet_web default in Dockerfile

Browsers look for `/favicon.png` at the root. The project `assets/` folder is served at `/assets/`, so `assets/favicon.png` is never seen as the favicon. The default favicon comes from inside the `flet_web` package at `flet_web/web/favicon.png`.

**Fix: overwrite it in the Dockerfile after pip install.**

```dockerfile
COPY assets/favicon.png /tmp/favicon.png
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import flet_web, os, shutil; shutil.copy('/tmp/favicon.png', os.path.join(os.path.dirname(flet_web.__file__), 'web', 'favicon.png'))"
```

Or more concisely (after `COPY . .`):

```dockerfile
RUN python -c "import flet_web, os, shutil; shutil.copy('assets/favicon.png', os.path.join(os.path.dirname(flet_web.__file__), 'web', 'favicon.png'))"
```

Do not place `favicon.png` in the project root expecting Flet to serve it — Flet's web server does not route `/favicon.png` from the project root.

---

## Splash/loading screen — overwrite loading-animation.png and patch scale CSS

The Flutter web loading animation lives at `flet_web/web/icons/loading-animation.png` (not the web root). It defaults to a Flutter logo. The CSS scale that controls its displayed size is in `flet_web/web/index.html`.

**Full Dockerfile pattern** — patches favicon, PWA icons, loading animation, and splash scale in one `RUN` step:

```dockerfile
RUN python -c "\
import flet_web, os, shutil; \
web = os.path.join(os.path.dirname(flet_web.__file__), 'web'); \
shutil.copy('assets/favicon.png', os.path.join(web, 'favicon.png')); \
[shutil.copy('assets/logo_192.png', os.path.join(web, 'icons', n)) for n in ['icon-192.png','icon-maskable-192.png','apple-touch-icon-192.png']]; \
[shutil.copy('assets/logo_512.png', os.path.join(web, 'icons', n)) for n in ['icon-512.png','icon-maskable-512.png']]; \
shutil.copy('assets/logo_512.png', os.path.join(web, 'icons', 'loading-animation.png')); \
idx = os.path.join(web, 'index.html'); \
html = open(idx).read().replace('scale(0.4)', 'scale(0.8)').replace('scale(0.35)', 'scale(0.75)'); \
open(idx, 'w').write(html) \
"
```

Notes:
- `loading-animation.png` is in `icons/`, not the web root.
- The CSS scale values (`0.4`, `0.35`) appear twice in `index.html` for portrait and landscape; both must be patched.
- The splash image should be at least 512×512px — use the same source as the PWA 512 icon or a dedicated 2048px splash image.
- `flet-web` must be in `requirements.txt` for this `RUN` step to work (see above).

---

## ACA ingress — force HTTP/1.1 for WebSocket

ACA ingress defaults to `transport: Auto`. Auto may negotiate HTTP/2, which does not support WebSocket upgrades. The symptom is **"stream timeout"** in the browser — the Flet Flutter client loads but the WebSocket never connects.

```bash
az containerapp ingress update \
  --name <app> --resource-group <rg> --transport http
```

Add this to `infra/setup-azure.sh` immediately after container creation. Do not leave it as Auto.

---

## GHCR auth — private packages cannot be pulled by ACA

Every approach to authenticate ACA against a private GHCR package fails:

| Approach | Why it fails |
|---|---|
| Classic PAT with `write:packages` | GHCR token exchange returns base64(PAT) as Bearer; manifest pulls return 404 for private packages |
| `GITHUB_TOKEN` in deploy job | Expires before ACA's async image pull — `ImagePullBackOff` |
| `az containerapp registry set` | Stored credentials persist even after making package public — stale bad creds block pulls |

**Fix: make the GHCR package public.** The Docker image is a compiled artifact — it does not expose source code. The private repository stays private.

```
GitHub → Profile → Packages → <package> → Package settings → Change visibility → Public
```

Then remove any stored registry credentials from ACA:

```bash
az containerapp registry remove --name <app> --resource-group <rg> --server ghcr.io
```

And simplify the deploy step — no registry auth fields:

```yaml
- uses: azure/container-apps-deploy-action@v2
  with:
    resourceGroup: rg-<appname>
    containerAppName: <appname>
    imageToDeploy: ghcr.io/<owner>/<repo-lowercase>:latest
```

If you previously stored bad credentials, remove them explicitly — they persist and block pulls even after the package is made public.

---

## ACA provisioning — common gotchas

- **Register resource providers before creating an environment:**
  ```bash
  az provider register -n Microsoft.App --wait --output none
  az provider register -n Microsoft.OperationalInsights --wait --output none
  ```

- **Use `--logs-destination none`** to skip Log Analytics workspace creation.

- **Bootstrap with a placeholder image**, then let CI deploy the real one:
  ```bash
  az containerapp create \
    --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
    --target-port 8550 ...
  ```

- **Set target port to 8550** — the placeholder uses port 80. The deploy action does not update the target port, only the image.

- **Set min replicas to 1.** With 0 min replicas, the first browser request arrives before the container is ready, causing a WebSocket cold-start timeout.

- **`--sdk-auth` is deprecated in Azure CLI 2.37+.** Build the credentials JSON manually:
  ```bash
  SP=$(az ad sp create-for-rbac --name "sp-<app>-github" --role Contributor \
    --scopes "/subscriptions/${SUB_ID}/resourceGroups/${RG}" --output json)
  # Extract appId, password, tenant from SP JSON + subscription ID
  ```

- **`MSYS_NO_PATHCONV=1` on any `az` call passing Unix-style paths in Git bash.** Git bash converts `/subscriptions/...` to `C:/Program Files/Git/subscriptions/...`:
  ```bash
  MSYS_NO_PATHCONV=1 az ad sp create-for-rbac --scopes "/subscriptions/..."
  ```

---

## Forcing a new ACA revision

`az containerapp update --image ...:latest` may not create a new revision if ACA sees the same tag. Use `--revision-suffix` to force one. In CI, use `${{ github.run_number }}` so each deploy gets a unique suffix automatically:

```bash
az containerapp update \
  --name <app> --resource-group <rg> \
  --image ghcr.io/<owner>/<repo>:latest \
  --revision-suffix r${{ github.run_number }} \
  --output none
```

This replaces the `azure/container-apps-deploy-action@v2` action approach — the `az` CLI is simpler and gives full control over the revision suffix.

---

## Diagnosing ACA revision failures

Check `runningStateDetails` to distinguish the two failure types:

```bash
az containerapp revision show \
  --name <app> --resource-group <rg> --revision <name> \
  --query "properties.runningStateDetails" -o tsv
```

| Value | Meaning | Fix |
|---|---|---|
| `Pending:ImagePullBackOff` | Image cannot be pulled | Fix registry auth or make package public |
| `Container crashing` | Image pulled, app crashes on startup | Check container logs |

Fetch logs for crash diagnosis:

```bash
az containerapp logs show \
  --name <app> --resource-group <rg> --revision <name> --tail 50
```

---

## Complete deploy job (GitHub Actions)

Use `az containerapp update` directly — simpler than the deploy action and guarantees a new revision via `--revision-suffix`:

```yaml
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Azure login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy to Azure Container Apps
        run: |
          az containerapp update \
            --name <appname> \
            --resource-group rg-<appname> \
            --image ghcr.io/<owner>/<repo-lowercase>:latest \
            --revision-suffix r${{ github.run_number }} \
            --output none
```

- Image name MUST be lowercase — GHCR package must be public (no auth credentials needed).
- `--revision-suffix r${{ github.run_number }}` guarantees a new revision every CI run.
- Required secret: `AZURE_CREDENTIALS` (SP JSON — see `infra/setup-azure.sh`).

---

## infra/setup-azure.sh — full pattern

```bash
#!/usr/bin/env bash
set -e
AZ="/c/Program Files/Microsoft SDKs/Azure/CLI2/wbin/az"
GH="/c/Program Files/GitHub CLI/gh.exe"
RESOURCE_GROUP="rg-<appname>"
LOCATION="australiaeast"
APP_NAME="<appname>"
REPO="<owner>/<repo>"

"$AZ" provider register -n Microsoft.App --wait --output none
"$AZ" provider register -n Microsoft.OperationalInsights --wait --output none
"$AZ" group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none
"$AZ" containerapp env create \
    --name "${APP_NAME}-env" --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" --logs-destination none --output none

"$AZ" containerapp create \
    --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
    --environment "${APP_NAME}-env" \
    --image "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" \
    --target-port 8550 --ingress external \
    --min-replicas 1 --max-replicas 2 --cpu 0.5 --memory 1.0Gi \
    --output none

# Force HTTP/1.1 — required for Flet WebSocket
"$AZ" containerapp ingress update \
    --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" \
    --transport http --output none

# No registry credentials — GHCR package must be public

SUBSCRIPTION_ID=$("$AZ" account show --query id -o tsv)
SP=$(MSYS_NO_PATHCONV=1 "$AZ" ad sp create-for-rbac \
    --name "sp-${APP_NAME}-github" --role Contributor \
    --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}" \
    --output json 2>/dev/null)

CLIENT_ID=$(echo "$SP" | python3 -c "import sys,json; print(json.load(sys.stdin)['appId'])")
CLIENT_SECRET=$(echo "$SP" | python3 -c "import sys,json; print(json.load(sys.stdin)['password'])")
TENANT_ID=$(echo "$SP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant'])")
SP_JSON=$(printf '{"clientId":"%s","clientSecret":"%s","subscriptionId":"%s","tenantId":"%s"}' \
    "$CLIENT_ID" "$CLIENT_SECRET" "$SUBSCRIPTION_ID" "$TENANT_ID")
echo "$SP_JSON" | "$GH" secret set AZURE_CREDENTIALS --repo "$REPO"
```

---

## Quality checklist

- [ ] Dockerfile CMD uses `python main.py`, not `flet run --web main.py`
- [ ] `main.py` uses `ft.run()` (not deprecated `ft.app()`) with `FLET_HOST` env var and `web_renderer=ft.WebRenderer.CANVAS_KIT`
- [ ] Dockerfile sets `ENV FLET_HOST=0.0.0.0`
- [ ] `flet-web==<version>` in `requirements.txt` (same version as `flet`) — required for Dockerfile RUN asset steps
- [ ] Dockerfile RUN step overwrites: `flet_web/web/favicon.png`, PWA icons, `icons/loading-animation.png`, and patches CSS scale in `index.html`
- [ ] ACA ingress transport set to `Http` — scripted in `infra/setup-azure.sh`
- [ ] ACA target port is 8550
- [ ] ACA min replicas set to 1
- [ ] GHCR package is public — no registry credentials stored in ACA
- [ ] Deploy workflow uses `az containerapp update` with `--revision-suffix r${{ github.run_number }}`
- [ ] Deploy workflow image reference is hardcoded lowercase
- [ ] `infra/setup-azure.sh` in repo — provisions everything from scratch reproducibly
- [ ] `AZURE_CREDENTIALS` GitHub secret set (SP JSON)

---

## Avoid

- `flet run --web` as Dockerfile CMD — crashes in slim containers; use `python main.py`
- `ft.app()` — deprecated since Flet 0.80; use `ft.run()`
- `web_renderer="html"` — removed in Flutter 3+; raises `ValueError`; use `ft.WebRenderer.CANVAS_KIT`
- Hardcoding `host="0.0.0.0"` in `ft.run()` — breaks local dev (browser opens `0.0.0.0`); use `FLET_HOST` env var
- Placing `favicon.png` in project `assets/` and expecting it to appear as the browser tab icon — it won't; overwrite `flet_web/web/favicon.png` in Dockerfile
- Omitting `flet-web` from `requirements.txt` — Dockerfile RUN steps that `import flet_web` will fail at build time even though it auto-installs at runtime
- Loading animation path `flet_web/web/loading-animation.png` — wrong path; it is in `flet_web/web/icons/loading-animation.png`
- ACA ingress transport `Auto` — may break WebSocket; use `Http`
- Private GHCR packages pulled by ACA — PATs and GITHUB_TOKEN both fail; use a public package
- Storing registry credentials in ACA for a public package — remove them if previously set
- `az containerapp update --image ...:latest` alone to force a new revision — always add `--revision-suffix r${{ github.run_number }}`
- `azure/container-apps-deploy-action@v2` — does not support `--revision-suffix`; use `az containerapp update` directly
- Min replicas 0 in production — WebSocket cold-start breaks the UI
- `--sdk-auth` flag with `az ad sp create-for-rbac` — deprecated in Azure CLI 2.37+
- Unix-style paths in `az` commands from Git bash without `MSYS_NO_PATHCONV=1`

## Example usage

> "The Flet web Docker image is building and pushing to GHCR. Set up Azure Container Apps and the GitHub Actions deploy job. Provision everything from scratch using the az CLI and store the AZURE_CREDENTIALS secret automatically."

---

_Source: This skill is sourced from the [PowerData Skills](https://github.com/POWR-DATA/skills) library. Learn more at the [AI Agent Skills Library](https://powrdata.com.au/ai-agent-skills)._
