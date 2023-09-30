from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from random import randrange
from plyer import notification
import os
import sys

class Worker(object):
    def __init__(self, driver) -> None:
        self.driver = driver
        self.email = "inakiagustin18@gmail.com"
        self.password = "Ateneodemanila08"
        self.rank = 2
        self.survey_xpath = f"//*[@id=\"MainContent\"]/div[4]/div/div/ol/li[{self.rank + 1}]/div[1]/span[6]/span/span/a[1]"

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element("xpath", xpath)
        except Exception:
            return False
        return True

    def log_in(self, webpage):
        self.driver.get(webpage)
        self.driver.find_element("xpath", "//*[@id=\"ap_email\"]").send_keys(self.email)
        sleep(2)
        self.driver.find_element("xpath", "//*[@id=\"ap_password\"]").send_keys(self.password)
        sleep(2)
        self.driver.find_element("xpath", "//*[@id=\"signInSubmit\"]").click()
        sleep(2)
    
    def select_survey(self):
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"MainContent\"]/div[5]/div/div/div/nav/ul/li[3]/a"))).click()
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"MainContent\"]/div[5]/div/div/div/nav/ul/li[4]/a"))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.survey_xpath))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/div/label/input"))).click()

    def restart_survey(self):
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/nav/div/div/div/div/form/button"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/nav/div/div[1]/div/div[3]/span/span/button"))).click()

    def complete_james_billings_survey(self):
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        sleep(1)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Start Task']"))).click()
        except Exception:
            if self.driver.find_element("xpath", "//*[text()='No Surveys available...']"):
                print("NO SURVEYS AVAILABLE")
            self.driver.close()
            os._exit(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(3)
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        sleep(2)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Bad Task']"))).click()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Technical Error']"))).click()
        except Exception:
            return False

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Attempt Complete']")))
        sleep(1)
        try:
            self.driver.find_element("xpath", "//*[@id=\"monitor-finish\"]").click()
        except Exception:
            pass
        
        sleep(1)
        return True

    def complete_ooga_survey(self):
        self.check_robot_notification()
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        # clicks "Surveys" button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/div[5]/div[1]/div/div[1]/a"))).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        # clicks "Best Value" option
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"surveys\"]/div[2]/a[1]"))).click()
        
        # checks if there are no surveys currently available
        for _ in range(3):
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Unavailable']")))
                sleep(3)
                self.driver.refresh()
            except Exception:
                break
        else:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return False

        # waits until the title of the page is "Return | Ooga"
        while self.driver.title != "Return | Ooga":
            pass
        
        # returns to main window and clicks the "Submit HIT" button
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"assignment_form\"]/a"))).click()
        sleep(3)

        # closes survey tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()

        # returns to main window
        self.driver.switch_to.window(self.driver.window_handles[0])
        return True

    def complete_brego_survey(self):
        price = randrange(500, 5000)
        sleep(3)
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"input-1\"]/input"))).send_keys(price)
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/crowd-form/form/crowd-button"))).click()

    def complete_avey_survey(self, survey_num):
        self.check_robot_notification()
        try:
            self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))
        except Exception:
            return False
        
        query = self.driver.find_element("xpath", "/html/body/div").text
        query = query.replace('\n', ' ')
        query = "YOUR RESPONSE FOR THIS PROMPT SHOULD FOLLOW THIS FORMAT: \"Doctor, I am experiencing [SYMPTOM].\" " + query

        self.driver.switch_to.window(self.driver.window_handles[1])
        response = self.get_chatgpt_answer(query, survey_num*2)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(self.driver.find_element("xpath", "//*[@id=\"MainContent\"]/div[3]/div/div[1]/iframe"))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/crowd-form/form/div/crowd-text-area"))).send_keys(response)
        sleep(1.5)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/crowd-form/form/crowd-button"))).click()
        except Exception:
            return False
        sleep(1.5)
        return True
    
    def launch_chatgpt(self):
        self.driver.execute_script("window.open('https://chat.openai.com/auth/login', 'new_window')")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.find_element("xpath", "//*[@id=\"__next\"]/div[1]/div[1]/div[4]/button[1]").click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/div/div/div/div[4]/form[2]/button"))).click()
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"identifierId\"]"))).send_keys(self.email)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"identifierNext\"]/div/button"))).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"password\"]/div[1]/div/div[1]/input"))).send_keys(self.password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"passwordNext\"]/div/button"))).click()
        
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"__next\"]/div[1]/div[2]/div/main/div[2]/form/div/div[2]")))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"radix-:re:\"]/div[2]/div/div[2]/button"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"radix-:re:\"]/div[2]/div/div[2]/button[2]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Done']"))).click()

        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def get_chatgpt_answer(self, query, response_num):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"prompt-textarea\"]"))).send_keys(query)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"__next\"]/div[1]/div[2]/div/main/div[2]/form/div/div[2]/button"))).click()
        sleep(5)
        response = self.driver.find_element("xpath", f"//*[@id=\"__next\"]/div[1]/div[2]/div/main/div[1]/div/div/div/div[{response_num}]").text
        return response

    def check_robot_notification(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Human or Robot?']")))
            try:
                self.notify_user()
                WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Human or Robot?']")))
            except Exception:
                os._exit(1)
        except Exception:
            pass

    @staticmethod
    def notify_user():
        while True:
            sleep(3)
            notification.notify(
                title = "'Human or Robot?' Notification "+ sys.argv[0],
                message = "ANSWER!",
            )
            sleep(5)
            break