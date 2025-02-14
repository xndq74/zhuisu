import time
from os import times

from selenium import webdriver  # 用于操作浏览器
from selenium.webdriver.chrome.options import Options  # 设置谷歌浏览器
from selenium.webdriver.chrome.service import Service  # 管理谷歌驱动
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def init_browser():
    """
    初始化Chrome浏览器，设置必要的选项并返回浏览器对象
    """
    options = Options()
    options.add_argument('--no-sandbox')  # 禁用沙盒模式，提升兼容性
    options.add_experimental_option('detach', True)  # 代码执行完毕后不关闭浏览器
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
    driver.set_window_size(1920, 1080)  # 设置浏览器窗口大小
    return driver


def click_element(driver, xpath, timeout=30):
    """
    等待元素可点击并执行点击操作
    :param driver: WebDriver实例
    :param xpath: 元素的XPath路径
    :param timeout: 等待时间（秒）
    """
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    return element
def click_element_data(driver, data, timeout=30):
    """
    等待元素可点击并执行点击操作
    :param driver: WebDriver实例
    :param data: 元素的data
    :param timeout: 等待时间（秒）
    """
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, data)))
    element.click()
    return element

def input_text(driver, xpath, text, timeout=30):
    """
    等待输入框可见并输入文本
    :param driver: WebDriver实例
    :param xpath: 元素的XPath路径
    :param text: 需要输入的文本
    :param timeout: 等待时间（秒）
    """
    input_field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    # 获取输入框当前的值
    current_value = input_field.get_attribute('value')

    # 检查输入框是否有文字
    if current_value:
        # 若有文字，先清除
        input_field.clear()
    input_field.send_keys(text)
    return input_field

def input_text_data(driver, data, text, timeout=30):
    """
    等待输入框可见并输入文本
    :param driver: WebDriver实例
    :param data: 元素的data
    :param text: 需要输入的文本
    :param timeout: 等待时间（秒）
    """
    input_field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, data)))
    # 获取输入框当前的值
    current_value = input_field.get_attribute('value')

    # 检查输入框是否有文字
    if current_value:
        # 若有文字，先清除
        input_field.clear()
    input_field.send_keys(text)
    return  input_field


def login_process(driver):
    """
    执行完整的登录流程
    """
    driver.get('https://220.160.53.129:8081/fdauser/user/authLogin.jsp')

    # 处理弹窗与登录
    click_element(driver, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button')  # 第一个弹窗
    click_element(driver, '/html/body/div[2]/div/div[3]/a[1]')  # 第二个登录按钮
    click_element(driver, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button')  # 第二个弹窗
    click_element(driver, '/html/body/div[2]/div[3]/div[1]/ul/li[2]')  # 选择账户密码登录
    click_element(driver, '//*[@id="frdl"]')  # 切换到法人登录
    click_element(driver, '/html/body/div[6]/div[3]/a')  # 点击提示信息确认

    # 输入账号和密码
    input_text(driver, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input',
               '13285909090')
    input_text(driver, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/form/div/div[4]/div[2]/input',
               'wl123321')
    # 点击登入
    # 等待3秒手动输入验证码
    time.sleep(8)
    click_element(driver,'//*[@id="submit1"]')
    # 进入销售追溯
    click_element(driver,'//*[@id="jquery-accordion-menu"]/ul/li[2]/a')
    # 进入进货登记
    click_element(driver,'//*[@id="jquery-accordion-menu"]/ul/li[2]/ul/li[2]/ul/li[1]/a')







    # 读取 Excel 文件
    file_path = 'data2025-02-1126.xlsx'
    df = pd.read_excel(file_path)

    # 打印数据框的前几行，确认数据加载是否成功
    print("数据框预览：")
    print(df.head())

    # 统计所有不重复的生产商数量
    unique_producers = df['生产商'].unique()
    num_producers = len(unique_producers)

    # 外层循环：遍历所有不重复的生产商
    for producer in unique_producers:
        print(f"\n正在处理的生产商：{producer}")
        # 新增
        click_element(driver,
                      '/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[1]/span[1]/span/span/span[1]')
        # 从备案库选择产品
        click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[2]/span[2]')
        time.sleep(1)
        # 设置生产厂商
        input_text(driver,
                   '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[4]/div/div[2]/input',
                   producer)

        # 内层循环：针对当前生产商的进货记录进行迭代
        # 使用 groupby 按生产商分组，获取当前生产商的所有记录
        producer_records = df[df['生产商'] == producer]

        # 遍历当前生产商的每一行记录
        for index, row in producer_records.iterrows():
            # 获取产品名称、进货数量和生产商信息
            product_name = row['产品名称'] if not pd.isna(row['产品名称']) else "未知产品"
            quantity = row['进货数量'] if not pd.isna(row['进货数量']) else "未知数量"
            df['日期'] = pd.to_datetime(df['日期'])
            date = ''
            data1 = ''
            # 遍历每一行
            for index1, row1 in df.iterrows():
                if pd.isna(row1['日期']):
                    date = "未知数量"
                else:
                    date = row1['日期'].strftime('%Y-%m-%d')
                    date1 = row1['日期'].strftime('%Y%m%d')
            # 输出当前处理的记录详情
            print(f"处理记录：产品名称={product_name}, 进货数量={quantity}, 生产商={producer} ,日期={date, date1}")

            # 输入产品名称
            time.sleep(1)
            input_text(driver,
                       '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[2]/div/div[2]/input',
                       product_name)

            time.sleep(1)
            # 点击查询
            click_element(driver,
                          '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[2]/td[3]/span[1]/span')
            time.sleep(2)
            # 输入日期
            input_text(driver,
                       '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[6]/div/div/div[3]/input[1]',
                       date)
            input_text(driver,
                       '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[7]/div/div/div[2]/input',
                       date1)
            # 输入数量
            input_text(driver,
                       '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[8]/div/div/div[3]/input[1]',
                       quantity)
            # 点击添加进货
            click_element(driver,
                          '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[12]/a')

        # 进入进货台账
        time.sleep(1)
        click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[1]/span[2]')
        click_element(driver,
                      '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div[2]')
        time.sleep(1)
        # # 切换
        # click_element(driver,'/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[2]/span[2]')
        # time.sleep(1)
        # click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[1]/span[2]')
        #
        # # 输入供应商
        # click_element(driver,
        #               '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div[2]')
        # time.sleep(1)
        # click_element(driver,'/html/body/div[15]/div/div[1]/div[2]/input')
        # time.sleep(1)
        # input_text(driver,'/html/body/div[13]/div/div[1]/div[2]/input',producer)
        #-----------------------------------------------------------------------------
        # 设置供货方 用ID的方式来查找
        time.sleep(1)
        #匹配dijit_form_ValidationTextBox开头的id
        # a1 = click_element(driver,"//div[starts-with(@id, 'dijit_form_ValidationTextBox')]")
        # print(f'是否找到元素A1：{a1}')
        parent_element = driver.find_element(By.ID,'widget_stockParmeter_add_form_supplyEntName_dropdown')

        print(f'是否找到父元素{parent_element}')
        print(parent_element.get_attribute('outerHTML'))
        time.sleep(5)
        input_element = parent_element.find_element(By.CSS_SELECTOR,'[data-dojo-attach-point="textbox,focusNode"]')
        print(f'是否找到元素{input_element}')
        print(input_element.get_attribute('outerHTML'))
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(input_element))
        element.click()
        time.sleep(1)
        # input_text(driver, "//div[starts-with(@id, 'dijit_form_ValidationTextBox')]", producer)

        input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(input_element))
        # 获取输入框当前的值
        current_value = input_field.get_attribute('value')

        # 检查输入框是否有文字
        if current_value:
            # 若有文字，先清除
            input_field.clear()
        input_field.send_keys(producer)




        time.sleep(1)
        # 点击查询
        click_element(driver, '/html/body/div[15]/div/span[1]/span/span')
        time.sleep(1)
        click_element(driver, '/html/body/div[15]/div/div[5]/div[3]/div[2]/div/table/tbody/tr')
        input_text(driver,
                   '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[1]/div[2]/input',
                   '福建万鹭贸易有限公司')
        time.sleep(1)
        input_text(driver,
                   '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[2]/div[2]/input',
                   '闽FZN138')
        time.sleep(1)
        input_text(driver,
                   '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[3]/div[2]/input',
                   '13950826868')
        # 提交操作
        click_element(driver, '/html/body/div[9]/div[2]/div[2]/span[2]/span/span/span[3]')






if __name__ == "__main__":
    browser = init_browser()  # 初始化浏览器
    login_process(browser)  # 执行登录流程
