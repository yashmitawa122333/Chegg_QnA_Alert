import settings
import json
import sys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import send_msg


class Chegg():
    def __init__(self):
        print("Hello, Welcome to Chegg")
        self._driver = None
        self.options = Options()
        self.options.add_argument('--headless=new')

        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self._driver.get('https://expert.chegg.com/auth/login?redirectTo=https%3A%2F%2Fexpert.chegg.com%2Fauth')
        self._driver.maximize_window()
        print("Loadded the website\n")

        #Login Function
        self.login()
        time.sleep(5)
        self.get_qna_status()


    def get_cred(self):
        # check file present on path or not
        try:
            os.path.isfile(settings.CRED_DIR)
        except Exception as e:
            raise FileNotFoundError('Credentials JSON is missing.') 
            print("Creating New Credential File")
            cred={}
            print("Enter your chegg username")
            email = str(input())
            print("Enter your chegg password")
            password = str(input())
            print("Enter your email id")
            senders_mail = str(input())
            print("Enter your email password")
            senders_mail_password = str(input())
            print("Enter the recivers email id")
            receivers_mail = str(input())
            cred["email"] = email
            cred["password"]= password
            cred["senders_mail"] =  senders_mail
            cred["senders_mail_password"] =   senders_mail_password
            cred["recivers_mail"] = receivers_mail
            with open(settings.BASE_DIR+"cred.json", "+w") as f:
                json.dump(cred, f )

        with open(settings.CRED_DIR, "+r") as f:
            json_data = json.load(f)
            return json_data

    def login(self):
        data = self.get_cred()
        self._driver.find_element(By.XPATH, "//input[@name='username']").send_keys(data['email'])
        time.sleep(2)
        self._driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
        self._driver.find_element(By.XPATH, "//input[@name='password']").send_keys(data['password'])
        time.sleep(2)
        self._driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged In ..\n")
        time.sleep(20)

    def get_qna_status(self):
        # click on start solving button 
        print("Clicking on start solving button\n")
        self._driver.find_element(By.XPATH, "//button[@type='button']").click()
        time.sleep(10)

        while(True):        
            stat = {}
            print("Checking the question status")
            try :
                self._driver.find_element(By.XPATH, "//*[text()='Hello, Expert!']")
                stat['msg'] = "No Question's Available"
                stat['status'] = 0
                print(stat['msg'])

            except Exception as e:
                stat['msg'] = "Question's Available"
                stat['status'] = 1
                print("\n" + stat['msg'])
                try:
                    send_msg.send_mail(stat['msg'])
                    print('\nEmail sended to the user\n')
                except Exception as e:
                    print("\n Error in sending mail")

            # Refreshing page 
            time.sleep(180)
            self._driver.refresh()
            time.sleep(10)
            print("\n\nIf you want to exit the code press(crtl+c)\n\n")


if __name__ == '__main__':
    opt = Chegg()

