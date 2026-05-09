import re
import os
import json
import vosk
import pyaudio


model_path = "./vosk-model"

words = [
    "a", "b", "c", "d", "e", "f", "g", "h",
    "1", "2", "3", "4", "5", "6", "7", "8",
    "one", "two", "three", "four", "five", "six", "seven", "eight",
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "ay", "bee", "see", "sea", "dee", "ef", "gee", "aitch",
    "move", "place", "put", "from", "to", "the",
    "pawn", "knight", "bishop", "rook", "queen", "king",
    "castle", "castling", "kingside", "queenside", "side", "short", "long",
    "quit", "exit", "flip", "board", "recalibrate",
    "uh", "um", "okay", "now", "i", "want", "my", "you", "know", "what",
]

letters = {
    "alpha": "a", "ay": "a",
    "bravo": "b", "bee": "b",
    "charlie": "c", "see": "c", "sea": "c",
    "delta": "d", "dee": "d",
    "echo": "e", "ee": "e",
    "foxtrot": "f", "ef": "f",
    "golf": "g", "gee": "g",
    "hotel": "h", "aitch": "h",
}

numbers = {
    "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8",
}

castling = {
    "castle kingside":   ("e1", "g1"),
    "castle king side":  ("e1", "g1"),
    "short castle":      ("e1", "g1"),
    "castle queenside":  ("e1", "c1"),
    "castle queen side": ("e1", "c1"),
    "long castle":       ("e1", "c1"),
}

pattern = re.compile(
    r"""
    \b
    ([a-h]|alpha|bravo|charlie|delta|echo|foxtrot|golf|hotel|ay|bee|see|sea|dee|ef|gee|aitch)
    \s*
    ([1-8]|one|two|three|four|five|six|seven|eight)
    \b
    """,
    re.IGNORECASE | re.VERBOSE,
)


class VoiceListener:

    def __init__(self):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"model not found at {model_path}\n"
                f"run download_model.py first"
            )

        print("loading vosk...")
        vosk.SetLogLevel(-1)
        model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(model, 16000, json.dumps(words))

        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()
        print("vosk ready")

    def listen(self):
        self.rec.Reset()

        while True:
            chunk = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(chunk):
                data = json.loads(self.rec.Result())
                text = data.get("text", "").strip()
                return text if text else None

    def parse(self, text):
        text = self.clean(text)

        for phrase, squares in castling.items():
            if phrase in text:
                return squares

        found = self.get_squares(text)

        if len(found) == 2:
            return found[0], found[1]

        if len(found) == 1:
            print(f"only heard one square: {found[0]}")
            return None

        if len(found) > 2:
            return found[0], found[1]

        return None

    def clean(self, text):
        for word, digit in numbers.items():
            text = re.sub(rf"\b{word}\b", digit, text)
        for word, letter in letters.items():
            text = re.sub(rf"\b{word}\b", letter, text)
        return text

    def get_squares(self, text):
        found = []
        for match in pattern.finditer(text):
            file_part = match.group(1).lower()
            rank_part = match.group(2)
            file_letter = letters.get(file_part, file_part)
            if len(file_letter) != 1:
                continue
            rank_digit = numbers.get(rank_part, rank_part)
            square = f"{file_letter}{rank_digit}"
            if self.valid(square):
                found.append(square)
        return found

    def valid(self, sq):
        return len(sq) == 2 and sq[0] in "abcdefgh" and sq[1] in "12345678"

    def __del__(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.mic.terminate()
        except:
            pass