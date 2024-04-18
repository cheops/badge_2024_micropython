from fri3d.badge import display, colors

def center_text(text):
    """clear display and show white text centered on black background"""
    display.fill(colors.BLACK)
    length =  len(text) if isinstance(text, str) else len(str(text))
    display.text(
        font,
        text,
        display.width() // 2 - length // 2 * font.WIDTH,
        display.height() // 2 - font.HEIGHT // 2,
    )
    display.show()
