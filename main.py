from pathlib import Path
from threading import Thread
from xml import etree
from IPython.display import display
import requests
import pandas as pd
import json
import xlsxwriter
import jinja2
import schedule
from datetime import datetime
import datetime
import time
import sched
import tkinter
import tkinter.messagebox  # 弹窗库
from lxml import etree
from django.conf.locale import pt
from openpyxl.workbook import web
# 需求：登陆12306,输入短信验证码后登陆
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
# 导入动作链对应的类
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.options import Options
import json
import time
from captcha import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #期望的条件 from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By

# 导入城市
f2 = open('city.json', 'r')
city = json.load(f2)

# 查询函数
def chaxun(city):
    # 判断出发地
    while True:
        in_start = input("请输入出发地：\n")
        if in_start not in city.keys():
            print("输入的城市有误，请重新输入：")
            continue
        else:
            break
    # 判断目的地
    while True:
        in_end = input("请输入目的地：\n")
        if in_end not in city.keys():
            print("输入的城市有误，请重新输入：")
            continue
        else:
            break
    # 判断输入时间格式
    while True:
        time = input("请输入时间（格式：xxxx.xx.xx)：\n")
        if (len(time.split(".")) != 3 or len(time.split(".")[0]) != 4
                or len(time.split(".")[1]) != 2 or len(time.split(".")[2]) != 2):
            print("输入的时间有误，请重新输入：")
            continue
        else:
            break
    time = time.replace('.', '-')
    in_start = city[in_start]
    in_end = city[in_end]
    chaxun_list = [in_start, in_end, time]
    return chaxun_list

def set_row_style(row):
    return ['background-color: green', 'color:black']

# 动车类型函数
def the_kind():
    # 输入动车类型
    kind_list = ['高铁', '火车', '全部']
    while True:
        kind = input("请输入要查询的类型（高铁/火车/全部）：\n")
        if kind in kind_list:
            break
        else:
            continue
    return kind

def func(time, start, end, kind):
    front_url = "https://kyfw.12306.cn/otn/leftTicket/query"
    data = {
        "leftTicketDTO.train_date": time,
        "leftTicketDTO.from_station": start,
        "leftTicketDTO.to_station": end,
        "purpose_codes": "ADULT"
    }
    header = {
        "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Cookie": (
            "_uab_collina=171612732780866759993918; JSESSIONID=1753D82C75A9D1B5FD26D74F047D5B2F; _jc_save_wfdc_flag=dc; BIGipServerotn=1373176074.50210.0000; BIGipServerpassport=837288202.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerportal=3084124426.17183.0000; _jc_save_fromStation=%u957F%u6C99%2CCSQ; "
            "_jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2024-06-28; _jc_save_toDate=2024-06-28")
    }

    front_content = requests.get(front_url, params=data, headers=header)
    front_content.encoding = "utf-8"
    front_content.close()  # 关闭requests
    result = front_content.json()['data']['result']  # 返回json字典数据

    lst_G = []  # 高铁信息
    lst_KTZ = []  # 火车信息
    lst_all = []  # 全部信息

    for it in result:
        info_list = it.split("|")  # 切割数据，中文转英文
        num = info_list[3]
        start = info_list[8]  # 启动时间
        arrive = info_list[9]  # 到达时间
        time = info_list[10]  # 经历时长
        business_seat = info_list[32]  # 高铁商务座
        if business_seat == "无":
            business_seat = ''
        first_seat = info_list[31]  # 高铁一等座
        if first_seat == "无":
            first_seat = ''
        second_seat = info_list[30]  # 高铁二等座
        if second_seat == "无":
            second_seat = ''
        soft_sleeper = info_list[23]  # 火车软卧
        hard_sleeper = info_list[28]  # 火车硬卧
        soft_seat = info_list[27]  # 火车软座
        hard_seat = info_list[29]  # 火车硬座
        none_seat = info_list[26]  # 无座
        dic = {
            "num": num,
            "start": start,  # 启动时间
            "arrive": arrive,  # 到达时间
            "time": time,  # 经历时长
            "business_seat": business_seat,  # 高铁商务座
            "first_seat": first_seat,  # 高铁一等座
            "second_seat": second_seat,  # 高铁二等座
            "soft_sleeper": soft_sleeper,  # 火车软卧
            "hard_sleeper": hard_sleeper,  # 火车硬卧
            "soft_seat": soft_seat,  # 火车软座
            "hard_seat": hard_seat,  # 火车硬座
            "none_seat": none_seat  # 无座
        }

        # 进行三种分类
        lst_all.append(dic)
        if 'G' in num:
            lst_G.append(dic)
        else:
            lst_KTZ.append(dic)

    # dataframe格式设置
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 200)

    # 三种类型票 高铁 火车 全部
    content_G = pd.DataFrame(lst_G)
    content_KTZ = pd.DataFrame(lst_KTZ)
    content_all = pd.DataFrame(lst_all)

    print(content_all)
    with pd.ExcelWriter("火车票查询.xlsx", engine='xlsxwriter') as writer:
        if kind == '高铁':
            content_G.to_excel(writer, sheet_name="sheet", index=False)
        elif kind == '火车':
            content_KTZ.to_excel(writer, sheet_name="sheet", index=False)
        else:
            content_all.to_excel(writer, sheet_name="sheet", index=False)

        worksheet = writer.sheets['sheet']
        workbook = writer.book
        format_green = workbook.add_format({'bg_color': 'green'})
        worksheet.conditional_format('E2:E1000', {'type': 'cell', 'criteria': '>', 'value': 0, 'format': format_green})
        worksheet.conditional_format('F2:F1000', {'type': 'cell', 'criteria': '>', 'value': 0, 'format': format_green})
        worksheet.conditional_format('G2:G1000', {'type': 'cell', 'criteria': '>', 'value': 0, 'format': format_green})

def time_printer(times, in_start, in_end, kind):
    print("time", times, in_start, in_end, kind)
    func(times, in_start, in_end, kind)
    print("刷新函数执行完毕")
    shed_time(times, in_start, in_end, kind)

def shed_time(times, in_start, in_end, kind):
    s = sched.scheduler(time.time, time.sleep)  # 生成调度器
    s.enter(5, 0, time_printer, (times, in_start, in_end, kind))
    s.run()

#提示余票弹窗
def show_have_ticket_pop():
    root = tkinter.Tk()
    root.withdraw()

    tkinter.messagebox.showinfo('提示', '有余票了')

#登陆12306
def login_account(false=None):
    #第一阶段登陆
    # username = input("请输入用户名/邮箱/手机号：")
    # while username == '':
    #     username = input('12306用户名不能为空，请重新输入：')
    # password = input("请输入密码：")
    # while username == '':
    #     username = input('12306密码不能为空，请重新输入：')

    username = "751746584@qq.com"
    password = "fc751746584fc"
    id_card = "001X"

    options = webdriver.ChromeOptions()
    # options.add_argument('headless')  # 设置option
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=options)
    actions = ActionChains(browser)

    browser.maximize_window()
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
    browser.get(login_url)
    time.sleep(2)

    print("输入账号")
    loginUserNameInput = browser.find_element(By.ID, "J-userName")
    actions.move_to_element(loginUserNameInput).click().perform()

    print("输入密码")
    loginPassWordInput = browser.find_element(By.ID, "J-password")
    actions.move_to_element(loginPassWordInput).click().perform()

    loginBtn = browser.find_element(By.ID, "J-login")

    loginUserNameInput.send_keys(username)
    loginPassWordInput.send_keys(password)
    loginBtn.click()

    #登陆
    time.sleep(2)

    print("身份证后四位")
    loginIdCardInput = browser.find_element(By.ID, "id_card")
    actions.move_to_element(loginIdCardInput).click().perform()
    loginIdCardInput.send_keys(id_card)
    time.sleep(2)

    print("发送短信验证码")
    loginVerificationButton = browser.find_element(By.ID, "verification_code")
    loginVerificationButton.click()

    loginVerificationCode = browser.find_element(By.ID, "code")
    actions.move_to_element(loginVerificationCode).click().perform()

    time.sleep(2)
    verification_code = input("请输入收到的短信验证码")
    loginVerificationCode.send_keys(verification_code)

    sureBtn = browser.find_element(By.ID, "sureClick")
    sureBtn.click()
    time.sleep(2)

    link_for_ticket = browser.find_element(By.ID, "link_for_ticket")
    # link_for_ticket.click()
    actions.move_to_element(link_for_ticket).click().perform()
    time.sleep(2)

    print("??123123123")
    #第二阶段锁定订单

    # 添加保持登录的数据路径：安装目录一般在C:\Users\****\AppData\Local\Google\Chrome\User Data
    # options = webdriver.ChromeOptions()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # browser = webdriver.Chrome(options=options)
    # actions = ActionChains(browser)
    # browser.maximize_window()

    # login_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    # browser.get(login_url)
    # browser.add_cookie({"domain": "kyfw.12306.cn", "name": "uKey", "path": "/", "sameSite": "Lax", "value": "991436403f4b1092262ee9a71d221bd30f540b0427ee58bfa642d039d4760a1f"})
    # browser.get(login_url)
    # time.sleep(1)

    fromStationText_label = browser.find_element(By.ID, "fromStationText")
    actions.move_to_element(fromStationText_label).click().perform()
    fromStationText_label.clear()
    fromStationText_label.send_keys("chengdu")
    fromStationText_label.send_keys(Keys.ENTER)
    time.sleep(2)
    print("??123123123--11")

    toStationText_label = browser.find_element(By.ID, "toStationText")
    actions.move_to_element(toStationText_label).click().perform()
    toStationText_label.clear()
    toStationText_label.send_keys("beijing")
    toStationText_label.send_keys(Keys.ENTER)
    time.sleep(2)
    print("??123123123--22")
    #
    train_date_label = browser.find_element(By.ID, "train_date")
    actions.move_to_element(train_date_label).click().perform()
    train_date_label.clear()
    train_date_label.send_keys("2024-08-27")
    time.sleep(2)

    query_ticket_btn = browser.find_element(By.ID, "query_ticket")
    query_ticket_btn.click()
    time.sleep(2)
    print("??123123123--33")
    # 点击预定

    # 一定要用显示等待，否则会返回空列表
    # WebDriverWait(browser, 1000).until( EC.presence_of_element_located((By.XPATH, ".//tbody[@id = 'queryLeftTable']/tr")) )

    tr_list = browser.find_elements(By.XPATH, ".//tbody[@id ='queryLeftTable']/tr[not(@datatran)]")
    print("tr_listtr_list", tr_list)

    for tr in tr_list:
        try:
            # train_number = tr.find_element(By.CLASS_NAME, "number").text
            left_ticket = tr.find_element(By.XPATH, ".//td[4]").text  # 找到第四个td标签下的文本 if left_ticket == "有" or left_ticket.isdigit: #判断输入的车次是否在列表中
        except:
            print("")
        else:
            print("")
            if left_ticket == "有":  # 判断输入的车次是否在列表中
                orderBotton = tr.find_element(By.CLASS_NAME, 'btn72')
                print("orderBotton", orderBotton)
                orderBotton.click()
                break

    # reserve = browser.find_element(By.XPATH, "/html/body/div[2]/div[7]/div[12]/table/tbody/tr[13]/td[13]/a")
    # print("reservereserve", reserve)
    # reserve.click()
    time.sleep(2)
    #
    print("normalPassenger_0")
    normalPassenger = browser.find_element(By.ID, "normalPassenger_0")
    normalPassenger.click()
    time.sleep(2)

    print("submitOrder_id")
    submitOrder_id = browser.find_element(By.ID, "submitOrder_id")
    submitOrder_id.click()
    time.sleep(2)

    print("确定")
    qr_submit_id = browser.find_element(By.ID, "qr_submit_id")
    qr_submit_id.click()
    time.sleep(2)


    time.sleep(5000)
    # browser.find_element(By.XPATH, '//*[@id="ticket_4p000G696505_03_05"]/td[13]/a').click()

if __name__ == '__main__':
    kind_list = ['抢票']
    while True:
        kind = input("请输入你是要抢票还是要查询：\n")
        if kind in kind_list:
            login_account()
        else:
            lis = chaxun(city)
            in_start = lis[0]
            in_end = lis[1]
            times = lis[2]
            kind = the_kind()
            func(times, in_start, in_end, kind)

            # shed_time(times, in_start, in_end, kind)




