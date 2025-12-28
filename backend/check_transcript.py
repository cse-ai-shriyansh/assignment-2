from youtube_transcript_api import YouTubeTranscriptApi

video_id = "c-UUFkNeQQY"

try:
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    print("✅ Transcript exists")

    for t in transcripts:
        print(t.language_code, t.is_generated, t.is_translatable)

except Exception as e:
    print("❌ Error:", e)
