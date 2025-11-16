#!/bin/bash
set -e

echo "🔨 Building SvelteKit site..."
cd svelte
npm install
npm run build
cd ..

echo "📦 Copying to site/ folder..."
rm -rf site
cp -r svelte/build site

echo "✅ Build complete! Run: docker compose up"
