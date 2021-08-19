#!/usr/bin/python3

import os

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
    options.headless = True
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              options=options)

    driver.get(LOGIN_URL)

    sleep(5)
    WebDriverWait(driver,
                  20).until(EC.presence_of_element_located(
                      (By.ID, 'username')))

    driver.find_element_by_id('username').send_keys(data['USERNAME'])
    driver.find_element_by_id('password').send_keys(data['PASSWORD'])
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
