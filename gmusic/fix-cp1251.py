#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import time
from selenium import selenium
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import Request, HttpErrorHandler
import urllib2
import urlparse
import json
from optparse import OptionParser

class GMusicFix(object):

    def __init__(self):
        """Constructor reads command line arguments and store given parameters."""
        ###Getting command line options
        #usage = 'usage: %prog [options]'
        #parser = optparse.OptionParser()
        #parser.add_option('-c',  action="store", dest="config_path")
        #cmd_opts, args = parser.parse_args()
        #config_path = cmd_opts.config_path
        #del sys.argv[1:]

        #check validity of paramters. Exit if false
        #if self.check_params(config_path, parser) is False: sys.exit(1)

        #self.configure(config_path,parser)
        if (platform.system() == 'Windows'):
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()

        self.google_music_url = "http://music.google.com/"
        self.login = "your.mail@gmail.com"
        self.password = "xxx"
        self.wait_time = 3

        #START_SONG = 3900
        self.start_song = 0
        self.process_all = False

        self.scroll_step = 10
        self.search_step = 200

    def prepare_text(self, text):
        if (platform.system() == 'Windows'):
            return text.encode('cp1251')
        else:
            return text.encode('utf-8')

    def fix_encoding(self, text):
        ln = u'';
        for c in text.decode('utf-8'):
            if (ord(c) >= 0xC0 and ord(c)<=0xFF):
                c = unichr(ord(c)+0x350)
            ln = ln + c
        return ln.encode('utf-8')

    def has_wrong_chars(self, text):
        try:
            text = prepare_text(text)
            tt = text.decode('utf-8')
        except:
            return False
        for c in text.decode('utf-8'):
            if (ord(c) >= 0xC0 and ord(c)<=0xFF):
                return True
        return False

    def process_field(self, id):
        value = prepare_text(self.driver.find_element_by_id(id).value)
        valueLen = len(self.driver.find_element_by_id(id).value)

        fixed = fix_encoding(value).decode('utf-8')
        fixed = fixed.replace('"','\\"')
        set_value_script = 'document.getElementById("'+id+'").value="'+fixed+'"'
        driver.execute_script(set_value_script)
        #send keys does not work
        #driver.find_element_by_id(id).clear()
        #driver.find_element_by_id(id).send_keys("test")
        #driver.find_element_by_id(id).clear()
        #driver.find_element_by_id(id).send_keys(fixed)

        if (valueLen != len(self.driver.find_element_by_id(id).value)):
            raise Exception("Possible fix error - value length changed")

    def open_menu(self, idx,  song):
        menu_script = """
            function sendEvent(elem, name) {
                var event = document.createEvent("MouseEvents");
                event.initMouseEvent(name,true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                elem.dispatchEvent(event);
            }

            var row = document.getElementsByClassName('songRow')["""+str(idx)+"""];
            var menu = row.getElementsByClassName('fade-out-with-menu')[0];
            sendEvent(menu,'mouseover');
            bt = menu.getElementsByClassName('goog-flat-button')[0];
            sendEvent(bt, 'click');
            editItem = document.getElementById(":d")
            sendEvent(editItem,'mousedown');
            sendEvent(editItem,'mouseup');
        """
        self.driver.execute_script(menu_script)
        #driver.find_element_by_id(":d").click()

    def process_song(self, idx,  song):
        open_menu(self.driver, idx,  song)
        process_field(self.driver, "edit-name")
        process_field(self.driver, "edit-song-artist")
        process_field(self.driver, "edit-album-artist")
        process_field(self.driver, "edit-album")
        process_field(self.driver, "edit-composer")
        self.driver.find_element_by_class_name("modal-dialog-buttons").find_element_by_tag_name("button").click()

    def process(self):
        num = 0
        try:
            self.driver.get(self.google_music_url)
            self.driver.find_element_by_id("Email").send_keys(self.login)
            #time.sleep(WAIT_TIME)
            #driver.find_element_by_id("Passwd").send_keys(LOGIN_PASSWORD)
            time.sleep(self.wait_time*3)
            try:
                bt = self.driver.find_element_by_id("signIn")
                bt.click()
            except:
                pass #if the user clicked sing in

            time.sleep(self.wait_time)
            if (self.process_all):
                # browse to all songs
                self.driver.find_element_by_id("all").click()
                time.sleep(self.wait_time*4)
            else:
                # wait until the user browses to the desired page
                time.sleep(self.wait_time*10)
            self.driver.switch_to_default_content()

            if (self.start_song > 0):
                sys.stdout.write("[\/]")
                dt = 0
                while (dt < self.start_song):
                    dt = dt + self.search_step
                    scroll_script = "document.getElementById('main').scrollTop=23*"+str(dt)
                    self.driver.execute_script(scroll_script)
                    time.sleep(self.wait_time/2)
                scroll_script = "document.getElementById('main').scrollTop=23*"+str(self.start_song)
                self.driver.execute_script(scroll_script)
                time.sleep(self.wait_time/2)
            sys.stdout.write("[?]")
            songs = self.driver.find_elements_by_class_name("songRow")
            for i in range(self.start_song, len(songs)-1):
                text = songs[i].text
                if (self.has_wrong_chars(text)):
                    self.process_song(i,  songs[i])
                    sys.stdout.write("+")
                    time.sleep(self.wait_time/2)
                else:
                    sys.stdout.write(".")
                if ((i-self.start_song) % self.scroll_step == 0):
                    scroll_script = "document.getElementById('main').scrollTop+=230"
                    self.driver.execute_script(scroll_script)
                if ((i-self.start_song) % self.search_step == 0):
                    #re-search songs every SEARCH_STEP (default 200) steps - new songs can be AJAX-loaded
                    sys.stdout.write("[?]")
                    songs = self.driver.find_elements_by_class_name("songRow")
                num = i
                sys.stdout.flush()

            time.sleep(self.wait_time)
            print('done: ' + str(num) + ' songs')
            self.driver.quit()
        except:
            print('failed after: ' + str(num) + ' songs')
            self.driver.quit()
            raise

fix = GMusicFix()
fix.process()
