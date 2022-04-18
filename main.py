# Author: Dakota James Owen keeler
# Email:  DakotaJKeeler@protonmail.com
# Purpose: The aim of this application is to make it easier to spend and use goldback. 

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import sys
from pathlib import Path

from kivy.lang import Builder

from kivymd.app import MDApp

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["GOLDBACK_ROOT"] = sys._MEIPASS
else:
    os.environ["GOLDBACK_ROOT"] = str(Path(__file__).parent)


KV_DIR = f"{os.environ['GOLDBACK_ROOT']}/libs/kv/"

for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

KV = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import GoldbackRootScreen libs.baseclass.root_screen.GoldbackRootScreen

ScreenManager:
    transition: FadeTransition()

    GoldbackRootScreen:
        name: "Goldback root screen"
"""


class MDGoldback(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "GoldBack"
        self.icon = f"{os.environ['GOLDBACK_ROOT']}/assets/images/logo_light.png"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "100"

    def build(self):
        FONT_PATH = f"{os.environ['GOLDBACK_ROOT']}/assets/fonts/"

        self.theme_cls.font_styles.update(
            {
                "H1": [FONT_PATH + "Raleway-Light", 96, False, -1.5],
                "H2": [FONT_PATH + "Raleway-Regular", 60, False, -0.5],
                "H3": [FONT_PATH + "Raleway-SemiBold", 48, False, 0],
                "H4": [FONT_PATH + "Raleway-SemiBold", 34, False, 0.25],
                "H5": [FONT_PATH + "Raleway-SemiBold", 24, False, 0],
                "H6": [FONT_PATH + "Raleway-SemiBold", 20, False, 0.15],
                "Subtitle1": [
                    FONT_PATH + "Raleway-Medium",
                    16,
                    False,
                    0.15,
                ],
                "Subtitle2": [
                    FONT_PATH + "Raleway-SemiBold",
                    14,
                    False,
                    0.1,
                ],
                "Body1": [FONT_PATH + "Raleway-SemiBold", 16, False, 0.5],
                "Body2": [FONT_PATH + "Raleway-Regular", 14, False, 0.25],
                "Button": [FONT_PATH + "Raleway-SemiBold", 14, True, 1.25],
                "Caption": [
                    FONT_PATH + "Raleway-Medium",
                    12,
                    False,
                    0.4,
                ],
                "Overline": [
                    FONT_PATH + "Raleway-SemiBold",
                    12,
                    True,
                    1.5,
                ],
            }
        )
        return Builder.load_string(KV)


MDGoldback().run()
