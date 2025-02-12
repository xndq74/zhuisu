import time
from os import times

from selenium import webdriver  # 用于操作浏览器
from selenium.webdriver.chrome.options import Options  # 设置谷歌浏览器
from selenium.webdriver.chrome.service import Service  # 管理谷歌驱动
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def click_element(driver, xpath, timeout=10):
    """
    等待元素可点击并执行点击操作
    :param driver: WebDriver实例
    :param xpath: 元素的XPath路径
    :param timeout: 等待时间（秒）
    """
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()


def input_text(driver, xpath, text, timeout=10):
    """
    等待输入框可见并输入文本
    :param driver: WebDriver实例
    :param xpath: 元素的XPath路径
    :param text: 需要输入的文本
    :param timeout: 等待时间（秒）
    """
    input_field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    input_field.send_keys(text)


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
    # 新增
    click_element(driver,'/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[1]/span[1]/span/span/span[1]')
    # 从备案库选择产品
    click_element(driver,'/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[2]/span[2]')
    # 输入产品名称
    time.sleep(1)
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[2]/div/div[2]/input','大白菜')
    time.sleep(1)
    # 设置生产厂商
    input_text(driver,
               '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[4]/div/div[2]/input',
               '新罗区谢贤福蔬菜摊')
    time.sleep(1)
    # 点击查询
    click_element(driver,
                  '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[2]/td[3]/span[1]/span')
    time.sleep(2)
    # 输入日期
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[6]/div/div/div[3]/input[1]','2025-02-12')
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[7]/div/div/div[2]/input','20250212')
    # 输入数量
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[8]/div/div/div[3]/input[1]','10')
    # 点击添加
    click_element(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[12]/a')

    # 进入进货台账
    click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[1]/span[2]')
    # 设置供货方
    click_element(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div[2]')
    input_text(driver,'/html/body/div[15]/div/div[1]/div[2]/input','新罗区谢贤福蔬菜摊')
    click_element(driver, '/html/body/div[15]/div/span[1]/span/span/span[3]')
    time.sleep(2)
    click_element(driver, '/html/body/div[15]/div/div[5]/div[3]/div[2]/div/table/tbody/tr/td[1]')
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[1]/div[2]/input','福建万鹭贸易有限公司')
    time.sleep(1)
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[2]/div[2]/input','闽FZN138')
    time.sleep(1)
    input_text(driver,'/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[3]/div[2]/input','13950826868')
    click_element(driver,'/html/body/div[9]/div[2]/div[2]/span[2]/span/span/span[3]')



if __name__ == "__main__":
    browser = init_browser()  # 初始化浏览器
    login_process(browser)  # 执行登录流程
