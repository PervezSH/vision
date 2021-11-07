from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout

Builder.load_file('bottomSheetWP.kv')

class BottomSheetWP(FloatLayout):
    image_path = StringProperty()