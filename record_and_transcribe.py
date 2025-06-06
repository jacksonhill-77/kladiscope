import asyncio
import os
import json
import pyaudio
import websockets

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Deepgram API key not found. Set DEEPGRAM_API_KEY in your environment.")

# Mic settings
RATE = 16000
CHUNK = 1024

def record_and_transcribe_deepgram(seconds=5):
    print("🎙️ Streaming to Deepgram...")
    return asyncio.run(deepgram_stream(seconds))


async def deepgram_stream(seconds):
    transcript = ""

    # Build headers manually in the URL
    url = (
        "wss://api.deepgram.com/v1/listen?punctuate=true&language=en"
        f"&access_token={DEEPGRAM_API_KEY}"
    )

    async with websockets.connect(
        url,
        ping_interval=5,
        ping_timeout=20
    ) as ws:

        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        async def send_audio():
            for _ in range(0, int(RATE / CHUNK * seconds)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                await ws.send(data)
            await ws.send(b"")

        async def receive_transcript():
            nonlocal transcript
            async for msg in ws:
                msg_json = json.loads(msg)
                if "channel" in msg_json and "alternatives" in msg_json["channel"]:
                    words = msg_json["channel"]["alternatives"][0].get("transcript", "")
                    if words:
                        transcript = words
                if msg_json.get("is_final"):
                    break

        await asyncio.gather(send_audio(), receive_transcript())

        stream.stop_stream()
        stream.close()
        audio.terminate()

    print(f"🗣️ Transcript: {transcript}")
    return transcript.strip()
