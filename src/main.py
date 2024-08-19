from kivy.app import App # type: ignore
from kivy.uix.widget import Widget # type: ignore
from kivy.properties import ObjectProperty # type: ignore
from kivy.lang import Builder # type: ignore
from kivy.uix.dropdown import DropDown # type: ignore
from plyer import filechooser # type: ignore
from kivy.core.window import Window # type: ignore


Builder.load_file("main.kv")


class SlLayout(Widget):
    text = ObjectProperty(None)
    info = ObjectProperty("Hello")
    current_file_path = ObjectProperty(None)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if 'ctrl' in modifier and codepoint == 's':
            self.save_button()

    def save_button(self):
        if self.current_file_path is None:
            self.ids.info_label.text = "This file doesn't exist"
            return
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = "File has been successfully saved!"
    
    def open_button(self):
        filechooser.open_file(on_selection=self.selected, 
                              filters=[["Supported files", "*.hdz", "*.txt"]],
                              title="Choose a file to open")
    
    def selected(self, selection):
        if not selection:
            return
        self.current_file_path = selection[0]
        with open(self.current_file_path, "r") as file:
            self.text.text = file.read()
        self.ids.info_label.text = f"Current file: {selection[0].split("\\")[-1]}"

    def file_button(self):
        file_content = self.text.text
        print(file_content)


class SlitherApp(App):
    def build(self):
        app = SlLayout()
        Window.bind(on_keyboard=app.on_keyboard)
        return app


if __name__ == "__main__":
    SlitherApp().run()
