#!/usr/bin/env python3
"""
OMNI VIDEO STUDIO — Autonomous Intent Router & Pipeline Dispatcher
Analyzes creative tasks and directs to the optimal video/motion/design engine.
"""

import sys
import json
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT_DIR / "modules"

ENGINES = {
    "core1_anything2video": {
        "name": "Anything-to-Video Multimodal Engine",
        "path": "modules/01_anything2video",
        "keywords": ["article", "script", "audio", "podcast", "explainer", "documentary", "bài viết", "kịch bản", "làm video từ", "chuyển bài"],
        "desc": "Converts text, articles, audio, and data into fully scripted, voiced, and rendered videos."
    },
    "core2_shotcraft": {
        "name": "Cinematic ShotCraft & Director",
        "path": "modules/02_video_shotcraft",
        "keywords": ["camera", "shot", "lens", "dolly", "orbit", "flycam", "capcut", "jianying", "beat sync", "góc quay", "máy quay", "tiêu cự"],
        "desc": "124 Hollywood cinematic shot cards, 3D camera paths, CapCut/JianYing draft export, and beat alignment."
    },
    "core3_mg_styles": {
        "name": "15 Motion Graphics Styles",
        "path": "modules/03_mg_styles_15",
        "keywords": ["motion graphics", "mg", "isometric", "kinetic typo", "hud", "liquid", "flat vector", "cel boil", "synthwave", "đồ họa chuyển động"],
        "desc": "15 battle-tested Motion Graphics styles with prompt engineering templates and design rubrics."
    },
    "core4_code_animation": {
        "name": "Code-Driven Animation Studio",
        "path": "modules/04_code_animation_studio",
        "keywords": ["remotion", "motion canvas", "threejs", "webgl", "canvas", "p5js", "svg", "lottie", "code animation", "lập trình hoạt hình"],
        "desc": "Deterministic, pixel-perfect code animation with zero AI hallucinations (React, TypeScript, Three.js, Canvas)."
    },
    "core5_dashi_dynamics": {
        "name": "Dashi Master Animation & Dynamics",
        "path": "modules/05_dashi_animation_style",
        "keywords": ["animation", "squash and stretch", "anticipation", "easing", "cubic-bezier", "timing sheet", "hoạt hình", "độ mượt", "gia tốc"],
        "desc": "Disney & Anime 12 animation principles, nonlinear easing curves, and physics-based motion."
    },
    "core6_huashu_oriental": {
        "name": "Huashu Oriental Art Motion & Donghua",
        "path": "modules/06_huashu_art_motion",
        "keywords": ["ink wash", "donghua", "anime", "thủy mặc", "tiên hiệp", "kiếm hiệp", "võ thuật", "thư pháp", "oriental", "asian fantasy"],
        "desc": "Chinese ink wash diffusion, Donghua combat dynamics, and Asian aesthetic video generation."
    },
    "core7_baoyu_design": {
        "name": "Baoyu Visual & Knowledge Architecture",
        "path": "modules/07_baoyu_design",
        "keywords": ["infographic", "svg card", "comic strip", "knowledge card", "slide", "tóm tắt", "thẻ kiến thức", "truyện tranh", "visual design"],
        "desc": "Visual knowledge cards, SVG summaries, 4-panel comic strip storytelling, and slide design."
    },
    "core8_opus_prompting": {
        "name": "Opus Cinematic Prompt Architect",
        "path": "modules/08_opus_cinematic",
        "keywords": ["prompt", "kling", "sora", "runway", "gen-3", "midjourney", "flux", "luma", "hailuo", "câu lệnh", "tạo prompt"],
        "desc": "Cinematic prompt engineering formulas for modern generative AI video and image models."
    }
}


def classify_intent(query: str):
    q = query.lower()
    scores = {}
    for key, data in ENGINES.items():
        score = sum(1 for kw in data["keywords"] if kw in q)
        scores[key] = score
    
    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_key, best_score = sorted_scores[0]
    
    if best_score == 0:
        # Default to multimodal engine if no specific keywords matched
        best_key = "core1_anything2video"
        
    return best_key, ENGINES[best_key]


def main():
    parser = argparse.ArgumentParser(description="Omni Video Studio Router")
    parser.add_argument("task", nargs="*", help="Task description or prompt")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    task_str = " ".join(args.task) if args.task else "Tạo video giải thích từ bài viết"
    engine_id, info = classify_intent(task_str)

    if args.json:
        print(json.dumps({
            "task": task_str,
            "engine_id": engine_id,
            "engine_name": info["name"],
            "module_path": info["path"],
            "description": info["desc"]
        }, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("🎬 OMNI VIDEO STUDIO — AUTONOMOUS DISPATCH RESULT")
        print("=" * 60)
        print(f"📌 Yêu cầu: {task_str}")
        print(f"🎯 Lõi kích hoạt: {info['name']} ({engine_id})")
        print(f"📁 Thư mục mã nguồn: {info['path']}")
        print(f"ℹ️ Mô tả chức năng: {info['desc']}")
        print("=" * 60)


if __name__ == "__main__":
    main()
