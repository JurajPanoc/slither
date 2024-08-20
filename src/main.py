from kivy.app import App # type: ignore
from kivy.uix.widget import Widget # type: ignore
from kivy.properties import ObjectProperty # type: ignore
from kivy.lang import Builder # type: ignore
from kivy.uix.dropdown import DropDown # type: ignore
from plyer import filechooser # type: ignore
from kivy.core.window import Window # type: ignore
from os.path import exists


Builder.load_file("main.kv")


class SlLayout(Widget): 
    text = ObjectProperty(None)
    info = ObjectProperty(None)
    current_file_path = ObjectProperty(None)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if "ctrl" in modifier and codepoint == "s":
            self.save_file()
        elif "ctrl" in modifier and codepoint == "o":
            self.open_file()
        elif "ctrl" in modifier and codepoint == "q":
            self.quit_program() #TODO: figure out how to trigger a popup from kv file here

    def reset_info_label(self, dt):
        self.ids.info_label.text = "..."

    def save_file(self):
        if self.current_file_path is None or not exists(self.current_file_path):
            self.save_as_file()
            return
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = "File has been successfully saved!"
    
    def open_file(self):
        filechooser.open_file(on_selection=self.selected_to_open, 
                              filters=[["Supported files", "*.hdz", "*.txt"]],
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
        self.current_file_path = selection[0]
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = f"File saved successfully: {selection[0]}"
    
    def selected_to_open(self, selection):
        if not selection:
            return
        self.current_file_path = selection[0]
        with open(self.current_file_path, "r") as file:
            self.text.text = file.read()
        self.ids.info_label.text = f"{selection[0].split("\\")[-1]}"

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
