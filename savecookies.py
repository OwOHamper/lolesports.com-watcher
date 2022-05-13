import pickle
from selenium import webdriver

path = 'C:\Program Files (x86)\chromedriver.exe'

options = webdriver.ChromeOptions() 
options.add_argument('log-level=3')
options.add_argument('--mute-audio')
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-extensions")
options.add_argument('--start-maximized')


driver = webdriver.Chrome(path, options=options)


def save_cookies():
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

driver.get("https://lolesports.com")
input("Login and then press enter in console")
save_cookies()