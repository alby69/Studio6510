from PySide6.QtGui import QColor

C64_PALETTE_HEX = [
    "#000000", "#FFFFFF", "#880000", "#AAFFEE",
    "#CC44CC", "#00CC55", "#0000AA", "#EEEE77",
    "#DD8855", "#664400", "#FF7777", "#333333",
    "#777777", "#AAFF66", "#0088FF", "#BBBBBB"
]

C64_PALETTE = [QColor(c) for c in C64_PALETTE_HEX]
