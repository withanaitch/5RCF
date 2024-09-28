import random
from flask import Flask
from flask import render_template

app = Flask(__name__)

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        color_string = ''.join(format(i, '02x')
                               for i in [self.r, self.g, self.b])
        return color_string.upper()
    
    def get_luminance(self):
        # source: https://stackoverflow.com/a/56678483
        def linearize(channel):
            channel /= 255
            if channel <= 0.04045:
                return channel / 12.92
            else:
                return ((channel + 0.055) / 1.055) ** 2.4
            
        lr = linearize(self.r)
        lg = linearize(self.g)
        lb = linearize(self.b)

        return (0.2126 * lr + 0.7152 * lg + 0.0722 * lb)
        
    def from_bytes(color_bytes):
        return Color(color_bytes[0], color_bytes[1], color_bytes[2])
    
    def get_random_color():
        return Color.from_bytes(random.randbytes(3))

def get_text_color(bg_color: Color):
        if bg_color.get_luminance() > 0.5:
            return Color(20, 20, 20)
        else:
            return Color(255, 255, 255)

@app.route('/')
def main():
    colors = []
    for _ in range(5):
        bg = Color.get_random_color()
        fg = get_text_color(bg)
        colors.append((str(bg), str(fg)))
    return render_template('color.html', colors=colors)