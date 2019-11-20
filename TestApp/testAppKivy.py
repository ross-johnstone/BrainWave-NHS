from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):
    def build(self):
        def callback(instance):
            print(instance.text)

        button = Button(text='Do Something')
        button.bind(on_press=callback)
        return button


TestApp().run()