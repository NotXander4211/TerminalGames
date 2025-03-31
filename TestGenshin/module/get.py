from contextlib import contextmanager
if __name__ == "__main__":
    from colors import Colors
else:
    from .colors import Colors

class GetKey():
    def __init__(self):
        self.t = __import__("termios")
        self.tty = __import__("tty")
        self.sys = __import__("sys")
        self.ARROWKEYS = {"\x1b[A": "up", "\x1b[B": "down", "\x1b[C": "right", "\x1b[D": "left", "\n": "enter"}
    @contextmanager
    def context(self):
        fd = self.sys.stdin.fileno()
        old_settings = self.t.tcgetattr(fd)
        self.tty.setcbreak(fd)
        try:
            yield
        finally:
            self.t.tcsetattr(fd, self.t.TCSADRAIN, old_settings)
    def getKey(self, withKeys: bool = False):
        with self.context():
            if withKeys:
                char = self.sys.stdin.read(1)
                if char == "\x1b":
                    char += self.sys.stdin.read(2)
            else:
                char = self.sys.stdin.read(1)
        if withKeys:
            return self.ARROWKEYS.get(char)
            # return ord(char)
        return char



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
        # key = GetKey().getKey(True)
        key = GetKey().getKey(True)
        if key == "up":
            index = index - 1 if index - 1 >= 0 else len(options) - 1
        if key == "down":
            index = index + 1 if index + 1 < len(options) else 0
        if key == "enter" and not yesNo:
            return f"{options[index].lower()}"
        if key == "enter" and yesNo:
            if index == 0:
                return True
            return False
