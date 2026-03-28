#!/bin/bash
cd "$(dirname "$0")"

echo "🌿 Running the Natuurpunt agent..."
python natuurpunt_agent.py

if [ ! -f "natuurpunt_vlaams_brabant.ics" ]; then
    echo "❌ No .ics file generated."
    exit 1
fi

echo "📤 Pushing to GitHub Pages..."
git add .
git commit -m "Update calendar $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ Done!"
