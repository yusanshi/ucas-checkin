import os
import easyocr

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

LOGIN_URL = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
RETRY = 5


def main():
    dirname = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dirname, 'ucas-checkin.txt'), 'r') as f:
        lines = f.read().splitlines()

    data = {}
    for line in lines:
        try:
            key, value = line.split('=')
            data[key] = value
        except ValueError:
            # In case there are some more blank lines
            pass

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    )

    service = Service('/usr/lib/chromium-browser/chromedriver')
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(LOGIN_URL)

        sleep(5)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'username')))

        driver.find_element(By.ID, 'username').send_keys(data['USERNAME'])
        driver.find_element(By.ID, 'password').send_keys(data['PASSWORD'])
        if driver.find_elements(By.ID, 'validate'):
            # If has the validating code
            image = driver.find_element(By.CSS_SELECTOR,
                                        '.validate img').screenshot_as_png
            reader = easyocr.Reader(['en'])
            captcha = reader.readtext(image, detail=0,
                                      allowlist='0123456789')[0]
            print('Captcha recognized: {}'.format(captcha))
            driver.find_element(By.ID, 'validate').send_keys(captcha)

        driver.find_element(By.ID, 'login').click()

        sleep(5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, 'report-submit-btn-a24'))).click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))


def notify_myself(message):
    # TODO email, Telegram bot, etc.
    print(message)


if __name__ == '__main__':
    for i in range(RETRY):
        try:
            main()
            print('Success')
            break
        except Exception as e:
            print('Failed for {} times: {}'.format(i + 1, e))
            sleep(10 * (i + 1))
    else:
        notify_myself('Failed')
