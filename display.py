import time
from picographics import PicoGraphics, DISPLAY_SCROLL_PACK, PEN_P8
from picoscroll import PicoScroll

def scroll_message(text, speed=0.1, wdt=None):
    graphics = PicoGraphics(DISPLAY_SCROLL_PACK, pen_type=PEN_P8)
    scroll = PicoScroll()
    t = scroll.get_width()
    wrap = -graphics.measure_text(text, scale=0)

    while t > wrap:
        graphics.set_pen(0)
        graphics.clear()
        graphics.set_pen(255)
        graphics.text(text, t, 0, scale=1)
        scroll.update(graphics)
        t -= 1
        time.sleep(speed)
        if wdt:
            wdt.feed()

if __name__ == "__main__":
    scroll_message("Hello World")