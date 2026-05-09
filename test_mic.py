import os
import json
import wave
import pyaudio
import vosk

model_path = "./vosk-model"
record_seconds = 5
chunk = 4000
rate = 16000

GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RESET  = "\033[0m"


def list_mics():
    print(f"\n{CYAN}microphones on your system:{RESET}")
    audio = pyaudio.PyAudio()

    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            tag = " <- default" if i == audio.get_default_input_device_info()["index"] else ""
            print(f"  [{i}] {info['name']}{tag}")

    audio.terminate()


def record(seconds, device=None):
    audio = pyaudio.PyAudio()
    chunks = []

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        input_device_index=device,
        frames_per_buffer=chunk
    )

    print(f"{RED}recording...{RESET} say a chess move")

    total = int(rate / chunk * seconds)
    for i in range(total):
        data = stream.read(chunk, exception_on_overflow=False)
        chunks.append(data)
        left = seconds - int(i * chunk / rate)
        print(f"  {left}s left  ", end="\r")

    print(f"\n{GREEN}done recording{RESET}      ")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return chunks


def save_wav(chunks, filename="recording.wav"):
    audio = pyaudio.PyAudio()
    with wave.open(filename, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        f.setframerate(rate)
        f.writeframes(b"".join(chunks))
    audio.terminate()
    return filename


def playback(filename):
    print(f"\n{CYAN}playing back...{RESET}")
    audio = pyaudio.PyAudio()

    with wave.open(filename, "rb") as f:
        stream = audio.open(
            format=audio.get_format_from_width(f.getsampwidth()),
            channels=f.getnchannels(),
            rate=f.getframerate(),
            output=True
        )
        data = f.readframes(chunk)
        while data:
            stream.write(data)
            data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(f"{GREEN}playback done{RESET}")


def transcribe(filename):
    if not os.path.exists(model_path):
        print(f"{RED}vosk model not found - run download_model.py{RESET}")
        return None

    print(f"\n{CYAN}running through vosk...{RESET}")
    vosk.SetLogLevel(-1)
    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, rate)

    with wave.open(filename, "rb") as f:
        while True:
            data = f.readframes(4000)
            if not data:
                break
            rec.AcceptWaveform(data)

    result = json.loads(rec.FinalResult())
    return result.get("text", "").strip()


def parse(text):
    from listener import VoiceListener

    class Quick(VoiceListener):
        def __init__(self):
            pass

    return Quick().parse(text)


def main():
    print(f"\n{CYAN}mic test tool{RESET}\n")

    list_mics()

    print(f"\n{YELLOW}which mic to use? press enter for default, or type a number: {RESET}", end="")
    choice = input().strip()
    device = int(choice) if choice.isdigit() else None

    input(f"\npress enter to start recording ({record_seconds} seconds)... ")
    chunks = record(record_seconds, device)
    filename = save_wav(chunks)

    playback(filename)

    print(f"\n{YELLOW}did you hear your voice clearly? (y/n): {RESET}", end="")
    answer = input().strip().lower()

    if answer != "y":
        print(f"\n{RED}mic issue - try a different mic number or check your settings{RESET}")
        return

    text = transcribe(filename)

    if not text:
        print(f"{RED}vosk couldn't hear anything - speak louder or closer to mic{RESET}")
        return

    print(f"\n{GREEN}vosk heard:{RESET} '{text}'")

    move = parse(text)

    if move:
        src, dst = move
        print(f"{GREEN}move parsed:{RESET} {src} → {dst}")
    else:
        print(f"{RED}couldn't parse a move from that - try saying 'e2 to e4'{RESET}")

    if os.path.exists(filename):
        os.remove(filename)

    print(f"\n{GREEN}all good - run main.py to start playing{RESET}\n")


if __name__ == "__main__":
    main()