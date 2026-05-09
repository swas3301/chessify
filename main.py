import time
import json
import os
from detector import BoardDetector
from listener import VoiceListener
from executor import MoveExecutor

save_file = "calibration.json"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"


def load():
    if os.path.exists(save_file):
        with open(save_file) as f:
            data = json.load(f)
        return data["top_left"], data["bottom_right"]
    return None, None


def save(top_left, bottom_right):
    with open(save_file, "w") as f:
        json.dump({"top_left": top_left, "bottom_right": bottom_right}, f)


def main():
    print(f"""
{CYAN}╔═══════════════════════════════════════╗
║     ♟  Chess Voice Controller  ♟      ║
║   say a move and it plays on screen   ║
╚═══════════════════════════════════════╝{RESET}
""")

    detector = BoardDetector()
    listener = VoiceListener()
    executor = MoveExecutor()

    print(f"{YELLOW}opening chess.com...{RESET}")
    detector.open_browser()
    time.sleep(4)

    top_left, bottom_right = load()

    if top_left is None:
        print(f"{YELLOW}looking for board...{RESET}")
        top_left, bottom_right = detector.find_board()

        if top_left is None:
            print(f"{YELLOW}could not find board automatically{RESET}")
            top_left, bottom_right = detector.manual_setup()

        save(top_left, bottom_right)

    executor.set_board(top_left, bottom_right)

    print(f"\n{GREEN}board ready{RESET}")
    print(f"  top left:     {top_left}")
    print(f"  bottom right: {bottom_right}")
    print(f"\n{YELLOW}say 'e2 to e4' to move")
    print(f"say 'flip' to switch sides")
    print(f"say 'recalibrate' to redo board setup")
    print(f"say 'quit' to exit{RESET}\n")

    while True:
        try:
            print(f"{CYAN}listening...{RESET}")
            text = listener.listen()

            if not text:
                print(f"{RED}didn't catch that{RESET}")
                continue

            print(f"heard: '{text}'")

            if "quit" in text or "exit" in text:
                print(f"\n{GREEN}bye!{RESET}")
                break

            if "recalibrate" in text:
                top_left, bottom_right = detector.manual_setup()
                executor.set_board(top_left, bottom_right)
                save(top_left, bottom_right)
                continue

            if "flip" in text:
                executor.flip()
                side = "black" if executor.flipped else "white"
                print(f"{GREEN}switched to {side} side{RESET}")
                continue

            move = listener.parse(text)

            if not move:
                print(f"{RED}couldn't understand that as a move{RESET}")
                continue

            src, dst = move
            print(f"moving {GREEN}{src} → {dst}{RESET}")
            executor.move(src, dst)
            print(f"{GREEN}done{RESET}\n")
            time.sleep(0.5)

        except KeyboardInterrupt:
            print(f"\n{GREEN}bye!{RESET}")
            break
        except Exception as e:
            print(f"{RED}error: {e}{RESET}")


if __name__ == "__main__":
    main()