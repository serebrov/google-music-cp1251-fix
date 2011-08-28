#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from selenium import selenium
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import Request, HttpErrorHandler
import urllib2
import urlparse
import json

SELENIUM_SERVER = "http://127.0.0.1:4444/wd/hub"
GOOGLE_MUSIC_URL = "http://music.google.com/"
LOGIN_EMAIL = "seb.goo@gmail.com"
LOGIN_PASSWORD = "xxx"
WAIT_TIME=3

START_SONG = 3146

def fix_encoding(text):
    ln = u'';
    for c in text.decode('utf-8'):
        if (ord(c) >= 0xC0 and ord(c)<=0xFF):
            c = unichr(ord(c)+0x350)
        ln = ln + c
    return ln.encode('utf-8')

def has_wrong_chars(text):
    try:
        text = text.encode('cp1251')
        tt = text.decode('utf-8')
    except:
        return False
    for c in text.decode('utf-8'):
        if (ord(c) >= 0xC0 and ord(c)<=0xFF):
            return True
    return False

def get_raw_value(driver, id):
    e = driver.find_element_by_id(id)

    url = SELENIUM_SERVER + '/session/'+driver.session_id + '/element/' + e.id + '/value'
    data = '{"sessionId": "'+driver.session_id +'", "id": "'+e.id+'"}'
    method = 'GET'
    request = Request(url, data=data, method=method)
    request.add_header('Accept', 'application/json')
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                                          HttpErrorHandler())
    response = opener.open(request)
    try:
        body = response.read().replace('\x00', '').strip()
        st = body.index('"value":"') + 9
        end = body.index('","class"')
        return body[st:end]
    finally:
        response.close()

def process_field(driver, id):
    value = driver.find_element_by_id(id).value.encode('cp1251')
    #even so the value is not the same as in text file test
    #try driver.get_page_source()
    #value = get_raw_value(driver, id)
    valueLen = len(value)

    fixed = fix_encoding(value).decode('utf-8')
    fixed = fixed.replace('"','\\"')
    set_value_script = 'document.getElementById("'+id+'").value="'+fixed+'"'
    driver.execute_script(set_value_script)
    #send keys does not work
    #driver.find_element_by_id(id).clear()
    #driver.find_element_by_id(id).send_keys("test")
    #driver.find_element_by_id(id).clear()
    #driver.find_element_by_id(id).send_keys(fixed)

    if (valueLen != len(driver.find_element_by_id(id).value)):
        raise Exception("Possible fix error - value length changed")

def open_menu(driver, idx):
    menu_script = """
        var row = document.getElementsByClassName('songRow')[+"""+str(idx)+"""];
        var menu = row.getElementsByClassName('fade-out-with-menu')[0];
        var overEvent = document.createEvent("MouseEvents");
        overEvent.initMouseEvent("mouseover",true, true);
        var clickEvent = document.createEvent("MouseEvents");
        clickEvent.initMouseEvent("click",true, true);
        menu.dispatchEvent(overEvent);
        bt = menu.getElementsByClassName('goog-flat-button')[0];
        bt.dispatchEvent(clickEvent);
    """
    #song.find_element_by_class_name("fade-out-with-menu").click()
    driver.execute_script(menu_script)
    driver.find_element_by_id(":c").click()

def process_song(driver, idx):
    open_menu(driver, idx)
    process_field(driver, "edit-name")
    process_field(driver, "edit-song-artist")
    process_field(driver, "edit-album-artist")
    process_field(driver, "edit-album")
    process_field(driver, "edit-composer")
    driver.find_element_by_class_name("modal-dialog-buttons").find_element_by_tag_name("button").click()

driver = webdriver.Remote(SELENIUM_SERVER,webdriver.DesiredCapabilities.CHROME)
print "start"
num = 0
try:
    driver.get(GOOGLE_MUSIC_URL)
    driver.find_element_by_id("Email").send_keys(LOGIN_EMAIL)
    #time.sleep(WAIT_TIME)
    #driver.find_element_by_id("Passwd").send_keys(LOGIN_PASSWORD)
    time.sleep(WAIT_TIME*3)
    try:
        bt = driver.find_element_by_id("signIn")
        bt.click()
    except:
        pass #if the user clicked sing in

    time.sleep(WAIT_TIME)
    driver.find_element_by_id("all").click()
    time.sleep(WAIT_TIME*4)
    driver.switch_to_default_content()

    songs = driver.find_elements_by_class_name("songRow")
    songs[0].find_element_by_class_name('variable-width-name-col').click()
    for i in range(START_SONG, len(songs)-1):
        text = songs[i].text
        if (has_wrong_chars(text)):
            process_song(driver, i)
            sys.stdout.write("+")
            time.sleep(WAIT_TIME/2)
        else:
            sys.stdout.write(".")
        if (i==0 or i == len(songs)-2 or i % 500 == 0):
            #force scroll
            open_menu(driver, i)
            driver.find_element_by_class_name('cancel-button-text').click()
            songs = driver.find_elements_by_class_name("songRow")
        num = i

    time.sleep(WAIT_TIME)
    print('done: ' + str(num) + ' songs')
    driver.quit()
except:
    print('failed after: ' + str(num) + ' songs')
    driver.quit()
    raise
