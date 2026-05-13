from manim import *

BG = "#0B0B0B"
PRIMARY = "#E10600"
SECONDARY = "#FF6A00"
ACCENT = "#FFC400"

class Intro(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("Vídeo Explicativo", color=PRIMARY, font_size=56)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)
