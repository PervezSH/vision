from kivy import utils
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import cv2
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDIconButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.label import MDLabel


class MainScreen(Screen):
    pass

class MainScreenManager(ScreenManager):
    screen_stack = []
    header_text = StringProperty()

    options = {
        'Warp Perspective': 'perspective-less',
        'Recognize Text': 'text-recognition',
        'Measure': 'tape-measure',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def push(self, screen_name):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "up"
            self.current = screen_name

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "down"
            self.current = screen_name

    def start_button_clicked(self):
        self.image_per_frame = Image(allow_stretch=True)
        self.header_text = 'Measure'
    #adding screen
        screen_layout = MainScreen(name='main_screen')
        self.add_widget(screen_layout)
    #displaying cam feed
        screen_layout.add_widget(self.image_per_frame)
    #capture button
        screen_layout.add_widget(MDIconButton(icon="camera-iris",
                                              pos_hint={"center_x": .5, "center_y": .1},
                                              user_font_size="45sp",
                                              theme_text_color="Custom",
                                              text_color= utils.get_color_from_hex('CEDFF0')))

    #select from gallery button
        screen_layout.add_widget(MDIconButton(icon='camera-burst',
                                              pos_hint={"center_x": .15, "center_y": .1},
                                              user_font_size="30sp",
                                              theme_text_color="Custom",
                                              text_color=utils.get_color_from_hex('CEDFF0')
                                              ))
    #Floating Speed dial button
        speed_dial = MDFloatingActionButtonSpeedDial(callback= self.callback)
        speed_dial.data = self.options
        speed_dial.root_button_anim = True
        screen_layout.add_widget(speed_dial)
    #video capture
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1 / 60)
    #Adding Border
        screen_layout.add_widget(Image(source='ui/Border.png',
                                       allow_stretch=True,
                                       keep_ratio=False))
    #Flash Light Button
        flash_button = MDIconButton(icon='flash-off',
                                    pos_hint={"center_x": .1, "center_y": .95},
                                    user_font_size="20sp",
                                    theme_text_color="Custom",
                                    text_color=utils.get_color_from_hex('CEDFF0')
                                    )
        screen_layout.add_widget(flash_button)
        self.ids['my_flash_button'] = flash_button
        flash_button.bind(on_press= self.flash_button_pressed)
    #Close Button
        close_button = MDIconButton(icon='close',
                                    pos_hint={"center_x": .9, "center_y": .95},
                                    user_font_size="20sp",
                                    theme_text_color="Custom",
                                    text_color=utils.get_color_from_hex('CEDFF0'))
        screen_layout.add_widget(close_button)
        close_button.bind(on_press= self.close_button_clicked)
    #Header
        header_label = MDLabel(text=self.header_text,
                               halign="center",
                               font_style='Quicksand',
                               pos_hint={"center_y": .90})
        screen_layout.add_widget(header_label)
        self.ids['my_header_label'] = header_label

    def flash_button_pressed(self, value):
        if self.ids.my_flash_button.icon == 'flash-off':
            self.ids.my_flash_button.icon = 'flash'
        else:
            self.ids.my_flash_button.icon = 'flash-off'

    def close_button_clicked(self, value):
        MDApp.get_running_app().stop()

    def callback(self, instance):
        if instance.icon == 'tape-measure':
            self.header_text = 'Measure'
        elif instance.icon == 'text-recognition':
            self.header_text = 'Recognize Text'
        elif instance.icon == 'perspective-less':
            self.header_text = 'Warp Perspective'

        self.ids.my_header_label.text = self.header_text

    def update(self, a):
        self.load_video()

    def load_video(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt= 'ubyte')
        self.image_per_frame.texture = texture


class OTDRSystem(MDApp):
    manager = ObjectProperty(None)
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "50"
        # Adding Custom Font
        LabelBase.register(name='Quicksand',
                           fn_regular='fonts/Quicksand-Regular.ttf')
        theme_font_styles.append('Quicksand')
        self.theme_cls.font_styles['Quicksand'] = ['Quicksand',
                                                   16,
                                                   False,
                                                   0.15, ]
        self.manager = MainScreenManager()

        return  self.manager

OTDRSystem().run()