from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from parser import UE4Parser
from editor import Editor

class MainUI(BoxLayout):

    def load_file(self):
        self.path = "/sdcard/Download/test.uasset"  # CHANGE FILE

        with open(self.path, "rb") as f:
            raw = f.read()

        parser = UE4Parser(raw)
        self.exports = parser.parse()

        self.editor = Editor(raw, self.path)

        self.ids.rv.data = [
            {"index": str(e["index"]), "name": e["name"]}
            for e in self.exports
        ]

    def save_file(self):
        self.editor.save()

    def on_touch_down(self, touch):
        if hasattr(self, "exports") and self.exports:
            e = self.exports[0]
            self.open_editor(e["offset"])
            return True
        return super().on_touch_down(touch)

    def open_editor(self, offset):
        layout = BoxLayout(orientation='vertical')

        inp = TextInput(text="1.0")
        layout.add_widget(inp)

        def save(x):
            try:
                self.editor.write_float(offset, float(inp.text))
            except:
                pass
            popup.dismiss()

        btn = Button(text="Save")
        btn.bind(on_release=save)
        layout.add_widget(btn)

        popup = Popup(title="Edit Value", content=layout, size_hint=(0.8,0.5))
        popup.open()


class UE4App(App):
    def build(self):
        return Builder.load_file("ui.kv")


if __name__ == "__main__":
    UE4App().run()