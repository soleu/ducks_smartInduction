'''
test api server 
'''

from flask import Flask, request ,jsonify,render_template
from flask_restful import Resource, Api 
from flask.views import MethodView
import logging 
import json,base64 
import os, sys 
import datetime 
import threading
from selenium.webdriver.common.keys import Keys
# import Obj
import urllib.request
import io
from io import BytesIO

from flask import current_app as app
from flask import send_file

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer


app = Flask(__name__) 
api = Api(app) 
log = logging.basicConfig(filename='testsvr.log', level=logging.INFO) 
# 로깅을 전부 끄기 
# # logging.getLogger('werkzeug') 
# # log = logging.get
# log.disabled = True 
# app.logger.disabled = True 

''' /getRecipeCrawler ''' 
class getRecipeCrawler(MethodView):
    def get(self): 
         data = request.args 
         print('recv:', data) # dictionary 
         return 'Hello.' 

    def __init__(self):
        self.url = 'https://www.haemukja.com/'
        self.nextPage = [
            '//*[@id="content"]/section/div[2]/div/div[2]/a[2]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[5]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[6]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[7]'
            ]
        self.location = 'a.call_recipe > strong'

    def launch_crawler(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)

    def find_click(self, xpath, sleep_interval=3):
        btn = self.driver.find_element_by_xpath(xpath)
        btn.click()
        time.sleep(sleep_interval)
    
    def find_recipe(self, ingredient):
        search_box = self.driver.find_element_by_name('name')
        search_box.send_keys(ingredient)
        search_box.submit()

    def get_recipe(self, element):
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')
        recipeName = self.soup.select(element)
        for recipe in recipeName:
            return(recipe.text)

    def post(self):
         result=""
         logging.info('ingredient test')
         data=request.get_json(force=True) # parse json string 
         print('request.json=', data)
         temp=data['ingred']
         Main_ingredient=str(temp)
         self.launch_crawler()
         self.find_recipe(Main_ingredient)

         for i in range(len(self.nextPage)):
                temp2=self.get_recipe(self.location)
                result+=temp2
                result+=", "
                self.get_recipe(self.location)
                self.find_click(self.nextPage[i])

         logging.info('result='+json.dumps(result))
        #  print("종료")
         self.driver.quit()
         print (result)
        #  self.send_response(result)
         return result
         
        
    def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
         server_address = ('', 8000)
         httpd = server_class(server_address, handler_class)
         httpd.serve_forever()
         


api.add_resource(getRecipeCrawler, '/getRecipeCrawler') 
# api.add_resource(getCookingCrawler,'/getCookingCrawler')
port = 18899 

if __name__=='__main__': 
    print('Start Server... port=', port) 
    logging.info('start server') 
    app.run(host='0.0.0.0', port=port, debug=True) 
    # 디버그 모드로 하면 소스 수정시 자동으로 서버 재시작이 된다.
