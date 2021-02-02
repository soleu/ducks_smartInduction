from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

# from flask import Flask, request, jsonify
# app = Flask(__name__)
 
# @app.route('/userLogin', methods = ['POST'])
# def userLogin():
#     user = request.get_json()#json 데이터를 받아옴
#     return jsonify(user)# 받아온 데이터를 다시 전송
 
# @app.route('/environments/<language>')
# def environments(language):
#     return jsonify({"language":language})
 
 
# if __name__ == "__main__":
#     app.run()


driver = webdriver.Chrome(executable_path=r'C:\Users\이솔\Desktop\crawling\selenium/chromedriver.exe')
driver.get("https://haemukja.com/")
elem = driver.find_element_by_name("name")

time.sleep(2)
key = input("음식을 입력하세요: ") #재료 입력이 아닌 받아서 할 수 있도록 구현
elem.send_keys(key)
elem.send_keys(Keys.RETURN)

pickimg = driver.find_element_by_class_name("call_recipe.thmb")
pickimg.click()

count = 1
time.sleep(2)

images=driver.find_elements_by_css_selector("#modal-content > div > div.view_recipe > section.sec_detail > section.sec_rcp_step> ol> li")
n=len(images)
print(n)
while count<=n :
    try:
        time.sleep(2)
        countstr=str(count)
        img='//*[@id="modal-content"]/div/div[1]/section[2]/section[1]/ol/li['+countstr+']/div/img'
        # img='//*[@id="modal-content"]/div/div[1]/section[2]/section[1]/ol/li[1]/div/img'
        textAddress=driver.find_element_by_xpath('//*[@id="modal-content"]/div/div[1]/section[2]/section[1]/ol/li['+countstr+']/p')
        text_data=textAddress.text
        print(text_data)
        imgUrl = driver.find_element_by_xpath(img).get_attribute("src")
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        
        count = count + 1
    except:
        pass

print("종료")
driver.quit()
# self.driver.quit()
# for image in images:
#     try:
#         time.sleep(2)
#         url='//*[@id="modal-content"]/div/div[1]/section[2]/section[1]/ol/li['+count+']/div/img'
#         imgUrl = driver.find_element_by_xpath(url).get_attribute("src")
#         urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
#         count = count + 1
#     except:
#         pass
