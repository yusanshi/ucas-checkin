import easyocr

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

try:
    from notify import notify
except ModuleNotFoundError:

    def notify(message):
        pass


from config import CAS_USERNAME, CAS_PASSWORD

LOGIN_URL = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'


def main():
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

        driver.find_element(By.ID, 'username').send_keys(CAS_USERNAME)
        driver.find_element(By.ID, 'password').send_keys(CAS_PASSWORD)
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


if __name__ == '__main__':
    errors = []
    for i in range(5):
        try:
            main()
            print('Success')
            break
        except Exception as e:
            print(f'Failed for {i+1} times: {e}')
            errors.append(str(e))
            sleep(10 * (i + 1))
    else:
        notify('[UCAS Checkin] Failed: ' + str(list(enumerate(errors))))
