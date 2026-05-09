import requests
import zipfile
import io
import os

url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
folder = "vosk-model"

if os.path.exists(folder):
    print("model already downloaded")
else:
    print("downloading vosk model 50mb...")
    res = requests.get(url, stream=True)
    total = int(res.headers.get("content-length", 0))
    received = 0
    data = []

    for chunk in res.iter_content(chunk_size=8192):
        data.append(chunk)
        received += len(chunk)
        percent = int(received / total * 100) if total else 0
        print(f"  {percent}%", end="\r")

    print("\nextracting...")
    z = zipfile.ZipFile(io.BytesIO(b"".join(data)))
    z.extractall(".")

    extracted = [f for f in os.listdir(".") if f.startswith("vosk-model")][0]
    os.rename(extracted, folder)
    print(f"done. saved to ./{folder}")