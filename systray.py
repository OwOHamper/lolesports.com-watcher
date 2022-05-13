import pystray
from pystray import MenuItem as item
from PIL import Image
import ctypes
import os
import subprocess
import webbrowser

class Systray():
    def __init__(self, handle, driver):
        self.handle = handle
        self.closed = False
        self.driver = driver


    def load_image(self):
        with Image.open("assets/icon.ico") as img:
            return img

    def on_clicked(self):
        self.closed = not self.closed
        if self.closed:
            ctypes.windll.user32.ShowWindow(self.handle, 0)
        else:
            ctypes.windll.user32.ShowWindow(self.handle, 1)


    def exit(self):
        print("Exiting program...")
        self.driver.quit()
        os._exit(1)

    def open_screenshots(self):
        subprocess.Popen('explorer /select, "' + os.getcwd() + '\screenshots"')

    def loop(self):
        try:
            menu = pystray.Menu(
                    item('Show/Hide window', lambda:  self.on_clicked()),
                    item('Open screenshot folder', lambda:  self.open_screenshots()),
                    item('Github', lambda:  self.github()),
                    item('Quit', lambda:  self.exit())
            )


            self.icon = pystray.Icon('lolesports.com watcher', self.load_image(), menu=menu)

            self.icon.run()
        except KeyboardInterrupt:
            self.exit()

    def github(self):
        webbrowser.open("https://github.com/OwOHamper/lolesports.com-watcher")



