util = __import__('Util')
from selenium import webdriver
import threading
import requests
import json
import time
import os


util.path_spiter = '/'
chrome_driver_path = os.getcwd() + util.path_spiter + 'chromedriver'
data_path = os.getcwd() + util.path_spiter + 'data'
thread_count = 8
gid_queue = []



def snap_data(driver):
    date_str = time.strftime('%Y-%m-%d', time.localtime())
    while True:
        if gid_queue.__len__() > 0:
            try:
                gid = gid_queue.pop()
                driver.get('http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=' + gid)
                datatbl = driver.find_element_by_id('datatbl')
                tbody = datatbl.find_element_by_tag_name('tbody')
                lines = tbody.find_elements_by_tag_name('tr')
                data_arr = []
                for line in lines:
                    data_line = []
                    cells = line.text.split(' ')
                    time_str = cells[0]
                    price_str = cells[1]
                    volume_str = cells[5].split('\n')[0].replace(',', '')
                    type_str = cells[5].split('\n')[1]
                    direction_str = '-'
                    if type_str.strip() == '买盘':
                        direction_str = 'U'
                    if type_str.strip() == '卖盘':
                        direction_str = 'D'
                    data_time = time.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')
                    data_line = [data_time, float(price_str), int(volume_str) * 100, direction_str]
                    data_arr.append(data_line)
                util.save_data_batch(gid, data_arr, data_path)
            except:
                continue
            print(gid_queue.__len__())
        else:
            time.sleep(60)



def get_all_gids():
    all_gid_json = json.loads(requests.get('http://52.80.17.211:8848/api/get_all_gids.aspx').text)
    for gid in all_gid_json['gids']:
        gid_queue.append(gid)



start_time = time.localtime()
get_all_gids()
driver_arr = []
i = 0
while i < thread_count:
    driver = webdriver.Chrome(chrome_driver_path)
    driver_arr.append(driver)
    threading.Thread(target=snap_data, args=(driver,)).start()
    i = i + 1

while gid_queue.__len__() > 0:
    time.sleep(5)

end_time = time.localtime()

print(time.strftime('%H:%M:S', start_time))
print(time.strftime('%H:%M:S', end_time))
for driver in driver_arr:
    driver.close()






