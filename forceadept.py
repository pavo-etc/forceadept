from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup
from PIL import Image
import sys
import os
from time import sleep
import pathlib


url = None
scrollcount = 150
pathname = "./out"


def usage():
    print(
        """usage: forceadept.py url [scrollcount] [outputdir]""", file=sys.stderr)
    sys.exit(1)


def main():

    print(f"Reading {url}")
    driver.get(url)
    inputbox = driver.find_element(by=By.ID, value='GuestLoginForm_email')
    inputbox.send_keys('real@gmail.com')
    inputbox.send_keys(Keys.ENTER)
    print('Waiting 4 secs for login...')
    sleep(4)
    newurl = driver.current_url

    for i in range(scrollcount):
        print(f'Scrolling ({i+1}/{scrollcount})')
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

    print('Waiting 6 secs to complete load...')
    sleep(6)
    html = (driver.page_source)
    driver.close()

    soup = BeautifulSoup(html, "html.parser")
    gallery = soup.find(id="gamma-container")
    items = gallery.find_all("li")

    pathlib.Path(pathname).mkdir(parents=True, exist_ok=True)

    for i, item in enumerate(items):
        hd_url = "https:" + \
            item.img["src"].replace(
                "xlarge", "xxlarge").replace("medium", "xxlarge")
        print(f"{i}: {hd_url}")
        img_file = Image.open(requests.get(hd_url, stream=True).raw)

        img_file.save(os.path.join(pathname, f'image-{i:04}.jpg'))
        print("Saved!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    if len(sys.argv) > 1:
        url = sys.argv[1]

    if len(sys.argv) > 2:
        try:
            scrollcount = int(sys.argv[2])
        except ValueError:
            usage()

    if len(sys.argv) > 3:
        pathname = sys.argv[3]
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        main()
    except KeyboardInterrupt:
        driver.close()
