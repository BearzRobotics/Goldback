from os import environ

from kivy.properties import StringProperty
from kivy.uix.image import Image

from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class GoldbackRootScreen(ThemableBehavior, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _late_init(self, i):
        self.image = Image(
            source=f"{environ['GOLDBACK_ROOT']}/assets/images/logo_light.png",
            size_hint=(None, None),
            size=("40dp", "40dp"),
        )



class GoldbackListItem(ThemableBehavior, MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    image = StringProperty()
