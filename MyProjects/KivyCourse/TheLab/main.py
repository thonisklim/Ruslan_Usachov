from kivy.app import App
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.graphics import *
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.uix.tabbedpanel import TabbedPanel


class ExampleTabWindow(MDApp):
    def build(self):
        return Builder.load_file("TheLab.kv")


class Tab(FloatLayout, MDTabsBase):
    pass


class WidgetExample(GridLayout):
    toggle_on_state = BooleanProperty(False)
    count = 0
    my_text = StringProperty("Hello!")
    text_input_str = StringProperty("foo!")

    def on_button_click(self):
        # print("Button clicked")
        if self.toggle_on_state:
            self.count += 1
            self.my_text = f"{self.count}"

    def on_toggle_button_state(self, widget):
        print("toggle state:" + widget.state)
        if widget.state == "normal":
            widget.text = "OFF"
            self.toggle_on_state = False
        else:
            widget.text = "ON"
            self.toggle_on_state = True

    def on_switch_active(self, widget):
        print("Switch: " + str(widget.active))

    def on_slider_value(self, widget):
        self.slider_value_txt = str(int(widget.value))

    def on_text_validate(self, widget):
        self.text_input_str = widget.text


class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "lr-tb"
        for i in range(100):
            # bsize = dp(100) + i*10
            bsize = dp(100)
            b = Button(text=str(i+1), size_hint=(None, None), size=(bsize, bsize))
            self.add_widget(b)


# class GridLayoutExample(GridLayout):
#     pass


class AnchorLayoutExample(AnchorLayout):
    pass


class BoxLayoutExample(BoxLayout):
    pass
    '''def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        b1 = Button(text="A")
        b2 = Button(text="B")
        b3 = Button(text="C")
        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)'''


class MainWidget(Widget):
    pass


class TheLabApp(App):
    pass


class CanvasExample1(Widget):
    pass


class CanvasExample2(Widget):
    pass


class CanvasExample3(Widget):
    pass


class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100, 100, 450, 900), width=2)
            Color(0, 1, 0)
            Line(circle=(300, 100, 100), width=2)
            Line(rectangle=(500, 100, 100, 200), width=2)
            self.rect = Rectangle(pos=(600, 200), size=(100, 50))

    def on_button_press (self):
        x, y = self.rect.pos
        w, h = self.rect.size
        inc = dp(10)

        diff = self.width - (x + w)
        if diff < inc:
            inc = diff

        x += inc
        self.rect.pos = (x, y)


class CanvasExample5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        self.vx = dp(3)
        self.vy = dp(4)
        with self.canvas:
            self.ball = Ellipse(pos=(100, 100), size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update, 1/60)

    def on_size (self, *args):
        print("on size: " + str(self.width) + ", " + str(self.height))
        self.ball.pos = (self.center_x - self.ball_size/2, self.center_y - self.ball_size/2)

    def update(self, dt):
        # print("update")
        x, y = self.ball.pos
        sh = self.height
        sw = self.width

        if x < 0 or x + self.ball_size > sw:
            self.vx *= -1
        elif y < 0 or y + self.ball_size > sh:
            self.vy *= -1

        self.ball.pos = (x+self.vx, y+self.vy)


TheLabApp().run()
