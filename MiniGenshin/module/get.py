from contextlib import contextmanager
import msvcrt

if __name__ == "__main__":
    from colors import Colors
else:
    from .colors import Colors

class GetKey():
    def __init__(self):
        self.ARROWKEYS = {b"\xe0H": "up", b"\xe0P": "down", b"\xe0M": "right", b"\xe0K": "left", b"\r": "enter"}
    
    @contextmanager
    def context(self):
        yield  # No special handling needed for Windows

    def getKey(self, withKeys: bool = False):
        with self.context():
            char = msvcrt.getch()
            if withKeys and char in {b"\xe0", b"\x00"}:  # Handle special keys
                char += msvcrt.getch()
        if withKeys:
            return self.ARROWKEYS.get(char)
        return char.decode("utf-8")

def SelectionMenu(question: str, options: list[str], wipeTerm: bool, yesNo: bool = False):
    index = 0
    possibleColors = [Colors.BLUE, Colors.PURPLE, Colors.RED, Colors.GREEN]
    while True:
        if wipeTerm:
            print("\033c", end="", flush=True)
            print(f"{Colors.CYAN}{question}{Colors.RESET}\n")
        for i, v in enumerate(options):
            if i == index:
                print(f"{Colors.RESET}> {possibleColors[i % 4]}{v}{Colors.RESET}")
            else:
                print(f"{possibleColors[i % 4]}{v}{Colors.RESET}")
        
        key = GetKey().getKey(True)
        if key == "up":
            index = index - 1 if index - 1 >= 0 else len(options) - 1
        if key == "down":
            index = index + 1 if index + 1 < len(options) else 0
        if key == "enter" and not yesNo:
            return f"{options[index].lower()}"
        if key == "enter" and yesNo:
            return index == 0
