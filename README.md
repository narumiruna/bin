# bin

一個以 Hugo 建立的靜態網站專案，內容包含 AI agent 方法論文章與 YouTube 字幕抓取腳本。

## 專案結構

- `content/`：網站文章內容（Markdown）
- `layouts/`：Hugo 模板
- `static/`：靜態資源（CSS）
- `scripts/fetch_subtitles.py`：抓取 YouTube 字幕並輸出 `.srt`
- `subtitles/`：已抓取的字幕檔
- `.github/workflows/hugo.yml`：GitHub Pages 部署流程

## 本機啟動網站

前置需求：已安裝 `hugo`。

```bash
hugo server -D
```

啟動後預設可在 `http://localhost:1313` 查看網站。

## 建置網站

```bash
hugo --minify
```

輸出目錄為 `public/`（已在 `.gitignore` 忽略）。

## 抓取 YouTube 字幕

前置需求：已安裝 `uv`。

```bash
uv run scripts/fetch_subtitles.py "https://www.youtube.com/watch?v=<VIDEO_ID>"
```

常用參數：

```bash
uv run scripts/fetch_subtitles.py <URL_OR_ID> --out-dir subtitles --languages zh-TW zh-Hant zh en
```

輸出規則：

- 有影片標題：`{title} [{video_id}].srt`
- 無影片標題（fallback）：`{video_id}.srt`
