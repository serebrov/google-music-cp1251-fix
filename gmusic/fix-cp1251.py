#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from selenium import webdriver

SELENIUM_SERVER = "http://127.0.0.1:4444/wd/hub"
GOOGLE_MUSIC_URL = "http://music.google.com/"
LOGIN_EMAIL = "seb.goo@gmail.com"
LOGIN_PASSWORD = "xxx"
WAIT_TIME=3

def processSong(song):
    song.find_element_by_class_name("fade-out-with-menu").click()
    selenium.find_element_by_id(":c").click()
    dialog = selenium.find_element_by_id("edit-song-info")
    processField(dialog.find_element_by_id("edit-name"))
    processField(dialog.find_element_by_id("edit-song-artist"))
    processField(dialog.find_element_by_id("edit-album-artist"))
    processField(dialog.find_element_by_id("edit-album"))
    processField(dialog.find_element_by_id("edit-composer"))
    processField(dialog.find_element_by_id("edit-name"))
    processField(dialog.find_element_by_id("edit-name"))
    dialog.find_element_by_class_name("modal-dialog-buttons").find_element_by_tag_name("button").click()

def processField(field):
    try:
        value = field.value.decode('cp1251')
        field.clear()
        field.send_keys(value)
    except:
        pass

#out = open("not-bug.txt", "w")
#for line in ( open ('bug.txt','r')):
#    try:
#        out.write(line.decode('cp1251'))
#    except:
#        out.write(line)

selenium = webdriver.Remote(SELENIUM_SERVER,webdriver.DesiredCapabilities.CHROME)
selenium.get(GOOGLE_MUSIC_URL)
selenium.find_element_by_id("Email").send_keys(LOGIN_EMAIL)
#time.sleep(WAIT_TIME)
#selenium.find_element_by_id("Passwd").send_keys(LOGIN_PASSWORD)
time.sleep(WAIT_TIME*3)
selenium.find_element_by_id("signIn").click()

time.sleep(WAIT_TIME)
selenium.find_element_by_id("all").click()

songs = selenium.find_elements_by_class_name("songRow")
for song in songs:
    processSong(song)

selenium.quit()
