import tkinter as tk
from tkinter import font

root = tk.Tk()

# Get all available font families
available_fonts = list(font.families())

# Print them
for f in available_fonts:
    print(f)

root.mainloop()