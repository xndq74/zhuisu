import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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


def click_element(driver, selector, method='xpath', timeout=30):
    """
    等待元素可点击并执行点击操作
    :param driver: WebDriver实例
    :param selector: 元素的定位符（XPath 或 CSS Selector）
    :param method: 定位元素的方法（'xpath' 或 'css'）
    :param timeout: 等待时间（秒）
    """
    by_method = By.XPATH if method == 'xpath' else By.CSS_SELECTOR
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_method, selector)))
    element.click()
    return element


def input_text(driver, selector, text, method='xpath', timeout=30):
    """
    等待输入框可见并输入文本
    :param driver: WebDriver实例
    :param selector: 元素的定位符（XPath 或 CSS Selector）
    :param text: 需要输入的文本
    :param method: 定位元素的方法（'xpath' 或 'css'）
    :param timeout: 等待时间（秒）
    """
    by_method = By.XPATH if method == 'xpath' else By.CSS_SELECTOR
    input_field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_method, selector)))
    current_value = input_field.get_attribute('value')

    if current_value:
        input_field.clear()  # 清除输入框中的现有内容
    input_field.send_keys(text)
    return input_field


def login_process(driver):
    """
    执行完整的登录流程并与网页进行交互
    """
    driver.get('https://220.160.53.129:8081/fdauser/user/authLogin.jsp')

    # 点击所有弹窗并处理登录
    click_element(driver, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button')  # 弹窗1
    click_element(driver, '/html/body/div[2]/div/div[3]/a[1]')  # 登录按钮
    click_element(driver, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button')  # 弹窗2
    click_element(driver, '/html/body/div[2]/div[3]/div[1]/ul/li[2]')  # 选择登录方式
    click_element(driver, '//*[@id="frdl"]')  # 切换到法人登录
    click_element(driver, '/html/body/div[6]/div[3]/a')  # 确认弹窗

    # 输入账号和密码
    input_text(driver, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input', '13285909090')
    input_text(driver, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/form/div/div[4]/div[2]/input', 'wl123321')

    # 等待验证码输入并提交登录
    time.sleep(8)
    click_element(driver, '//*[@id="submit1"]')

    # 读取数据文件
    df = pd.read_excel('data2025-02-1126.xlsx')
    print("数据框预览：")
    print(df.head())

    # 处理每个不重复的生产商
    unique_producers = df['生产商'].unique()
    for producer in unique_producers:
        print(f"\n正在处理的生产商：{producer}")
        driver.refresh() # 刷新
        click_element(driver, '//*[@id="jquery-accordion-menu"]/ul/li[2]/a') # 进入销售追溯
        click_element(driver, '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/ul/li[2]/ul/li[2]/ul/li[1]/a')  # 进入进货登记
        click_element(driver, '/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[1]/span[1]/span/span/span[1]') # 新增
        time.sleep(1)
        click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[2]')
        time.sleep(1)
        # 设置生产厂商
        input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[4]/div/div[2]/input', producer)

        # 处理当前生产商的进货记录
        producer_records = df[df['生产商'] == producer]
        for index, row in producer_records.iterrows():
            product_name = row['产品名称'] if not pd.isna(row['产品名称']) else "未知产品"
            quantity = row['进货数量'] if not pd.isna(row['进货数量']) else "未知数量"
            date = row['日期'].strftime('%Y-%m-%d') if not pd.isna(row['日期']) else "未知数量"
            date1 = row['日期'].strftime('%Y%m%d') if not pd.isna(row['日期']) else "未知数量"

            print(f"处理记录：产品名称={product_name}, 进货数量={quantity}, 生产商={producer}, 日期={date}, 日期1={date1}")

            # 输入产品名称
            time.sleep(1)
            input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[1]/td[2]/div/div[2]/input', product_name)
            # 点击查询
            time.sleep(1)
            click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[1]/form/table/tbody/tr[2]/td[3]/span[1]/span')
            # 输入日期
            time.sleep(1)
            input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[6]/div/div/div[3]/input[1]', date)
            input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[7]/div/div/div[2]/input', date1)
            # 输入数量
            input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[8]/div/div/div[3]/input[1]', quantity)
            click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/div/table/tbody/tr/td[12]/a')

        # 进入进货台账
        time.sleep(1)
        click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[1]/div[4]/div/div[1]/span[2]')
        click_element(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div[2]')

        # 处理供货方信息 用ID查找的
        time.sleep(1)
        parent_element = driver.find_element(By.ID, 'widget_stockParmeter_add_form_supplyEntName_dropdown')
        input_element = parent_element.find_element(By.CSS_SELECTOR, '[data-dojo-attach-point="textbox,focusNode"]')
        input_element.send_keys(producer)

        # 查询并提交
        time.sleep(1)
        click_element(driver, '/html/body/div[15]/div/span[1]/span/span')
        time.sleep(1)
        click_element(driver, '/html/body/div[15]/div/div[5]/div[3]/div[2]/div/table/tbody/tr')
        input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[1]/div[2]/input', '福建万鹭贸易有限公司')
        time.sleep(1)
        input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[2]/div[2]/input', '闽FZN138')
        time.sleep(1)
        input_text(driver, '/html/body/div[9]/div[2]/div[1]/div[3]/div[1]/div/div/div[2]/form/table/tbody/tr[4]/td/div[3]/div[2]/input', '13950826868')
        click_element(driver, '/html/body/div[9]/div[2]/div[2]/span[2]/span/span/span[3]')

        time.sleep(1)


if __name__ == "__main__":
    browser = init_browser()  # 初始化浏览器
    login_process(browser)  # 执行登录流程
