import os
import random
import tkinter as tk
from PIL import Image, ImageTk
import miniaudio

BASE = os.path.expanduser("~/.zaicy")

IMAGES = [
    os.path.join(BASE, f)
    for f in [
        "zaec1.png",
        "zaec2.png",
        "zaec3.png",
        "zaec4.png",
        "zaec.png",
    ]
]

AUDIO = os.path.join(BASE, "zaicy audio.mp3")

SPAWN_MS = 10
LIFETIME_MS = 2000
MAX_WINDOWS = 5000

def looped_stream(path):
    required = yield b""             
    while True:
        gen = miniaudio.stream_file(path)
        next(gen)                   
        while True:
            try:
                data = gen.send(required)
            except StopIteration:   
                break
            required = yield data

stream = looped_stream(AUDIO)
next(stream)                         
device = miniaudio.PlaybackDevice()
device.start(stream)

root = tk.Tk()
root.withdraw()

def quit_program(event=None):
    try:
        device.stop()
        device.close()
    finally:
        root.destroy()

root.bind_all("<Escape>", quit_program)

photos = [ImageTk.PhotoImage(Image.open(p)) for p in IMAGES]
windows = []
counter = 0

def spawn():
    global counter

    if len(windows) < MAX_WINDOWS:
        counter += 1
        photo = random.choice(photos)

        w, h = photo.width(), photo.height()
        x = random.randint(0, max(0, root.winfo_screenwidth() - w))
        y = random.randint(0, max(0, root.winfo_screenheight() - h))

        win = tk.Toplevel(root)
        win.title(f"Rabbit #{counter}")
        win.overrideredirect(True)
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.attributes("-topmost", True)

        tk.Label(win, image=photo).pack(fill="both", expand=True)
        win.image = photo

        win.bind("<Button-1>", lambda e, ww=win: ww.destroy())

        win.after(LIFETIME_MS, win.destroy)

        windows.append(win)

    root.after(SPAWN_MS, spawn)

spawn()
root.mainloop()

spawn()
root.mainloop()
