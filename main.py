import pickle
import schedule
from selenium import webdriver
import time
from datetime import datetime
import ctypes
import systray
import os
from threading import Thread

path = 'C:\Program Files (x86)\chromedriver.exe'

options = webdriver.ChromeOptions() 
options.add_argument('log-level=3')
options.add_argument('--mute-audio')
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-extensions")
options.add_argument('--start-maximized')
options.add_argument('--autoplay-policy=no-user-gesture-required')




driver = webdriver.Chrome(path, options=options)


def save_cookies():
    driver.get("https://lolesports.com")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

def load_cookies():
    for cookie in pickle.load( open("cookies.pkl", "rb") ):
        driver.add_cookie(cookie)


def open_in_new_tab(url):
    driver.execute_script(f'window.open("{url}","_blank");')


def open_stream(url):
    open_in_new_tab(url)
    

def accept_cookies_f():
    a = driver.find_element_by_css_selector(".osano-cm-save.osano-cm-buttons__button.osano-cm-button.osano-cm-button--type_save")
    a.click()


def streams_watcher(accept_cookies=False):
    try:
        streams = 0
        driver.get("https://lolesports.com/schedule")
        if accept_cookies:
            accept_cookies_f()
        load_cookies()
        driver.implicitly_wait(10)
        matches = driver.find_elements_by_class_name('EventMatch')
        for match in matches:
            child_element = match.find_element_by_css_selector("*")
            if child_element.tag_name == "a":
                stream_link = child_element.get_attribute("href")
                #prevents opening vods
                if "live" in stream_link:
                    streams += 1
                    print("Opened stream " + stream_link)
                    open_stream(stream_link)
                    # option_select()
                    time.sleep(15)
        if streams == 0:
            print("No streams found")
        print()
    except Exception as e:
        print("Error")
        print(e)
        streams_watcher()
            


def take_screenshots():
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        time.sleep(2)
        now = datetime.now().strftime('%m-%d_%H-%M-%S')
        driver.save_screenshot(f'screenshots/screenshot-{now}.png')
        

def close_tabs():
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

def job():
    take_screenshots()
    close_tabs()
    streams_watcher()


def setup():
    global tray
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(handle, 0)
    tray = systray.Systray(handle, driver)
    tray.closed = True
    os.system("cls")


    trayT = Thread(target=tray.loop)
    trayT.start()

schedule.every().hour.at(":05").do(job)


setup()
streams_watcher(accept_cookies=True)
take_screenshots()
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        tray.exit()