from kivy import Config # type: ignore
#NOTE: config is up here because it should be the first thing that is run in the file 
Config.set('graphics', 'minimum_width', '600') 
Config.set('graphics', 'minimum_height', '400')

from kivy.app import App # type: ignore
from kivy.properties import ObjectProperty # type: ignore
from kivy.lang import Builder # type: ignore
from kivy.uix.popup import Popup # type: ignore
from plyer import filechooser # type: ignore
from kivy.core.window import Window # type: ignore
from kivy.clock import Clock # type: ignore
from kivy.uix.screenmanager import Screen, ScreenManager # type: ignore
from kivy.uix.button import Button # type: ignore
from kivy.storage.jsonstore import JsonStore # type: ignore

from pathlib import Path
from os import rename


class Mybutton(Button): # defined also here just so the python doesn't freak out and throw an error
    pass

Builder.load_file("main.kv")

class QuitPopup(Popup):
    opened: bool = False
    
    def on_open(self):
        self.opened = True
    
    def on_dismiss(self):
        self.opened = False

    def my_open(self):
        self.open() if self.opened == False else self.dismiss()


class MainScreen(Screen):
    text: str = ObjectProperty(None)
    info: str = ObjectProperty(None)
    current_file_path: Path = ObjectProperty(None)
    working_directory: Path = ObjectProperty(None)
    quit_popup = ObjectProperty(QuitPopup())

    def reset_info(self, *args):
        print("AAAAAAAAAAAA")
        self.ids.info_label.text = "..."

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if "ctrl" in modifier and codepoint == "s":
            self.save_file()
        elif "ctrl" in modifier and codepoint == "o":
            self.open_file()
        elif "ctrl" in modifier and codepoint == "q":
            self.quit_popup.my_open()

    def save_file(self):
        if self.current_file_path is None or not self.current_file_path.exists():
            self.save_as_file()
            return
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = "File has been saved successfully!"
        Clock.schedule_once(self.reset_info, 3) #FIXME: find a way for them to not behave inconsistently (some are faster than others)
    
    def open_file(self):
        filechooser.open_file(on_selection=self.selected_to_open,
                              path=str(self.working_directory) if self.working_directory is not None else "",
                              filters=[["All files", "*"], ["Supported files", "*.hdz", "*.txt"]],
                              title="Choose a file to open",
                              multiple=False)
    
    def open_directory(self):
        filechooser.choose_dir(on_selection=self.selected_to_open_dir,
                             title="select a working directory",
                             multiple=False)

    def save_as_file(self):
        filechooser.save_file(on_selection=self.selected_to_save_as,
                              title="Save as... (dont forget the file extension)",
                              path=str(self.working_directory) + "\\" + self.ids.filename_input.text,
                              multiple=False,
                              filters=[["All files"], ["Text Document", "*.txt"], ["Hadzik programming language file", "*.hdz"]])

    def selected_to_save_as(self, selection):
        if not selection:
            return
        print(selection)
        self.current_file_path = Path(selection[0])
        with open(self.current_file_path, "w") as file:
            file.write(self.text.text)
        self.ids.info_label.text = f"Saved here: {selection[0]}"
        self.ids.filename_input.text = self.current_file_path.name
        Clock.schedule_once(self.reset_info, 3)
    
    def selected_to_open(self, selection):
        if not selection:
            return
        self.current_file_path = Path(selection[0])
        with open(self.current_file_path, "r") as file:
            self.text.text = file.read()
        self.ids.filename_input.text = self.current_file_path.name
        self.ids.info_label.text = "File has been opened successfully!"
        Clock.schedule_once(self.reset_info, 3)
    
    def selected_to_open_dir(self, selection):
        if not selection:
            return
        self.working_directory = Path(selection[0])
        self.ids.directory_label.text = str(self.working_directory)

    def rename_file(self):
        if self.current_file_path is not None and self.current_file_path.exists():
            rename(self.current_file_path, str(self.current_file_path.parent) +  "\\" + self.ids.filename_input.text)
            self.ids.info_label.text = "File has been renamed successfully!"
            Clock.schedule_once(self.reset_info, 3)


class SettingsScreen(Screen):
    json_settings = JsonStore('settings.json')
    settings: dict[str, type] = {}

    def maximize_on_startup_setting(self, instance, value: bool):
        if value:
            Config.set('graphics', 'window_state', 'maximized')
            self.settings["maximize_on_startup"] = "down"
        else:
            Config.set('graphics', 'window_state', 'visible')
            self.settings["maximize_on_startup"] = "normal"
    
    def fullscreen_setting(self, instance, value: bool):
        if value:
            Window.fullscreen = "auto"
            self.settings["fullscreen"] = "down"
        else:
            Window.fullscreen = False
            self.settings["fullscreen"] = "normal"

    def fullscreen_on_startup_setting(self, instance, value: bool):
        if value:
            Config.set('graphics', 'fullscreen', 'auto')
            self.settings["fullscreen_on_startup"] = "down"
        else:
            Config.set('graphics', 'fullscreen', 0)
            self.settings["fullscreen_on_startup"] = "normal"
    
    def always_on_top_setting(self, instance, value: bool):
        if value:
            Config.set('graphics', 'always_on_top', 1)
            self.settings["always_on_top"] = "down"
        else:
            Config.set('graphics', 'always_on_top', 0)
            self.settings["always_on_top"] = "normal"

    def apply_settings(self):
        self.json_settings.put("1check", name="maximize_on_startup", value=self.settings.get("maximize_on_startup", "normal"))
        self.json_settings.put("2check", name="fullscreen", value=self.settings.get("fullscreen", "normal"))
        self.json_settings.put("3check", name="fullscreen_on_startup", value=self.settings.get("fullscreen_on_startup", "normal"))
        self.json_settings.put("4check", name="always_on_top", value=self.settings.get("always_on_top", "normal"))
        Config.write()


class RootScreenManager(ScreenManager):
    pass


class SlitherApp(App):
    text_size: int = 20
    def build(self):
        app = RootScreenManager()
        Window.bind(on_keyboard=app.ids.mainscreen.on_keyboard)
        return app


if __name__ == "__main__":
    SlitherApp().run()
