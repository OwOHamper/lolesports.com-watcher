import os


def addToStartup():
    file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = os.path.join(os.getenv('APPDATA'), R'Microsoft\Windows\Start Menu\Programs\Startup')
    with open(bat_path + '\\' + "lolesports_com_watcher.bat", "w") as bat_file:
        bat_file.write(f"cd {file_path}\n{file_path[0:2]}\npython main.py\nPAUSE")


if __name__ == '__main__':
    addToStartup()
