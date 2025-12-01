# personal_webpage

Static personal website frontend (SvelteKit) + Python FastAPI backend that answers FAQ-style questions about me using the Anthropic Claude API.

Overview
--------
This repo hosts a small SvelteKit frontend (static pre-render) and a FastAPI backend providing:
- /api/ask POST - ask a question about *Lennart* using Anthropic Claude (`/api/ask` implemented in [backend/app/main.py](backend/app/main.py))
- /api/health GET - simple health endpoint
- /admin - simple HTML admin panel, protected by token (`ADMIN_TOKEN`)

The backend uses Anthropic to (1) classify if a question is about Lennart and (2) answer it using the `backend/data/about_me.txt` biography.

Architecture
------------
- Frontend: SvelteKit pre-rendered build in `/svelte` built to `/svelte/build` and copied to `/site` by the build script. Dev server: [svelte/package.json](svelte/package.json) (npm scripts).
- Backend: Python FastAPI in [backend/](backend/). Dockerfile builds the backend container and exposes it on port 8000.
- Reverse proxy: Caddy configured in [Caddyfile](Caddyfile). It proxies `/api` and `/admin` to the backend and serves static files from `/site`.
- Deployment: Docker Compose (`docker-compose.yml`) for hosting both services and a GitHub Actions workflow (see [.github/workflows/deploy.yml](.github/workflows/deploy.yml)) to deploy to a VPS.

Local development
-----------------
Build local static site and run with Docker Compose:
   - Build frontend static site and copy to :
     ```bash
     ./build-local.sh
     ```
   - Start services:
     ```bash
     DOMAIN=localhost \
     ANTHROPIC_API_KEY=<your-key> \
     ADMIN_TOKEN=<token> \
     docker compose up -d --build
     ```
   - Visit: http://localhost
