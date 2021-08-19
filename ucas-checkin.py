import os
import easyocr
import warnings

from time import sleep
from selenium import webdriver
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
        key, value = line.split('=')
        data[key] = value

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    )

    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                              options=options)

    driver.get(LOGIN_URL)

    sleep(5)
    WebDriverWait(driver,
                  20).until(EC.presence_of_element_located(
                      (By.ID, 'username')))

    driver.find_element_by_id('username').send_keys(data['USERNAME'])
    driver.find_element_by_id('password').send_keys(data['PASSWORD'])
    if driver.find_elements_by_id('validate'):
        # If has the validating code
        image = driver.find_element_by_css_selector(
            '.validate img').screenshot_as_png
        reader = easyocr.Reader(['en'])
        captcha = reader.readtext(image, detail=0, allowlist='0123456789')[0]
        print('Captcha recognized: {}'.format(captcha))
        driver.find_element_by_id('validate').send_keys(captcha)

    driver.find_element_by_id('login').click()

    sleep(5)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'report-submit-btn'))).click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))

    driver.close()


def notify_myself(message):
    # TODO email, Telegram bot, etc.
    print(message)


if __name__ == '__main__':
    # https://github.com/pytorch/pytorch/issues/54846
    # Suppress the annoying warning
    warnings.filterwarnings('ignore', category=UserWarning)
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
