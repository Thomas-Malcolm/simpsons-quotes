#!/usr/bin/env python

"""
Takes raw quotes and fuzzy searches them on Frinkiac. Uses this to confirm season/episode, and downloads a frame from
the episode
"""

from typing import Tuple

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from textwrap import wrap
import time
import sys

FRINKIAC = "https://frinkiac.com/?q={}"
MEME_CHAR_WIDTH = 28

"""
Get the season, episode, and image url. If these are (None, None, None), then assume the quote couldn't be found.
"""
def get_quote_deets(browser: webdriver, quote: str) -> Tuple[int, int, str]:

    browser.get(FRINKIAC.format(quote))

    # Check if quote fonud
    main_el = browser.find_element(By.CLASS_NAME, "main")
    if "Nothing found" in main_el.text:
        return (None, None, None)
    
    # Navigate to scene with quote
    first_el = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]")
    first_el.click()

    time.sleep(5) # wait for the browser to catch up 

    episode_el = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div[2]/div/div[2]/div[1]/p")
    quotes_el = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div[2]/div/div[3]") # not needed
    img_el = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div[1]/div/div/a/img")

    episode = episode_el.text.split('(')[0].split('/')
    season, episode = episode[0].split(' ')[1], episode[1].strip().split(' ')[1]

    img_url = img_el.get_attribute("src")

    return (season, episode, img_url)

if __name__ == "__main__":

    quote = sys.argv[1]

    options = Options()
    # options.add_argument("--headless") # commented out for debugging
    browser = webdriver.Firefox(options = options)

    season, episode, img_url = get_quote_deets(browser, quote)

    open(f"s{season}-e{episode}-{img_url.split('/')[-1]}", "wb").write(requests.get(img_url).content)

    print("Season:", season)
    print("Episode:", episode)
    print("img url:", img_url)

    meme_btn = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div[2]/div/div[4]/div[1]/button")
    meme_btn.click()
    time.sleep(2)

    meme_text = browser.find_element(By.XPATH, "//*[@id=\"meme-text\"]")
    meme_text.clear()
    meme_happy_quote = "\n".join(wrap(quote, MEME_CHAR_WIDTH))
    meme_text.send_keys(meme_happy_quote)
    time.sleep(0.5)

    meme_img_el = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div[1]/div/a/img")
    meme_img_url = meme_img_el.get_attribute("src")

    open(f"s{season}-e{episode}-meme-{img_url.split('/')[-1]}", "wb").write(requests.get(meme_img_url).content)


    