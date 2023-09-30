from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from worker import Worker
import os
import time

class Bot(object):
    def __init__(self) -> None:
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self._configure_driver()

        self.worker = Worker(self.driver)

    def _configure_driver(self):
        # self.driver.service = Service(ChromeDriverManager().install())

        # adblocker_path = r"/Users/inakiagustin18/Desktop/5.1.1_1.crx"
        options = webdriver.ChromeOptions()
        options.user_data_dir = "/Users/inakiagustin18/Library/Application Support/Google/Chrome/Default"
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('--load-extension =' + adblocker_path)
        # options.add_extension(adblocker_path)
        options.add_argument('--disable-popup-blocking') # add when using undetected_chromedriver
        # options.add_argument('--headless=new')
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # self.driver.options = options
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
        self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}) 

    def start(self):
        self.worker.log_in("https://worker.mturk.com/")
        self.worker.select_survey()
        # self.worker.launch_chatgpt()
        for i in range(100):
            for _ in range(3):
                if self.worker.complete_ooga_survey():
                    print(f"COMPLETED SURVEY {i+1}")
                    break
                else:
                    self.worker.restart_survey()
                    print(f"FAILED SURVEY {i+1}")
            else:
                self.driver.close()
                os._exit(1)

if __name__ == "__main__":
    bot = Bot()
    t0 = time.time()
    bot.start()
    t1 = time.time()
    print("TIME:", t1-t0)