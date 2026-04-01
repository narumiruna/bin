#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "youtube-transcript-api==1.2.4",
# ]
# ///

from __future__ import annotations

import argparse
import re
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter


VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})")


def extract_video_id(url_or_id: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id

    match = VIDEO_ID_RE.search(url_or_id)
    if not match:
        raise ValueError(f"Cannot parse video id from: {url_or_id}")
    return match.group(1)


def sanitize_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._ -]+", "_", text).strip() or "untitled"


def fetch_and_save(video: str, out_dir: Path, languages: list[str]) -> Path:
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video, languages=languages)

    formatter = SRTFormatter()
    srt_text = formatter.format_transcript(transcript)

    title = sanitize_filename(getattr(transcript, "video_title", ""))
    # video_title may be unavailable depending on upstream response; keep deterministic fallback.
    if not title or title == "untitled":
        out_path = out_dir / f"{video}.srt"
    else:
        out_path = out_dir / f"{title} [{video}].srt"
    out_path.write_text(srt_text, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch YouTube subtitles and save as SRT.")
    parser.add_argument("urls", nargs="+", help="YouTube URLs or video IDs")
    parser.add_argument(
        "--out-dir",
        default="subtitles",
        help="Directory to store subtitle files (default: subtitles)",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["zh-TW", "zh-Hant", "zh", "en"],
        help="Language priority list (default: zh-TW zh-Hant zh en)",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    failed: list[str] = []
    saved: list[Path] = []

    for raw in args.urls:
        try:
            video = extract_video_id(raw)
            path = fetch_and_save(video, out_dir, args.languages)
            saved.append(path)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAILED] {raw}: {exc}")
            failed.append(raw)

    for path in saved:
        print(f"[SAVED] {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
