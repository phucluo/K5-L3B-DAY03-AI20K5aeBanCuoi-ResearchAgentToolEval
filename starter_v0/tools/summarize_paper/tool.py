from __future__ import annotations

import re
from typing import Any

from tools._shared import err


ALLOWED_FOCUS_AREAS = {"all", "methodology", "findings", "limitations"}


def summarize_paper(
    paper_text: str = "",
    focus_area: str = "all",
    max_points: int = 3,
) -> dict[str, Any]:
    """Extract structured takeaways from research paper text."""
    try:
        if not paper_text or not isinstance(paper_text, str) or not paper_text.strip():
            raise ValueError("paper_text must not be empty")

        if focus_area not in ALLOWED_FOCUS_AREAS:
            focus_area = "all"

        limit = max(1, min(int(max_points or 3), 10))

        sentences = [
            s.strip()
            for s in re.split(r"[.\n]+", paper_text)
            if len(s.strip()) > 20
        ]

        if not sentences:
            raise ValueError("No meaningful sentences found in paper_text")

        keywords = {
            "methodology": ["method", "propose", "architecture", "model", "algorithm", "approach", "train"],
            "findings": ["result", "show", "outperform", "achieve", "improve", "accuracy", "findings"],
            "limitations": ["limit", "bottleneck", "future work", "drawback", "failure", "cost", "weakness"],
        }

        if focus_area == "all":
            selected = sentences[:limit]
        else:
            targets = keywords.get(focus_area, [])
            selected = [
                s for s in sentences
                if any(k in s.lower() for k in targets)
            ]
            if not selected:
                selected = sentences[:limit]
            else:
                selected = selected[:limit]

        takeaways = selected[:limit]
        return {
            "tool": "summarize_paper",
            "focus_area": focus_area,
            "point_count": len(takeaways),
            "takeaways": takeaways,
            "status": "success",
        }
    except Exception as exc:
        return err("summarize_paper", exc)

