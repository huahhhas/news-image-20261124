#!/usr/bin/env python3
"""Sum up the world news of Tuesday 24 November 2026 in one image.

Pure Python 3.13 standard library: draws a 1024x1024 news poster with a
built-in 5x7 bitmap font and writes the PNG by hand (zlib + struct).
Deterministic: no randomness, no timestamps, no network.

Run: python3 main.py
Writes entry.png to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png),
then re-reads it and asserts the PNG signature, dimensions and size,
and prints its sha256.
"""

import hashlib
import os
import struct
import zlib

W, H = 1024, 1024
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

# Palette: dark navy poster, light text, one accent per story.
BG = (13, 27, 48)
PANEL = (19, 38, 66)
WHITE = (244, 242, 235)
GOLD = (212, 175, 55)
RED = (214, 69, 65)
LIGHT = (176, 190, 208)
DIVIDER = (48, 68, 96)

# 5x7 bitmap font: each glyph is 7 rows of 5 cells ('#' = on).
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}

# (kicker, headline, marker colour) — the day's six most consequential
# stories, reported 24 November 2026.
STORIES = [
    ("EUROPE - NATO",
     "NATO SENDS AWACS TO POLAND AFTER RUSSIAN MISSILES LAND",
     (212, 175, 55)),
    ("MIDDLE EAST",
     "IRAN VOWS TO DEFY US NAVAL BLOCKADE AS US SANCTIONS ITS BANKS",
     (214, 69, 65)),
    ("CLIMATE",
     "UN CLIMATE TALKS IN TURKEY COLLAPSE WITH NO FOSSIL-FUEL DEAL",
     (86, 186, 130)),
    ("UKRAINE WAR",
     "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA AS WAR SPREADS",
     (96, 165, 224)),
    ("ASIA",
     "FACTORY FIRE IN INDONESIA KILLS AT LEAST 24; RESCUERS SEARCH",
     (232, 138, 46)),
    ("TECH - BUSINESS",
     "NVIDIA REINSTATES JENSEN HUANG AS CEO; SHARES SURGE 31%",
     (178, 140, 224)),
]


class Canvas:
    """An RGB pixel buffer with rectangle and bitmap-text drawing."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def rect(self, x, y, w, h, color):
        r, g, b = color
        for yy in range(y, y + h):
            base = (yy * self.w + x) * 3
            for xx in range(w):
                i = base + xx * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def hline(self, x0, x1, y, h, color):
        self.rect(x0, y, x1 - x0, h, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT[ch]
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_centred(self, y, s, scale, color):
        x = (self.w - self.text_width(s, scale)) // 2
        self.text(x, y, s, scale, color)


def wrap(text, max_chars):
    """Greedy word wrap to lines of at most max_chars characters."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw():
    c = Canvas(W, H, BG)
    # Thin gold frame.
    c.rect(14, 14, W - 28, 3, GOLD)
    c.rect(14, H - 17, W - 28, 3, GOLD)
    c.rect(14, 14, 3, H - 28, GOLD)
    c.rect(W - 17, 14, 3, H - 28, GOLD)

    # Masthead: the day, named loud and clear.
    c.text_centred(48, "24 NOVEMBER 2026", 8, WHITE)
    c.text_centred(128, "THE WORLD IN ONE DAY", 4, GOLD)
    c.hline(64, W - 64, 176, 4, GOLD)
    c.hline(64, W - 64, 186, 2, LIGHT)

    # Six stories, one row each: coloured marker, kicker, headline.
    y = 212
    for kicker, headline, color in STORIES:
        c.rect(64, y + 4, 30, 30, color)
        c.text(112, y, kicker, 3, color)
        lines = wrap(headline, 35)
        assert len(lines) <= 2, headline
        ly = y + 30
        for ln in lines:
            c.text(112, ly, ln, 4, WHITE)
            ly += 36
        c.hline(64, W - 64, y + 110, 1, DIVIDER)
        y += 118

    # Footer: the day again, plus where it was reported.
    c.text_centred(936, "TUESDAY 24 NOVEMBER 2026", 3, GOLD)
    c.text_centred(966, "REPORTED BY REUTERS AND THE TIMES OF INDIA", 2, LIGHT)
    return c


def chunk(tag, data):
    out = tag + data
    return struct.pack(">I", len(data)) + out + struct.pack(
        ">I", zlib.crc32(out) & 0xFFFFFFFF)


def write_png(canvas, path):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    row_len = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * row_len:(y + 1) * row_len]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return png


def main():
    canvas = draw()
    os.makedirs(OUT_DIR, exist_ok=True)
    png = write_png(canvas, OUT)
    # Verify the output we just wrote.
    with open(OUT, "rb") as f:
        data = f.read()
    assert data == png
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", data[16:24])
    assert (w, h) == (W, H), f"dimensions {w}x{h}"
    assert w <= 1024 and h <= 1024, "too large"
    assert len(data) <= 1048576, f"size {len(data)} over 1 MiB"
    # Whole image: the file must end with a valid IEND chunk.
    assert data[-12:] == struct.pack(">I", 0) + b"IEND" + struct.pack(
        ">I", zlib.crc32(b"IEND") & 0xFFFFFFFF), "missing IEND"
    print(f"wrote {OUT}: {w}x{h}, {len(data)} bytes")
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
