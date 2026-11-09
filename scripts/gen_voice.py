import asyncio
import os
import json
import re
import subprocess
import edge_tts

VOICE = "en-US-ChristopherNeural"
OUTPUT_DIR = "/root/agyrepo/voice"
MP3_FILE = os.path.join(OUTPUT_DIR, "voice_raw.mp3")
WAV_FILE = os.path.join(OUTPUT_DIR, "voice.wav")
WORDS_FILE = os.path.join(OUTPUT_DIR, "words.json")

SCRIPT_TEXT = """If you fall off a tower, your brain thinks you entered The Matrix.
In 2007, scientists dropped volunteers a hundred and fifty feet into free fall.
While falling at seventy miles an hour, they stared at wristwatches flashing numbers.
If panic actually slowed down time, reading them would be easy.
Nobody could read a single one.
Luckily, the net caught them.
Unluckily, their brains were lying.
Panic does not speed up your eyes.
Instead, terror triggers an emergency memory dump, recording every tiny detail without compression.
When you land, your brain unzips that massive file and assumes the fall lasted ten seconds.
The world never slowed down.
You just took five times longer to remember screaming."""

async def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    c = edge_tts.Communicate(SCRIPT_TEXT, VOICE, rate="+20%")
    
    sentences = []
    audio_data = bytearray()
    
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            s = chunk["offset"] / 1e7
            e = (chunk["offset"] + chunk["duration"]) / 1e7
            txt = chunk["text"]
            sentences.append({"s": s, "e": e, "text": txt})
            
    with open(MP3_FILE, "wb") as f:
        f.write(audio_data)
        
    subprocess.run([
        "ffmpeg", "-y", "-i", MP3_FILE,
        "-ar", "48000", "-ac", "2", WAV_FILE
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    words = []
    for sent in sentences:
        s_time = sent["s"]
        e_time = sent["e"]
        raw_words = [w for w in sent["text"].split() if w]
        if not raw_words:
            continue
        total_chars = sum(len(w) for w in raw_words)
        duration = e_time - s_time
        curr = s_time
        for w in raw_words:
            w_dur = max(0.10, duration * (len(w) / total_chars))
            w_end = min(e_time, curr + w_dur)
            clean_w = re.sub(r'^[^\w]+|[^\w]+$', '', w)
            words.append({
                "w": clean_w,
                "s": round(curr, 3),
                "e": round(w_end, 3)
            })
            curr = w_end
            
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
        
    print(f"Generated {len(words)} words in {sentences[-1]['e']:.2f}s.")
    print(f"Total audio duration: {sentences[-1]['e']:.2f}s (Target: ~36s-38s for 40s short).")

if __name__ == "__main__":
    asyncio.run(generate())
