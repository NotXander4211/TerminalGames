from module import getKey, selectionMenu

bold = "\033[1m"

x = selectionMenu("Yes Or No: ", ["Yes", "No"], True, True)
y = selectionMenu("Which One?", ["This", "That", "There", "Here"], True)
print(x, f"-{type(x)}")
print(y, f"-{type(y)}")
