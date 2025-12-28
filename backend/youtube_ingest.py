from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)


def fetch_transcript(url: str):
    video_id = extract_video_id(url)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # 1️⃣ Try English directly (manual or generated)
    try:
        transcript = transcript_list.find_transcript(["en"])
    except:
        # 2️⃣ Otherwise find ANY transcript and translate to English
        transcript = transcript_list.find_transcript(
            [t.language_code for t in transcript_list]
        ).translate("en")

    raw = transcript.fetch()

    # 3️⃣ Chunk into NotebookLM-style pages
    pages = []
    buffer = ""
    page_num = 1

    for entry in raw:
        buffer += entry["text"] + " "

        if len(buffer) >= 800:
            pages.append({
                "page": f"YT-{page_num}",
                "text": buffer.strip()
            })
            buffer = ""
            page_num += 1

    if buffer:
        pages.append({
            "page": f"YT-{page_num}",
            "text": buffer.strip()
        })

    return pages
