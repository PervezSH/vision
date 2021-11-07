from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout

Builder.load_file('bottomSheetTR.kv')

class BottomSheetTR(FloatLayout):
    text = StringProperty()
    image_path = StringProperty()