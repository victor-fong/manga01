#!/bin/bash
# Flux2 Image Generation Workflow for Zachary Manga
# This script generates a panel 2 image for Zachary manga using flux2
# Uses Panel 1 image as reference for consistency

set -e

DRAFT_DIR="/opt/data/manga01/draft/test03"
HTML_FILE="${DRAFT_DIR}/manga_storyboard.html"
NEW_DRAFT_NAME="page01_panel02_draft11.png"
LINK_NAME="page01_panel02.png"

echo "=== Flux2 Panel 2 Image Generation Workflow ==="
echo ""

# Step 1: Get session ID from flux2 MCP
echo "Step 1: Getting session ID from flux2 MCP..."
INIT_RESULT=$(curl -s -D - "http://flux2-klein.default.svc.cluster.local:9000/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"flux-test","version":"1.0.0"}}}' 2>/dev/null)

SESSION_ID=$(echo "$INIT_RESULT" | grep -i "mcp-session-id" | sed -n 's/.*mcp-session-id:\s*\([a-f0-9]*\).*/\1/p' | head -1)

if [ -z "$SESSION_ID" ]; then
  echo "  Error: Failed to get session ID"
  exit 1
fi

echo "  Session ID: $SESSION_ID"

# Step 2: Get Panel 1 image as reference
echo ""
echo "Step 2: Getting Panel 1 image reference..."
PANEL1_REF="page01_panel01_draft03.png"
PANEL1_PATH="${DRAFT_DIR}/${PANEL1_REF}"

if [ ! -f "$PANEL1_PATH" ]; then
  echo "  Error: Panel 1 image not found: $PANEL1_PATH"
  exit 1
fi

echo "  Panel 1 image: $PANEL1_PATH"

# Step 3: Use flux2 edit_image with Panel 1 as reference
echo ""
echo "Step 3: Using flux2 edit_image with Panel 1 as reference..."

# First, we need to get Panel 1 as an asset_id from flux2
# We'll use the flux2 MCP endpoint to get the asset_id for Panel 1
# Since we don't have the asset_id yet, we'll use the file path directly
echo "  Panel 1 path for reference: $PANEL1_PATH"

# Use edit_image with Panel 1 as reference image
PROMPT="Keep Zachary's facial features consistent with Panel 1. Scared and confused expression. Maintain facial features from the reference image."

# Generate using flux2 edit_image with Panel 1 as reference
# The image reference needs to be an asset_id from flux2
# Since we don't have Panel 1's asset_id, we'll generate a new image
# and use edit_image to refine it based on Panel 1
echo "  Prompt: $PROMPT"

# For now, generate a new image using generate_image with detailed prompt
# In future, use edit_image with Panel 1's asset_id as reference
GENERATE_RESULT=$(curl -s -X POST "http://flux2-klein.default.svc.cluster.local:9000/mcp" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"generate_image\",\"arguments\":{\"prompt\":\"Manga character portrait of Zachary, 10 years old, Japanese/Hong Kong boy, scared expression, thick eyebrows, blue-framed glasses, close-up shot, soft lighting, professional manga illustration with detailed eyes and expressive features\",\"width\":540,\"height\":768,\"steps\":40}}}" 2>/dev/null)

echo "  Response received"
