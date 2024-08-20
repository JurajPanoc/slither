#NOTE: config is up here because it should be the first thing that is run in the file 
from kivy import Config # type: ignore
Config.set('graphics', 'minimum_width', '600') 
Config.set('graphics', 'minimum_height', '400')

from kivy.app import App # type: ignore
from kivy.uix.widget import Widget # type: ignore
from kivy.properties import ObjectProperty # type: ignore
from kivy.lang import Builder # type: ignore
from kivy.uix.popup import Popup # type: ignore
from plyer import filechooser # type: ignore
from kivy.core.window import Window # type: ignore

from pathlib import Path
from os import rename


Builder.load_file("main.kv")


class QuitPopup(Popup): # defined also here just so the python doesn't freak out and throw an error
    pass


class SlLayout(Widget): 
    text = ObjectProperty(None)
    info = ObjectProperty(None)
    current_file_path: Path = ObjectProperty(None)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if "ctrl" in modifier and codepoint == "s":
            self.save_file()
        elif "ctrl" in modifier and codepoint == "o":
            self.open_file()
        elif "ctrl" in modifier and codepoint == "q":
            QuitPopup().open()

    def save_file(self):
        if self.current_file_path is None or not self.current_file_path.exists():
            self.save_as_file()
            return
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = "File has been saved successfully!"
    
    def open_file(self):
        filechooser.open_file(on_selection=self.selected_to_open, 
                              filters=[["All files", "*"], ["Supported files", "*.hdz", "*.txt"]],
                              title="Choose a file to open",
                              multiple=False)
    
    def save_as_file(self):
        filechooser.save_file(on_selection=self.selected_to_save_as,
                              title="Save as... (dont forget the file extension)",
                              multiple=False,
                              filters=[["All files"], ["Text Document", "*.txt"], ["Hadzik programming language file", "*.hdz"]]) #FIXME:for some reason doesn't actually give the selected type to the file

    def selected_to_save_as(self, selection):
        if not selection:
            return
        self.current_file_path = Path(selection[0])
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = f"Saved here: {selection[0]}"
        self.ids.filename_input.text = self.current_file_path.name
    
    def selected_to_open(self, selection):
        if not selection:
            return
        self.current_file_path = Path(selection[0])
        with open(self.current_file_path, "r") as file:
            self.text.text = file.read()
        self.ids.filename_input.text = self.current_file_path.name
        self.ids.info_label.text = "File has been opened successfully!"

    def rename_file(self):
        if self.current_file_path is None or not self.current_file_path.exists():
            self.save_as_file()
        else:
            print("renamed", self.current_file_path, str(self.current_file_path.parent) +  "\\" + self.ids.filename_input.text)
            rename(self.current_file_path, str(self.current_file_path.parent) +  "\\" + self.ids.filename_input.text)
            self.ids.info_label.text = "File has been renamed successfully!"

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
