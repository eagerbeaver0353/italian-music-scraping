from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException, ElementNotInteractableException
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

target_url = "https://www.spotontrack.com/"
target_url_login = "https://www.spotontrack.com/login"

soundcharts_url = "https://app.soundcharts.com/"
soundcharts_url_login = "https://app.soundcharts.com/login"

email = os.getenv("ACCOUNT_EMAIL")
password = os.getenv("ACCOUNT_PWD")

soundcharts_email = os.getenv("SOUNDCHARTS_ACCOUNT_EMAIL")
soundcharts_password = os.getenv("SOUNDCHARTS_ACCOUNT_PWD")

class Driver:
    def __init__(self):
        self.createBrowser()
    
    def createBrowser(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1280,800")
        self.driver = webdriver.Chrome(ChromeDriverManager(latest_release_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip").install(), options=chrome_options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        print("Loading Page ...")
        # self.driver.get(target_url)
        print("--------Ready------")
        self.status = 'ready'
        self.response = None

    def is_available(self):
        return self.status == 'ready'
    
    def reload_page(self):
        try:
            self.driver.get(target_url)
        except Exception:
            return
        
    def login(self):
        try:
            self.driver.get(target_url_login)
            # WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, "//input[@name=\"email\"]"))
            self.driver.find_element(By.XPATH, "//input[@name=\"email\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@name=\"email\"]").send_keys(email)
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//input[@name=\"password\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@name=\"password\"]").send_keys(password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//button[text()=\"Login\"]').click()
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in login process")
            print(err)

    def do_login(self):
        self.status = 'busy'
        threading.Thread(target=self.login, args=()).start()

    # get Spotify Charts
    def get_charts_spotify_execute(self, country_id, charts_date, date_type):
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]'))
            self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'Spotify\']').click()
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[3]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\''+date_type+'\']').click()
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[4]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'' + country_id + '\']').click()
            if charts_date is not None:
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').clear()
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').send_keys(charts_date + Keys.ENTER)
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get spotify charts")
            print(err)

    def get_charts_spotify(self, country_id, charts_date, date_type="Daily"):
        self.status = 'busy'
        threading.Thread(target=self.get_charts_spotify_execute, args=(country_id, charts_date, date_type)).start()

    # get TikTok Charts
    def get_charts_tiktok_execute(self, country_id, charts_date, date_type):
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]'))
            self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'TikTok\']').click()
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[2]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\''+date_type+'\']').click()
            if charts_date is not None:
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').clear()
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').send_keys(charts_date + Keys.ENTER)
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get tiktok charts")
            print(err)

    def get_charts_tiktok(self, country_id, charts_date, date_type="Daily"):
        self.status = 'busy'
        threading.Thread(target=self.get_charts_tiktok_execute, args=(country_id, charts_date, date_type)).start()

    # get Shazam Charts
    def get_charts_shazam_execute(self, country_id, charts_date):
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]'))
            self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'Shazam\']').click()
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[3]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'' + country_id + '\']').click()
            if charts_date is not None:
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').clear()
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').send_keys(charts_date + Keys.ENTER)
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get shazam charts")
            print(err)

    def get_charts_shazam(self, country_id, charts_date):
        self.status = 'busy'
        threading.Thread(target=self.get_charts_shazam_execute, args=(country_id, charts_date)).start()

    # get Shazam Charts
    def get_charts_radio_execute(self, country_id, charts_date):
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]'))
            self.driver.find_element(By.XPATH, '//header//nav//ul/li/a[contains(text(), \"Charts\")]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'Radio\']').click()
            self.driver.find_element(By.XPATH, '//section[2]/div/div/div[2]/button').click()
            self.driver.find_element(By.XPATH, '//section[2]//a[@class=\'dropdown-item\'][normalize-space()=\'' + country_id + '\']').click()
            if charts_date is not None:
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').clear()
                self.driver.find_element(By.XPATH, '//section[2]//input[@id=\'datepicker-chart\']').send_keys(charts_date + Keys.ENTER)
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get shazam charts")
            print(err)

    def get_charts_radio(self, country_id, charts_date):
        self.status = 'busy'
        threading.Thread(target=self.get_charts_radio_execute, args=(country_id, charts_date)).start()

    # soundcharts
    def login_soundcharts(self):
        try:
            self.driver.get(soundcharts_url_login)
            # WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, "//input[@name=\"email\"]"))
            self.driver.find_element(By.XPATH, "//input[@name=\"email\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@name=\"email\"]").send_keys(soundcharts_email)
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//input[@name=\"password\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@name=\"password\"]").send_keys(soundcharts_password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//button[text()=\"Log in\"]').click()
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in login process")
            print(err)

    def do_login_soundcharts(self):
        self.status = 'busy'
        threading.Thread(target=self.login_soundcharts, args=()).start()

    def get_charts_youtube_soundcharts_execute(self, country_id, charts_date):
        print(country_id)
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//a[@title=\'Charts\']//span[normalize-space()=\'Charts\']'))
            self.driver.find_element(By.XPATH, '//a[@title=\'Charts\']//span[normalize-space()=\'Charts\']').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '(//button[@role=\'button\'])[1]').click()
            self.driver.find_element(By.XPATH, '//div[@id=\'id-youtube\']').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '(//button[@role=\'button\'])[3]').click()
            self.driver.find_element(By.XPATH, '//div[@title=\'' + country_id + '\']').click()
            time.sleep(5)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get youtube charts")
            print(err)

    def get_charts_youtube_soundcharts(self, country_id, charts_date):
        self.status = 'busy'
        threading.Thread(target=self.get_charts_youtube_soundcharts_execute, args=(country_id, charts_date)).start()
    
    def execute(self, task, url=None):
        try:
            if task == 'get_page' and url:
                # check if the element exist
                elements = self.driver.find_elements(By.XPATH, '//input[@id="searchboxinput"]')
                if len(elements) == 0:
                    # close
                    self.reload_page()
                else:
                    self.driver.find_element(By.XPATH, '//input[@id="searchboxinput"]').clear()
                    self.driver.find_element(By.XPATH, '//input[@id="searchboxinput"]').send_keys(url)
                    self.driver.find_element(By.XPATH, '//button[@id="searchbox-searchbutton"]').click()
                    time.sleep(4)
                    self.response = self.driver.page_source
            self.status = 'ready'
        except NoSuchElementException:
            # handle the exception
            print("Element not found")
            self.reload_page()
        except ElementNotInteractableException:
            self.reload_page()
        except InvalidSessionIdException:
            self.createBrowser()

    def get_page(self, url):
        self.status = 'busy'
        threading.Thread(target=self.execute, args=('get_page', url)).start()

    def has_response(self):
        return self.response is not None
    
    def get_response(self):
        if self.status == 'ready':
            result = self.response
            self.response = None
            return result
    
    def release(self):
        self.response = None
        self.status = 'ready'