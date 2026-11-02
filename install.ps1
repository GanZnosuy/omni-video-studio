# ==============================================================================
# OMNI VIDEO STUDIO — AUTOMATED INSTALLATION SCRIPT (WINDOWS)
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "🎬 Installing Omni Video Studio..." -ForegroundColor Cyan

$userHome = [System.Environment]::GetFolderPath('UserProfile')
$targetDir = Join-Path $userHome ".gemini\config\skills\omni-video-studio"
$claudeDir = Join-Path $userHome ".claude\skills\omni-video-studio"
$codexDir  = Join-Path $userHome ".codex\skills\omni-video-studio"

# 1. Clone into Antigravity Global Skills
if (!(Test-Path $targetDir)) {
    Write-Host "Cloning into Antigravity Global Skills ($targetDir)..." -ForegroundColor Yellow
    git clone https://github.com/GanZnosuy/omni-video-studio.git $targetDir
} else {
    Write-Host "Updating Antigravity Global Skills..." -ForegroundColor Yellow
    git -C $targetDir pull
}

# 2. Symlink or copy to Claude Code & Codex
if (!(Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path (Split-Path $claudeDir) -Force | Out-Null
    Copy-Item -Path $targetDir -Destination $claudeDir -Recurse -Force
    Write-Host "Linked to Claude Code ($claudeDir)" -ForegroundColor Green
}

if (!(Test-Path $codexDir)) {
    New-Item -ItemType Directory -Path (Split-Path $codexDir) -Force | Out-Null
    Copy-Item -Path $targetDir -Destination $codexDir -Recurse -Force
    Write-Host "Linked to Codex ($codexDir)" -ForegroundColor Green
}

Write-Host "✅ Omni Video Studio successfully installed!" -ForegroundColor Green
