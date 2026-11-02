#!/usr/bin/env bash
set -e

echo "🎬 Installing Omni Video Studio..."

TARGET_DIR="$HOME/.gemini/config/skills/omni-video-studio"
CLAUDE_DIR="$HOME/.claude/skills/omni-video-studio"
CODEX_DIR="$HOME/.codex/skills/omni-video-studio"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Cloning into Antigravity Global Skills ($TARGET_DIR)..."
    git clone https://github.com/GanZnosuy/omni-video-studio.git "$TARGET_DIR"
else
    echo "Updating Antigravity Global Skills..."
    git -C "$TARGET_DIR" pull
fi

mkdir -p "$(dirname "$CLAUDE_DIR")"
cp -R "$TARGET_DIR" "$CLAUDE_DIR"
echo "Linked to Claude Code ($CLAUDE_DIR)"

mkdir -p "$(dirname "$CODEX_DIR")"
cp -R "$TARGET_DIR" "$CODEX_DIR"
echo "Linked to Codex ($CODEX_DIR)"

echo "✅ Omni Video Studio successfully installed!"
