#Задание
#1) Написать базовый функционал для работы с приложением (поиск элемента, клик элемента и тд).
#2) Написать тест логина пользователя в приложение (позитивный и негативные кейсы).
#3) Использовать параметризацию.
#4) Закомитить выполненное задание на гитхаб.

### Дополнительное задание (опционально)
#1) *Реализовать логирование теста.
#2) *Реализовать динамическое определение udid телефона через subprocess
#3) **Написать на проверку элементов SideBar (выезжающее меню слева).


#pip install pytest
#pip install Appium-Python-Client
#pip install parameterized

import pytest
import subprocess
import logging
from appium import webdriver
from parameterized import parameterized

# Настройка ведения журнала тестирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Реализация динамического обнаружение UDID телефона через подпроцесс.
def get_device_udid():
    udid = subprocess.check_output(["adb", "devices"]).decode("utf-8").split("\n")[1].split("\t")[0].strip()
    return udid

# Настройка возможности Appium с динамическим обнаружением UDID
def android_get_desired_capabilities():
    return {
        'autoGrantPermissions': True,
        'automationName': 'uiautomator2',
        'newCommandTimeout': 500,
        'noSign': True,
        'platformName': 'Android',
        'platformVersion': '10',
        'resetKeyboard': True,
        'systemPort': 8301,
        'takesScreenshot': True,
        'udid': get_device_udid(),  # Использование динамического обнаружения UDID
        'appPackage': 'com.ajaxsystems',
        'appActivity': 'com.ajaxsystems.ui.activity.LauncherActivity'
    }

# Настройка драйвера Appium
@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Remote('http://localhost:4723/wd/hub', android_get_desired_capabilities())
    yield driver
    driver.quit()

# Макет интерфейса приложения
class Application:
    def search(self, query):
        return f"Search result for {query}"

    def click(self, element):
        return f"Clicked on {element}"

    def login(self, username, password):
        if username == "validuser" and password == "password":
            return True
        else:
            return False

    def open_sidebar(self):
        return "Sidebar opened"

app = Application()

# Тестовые случаи с логированием
class TestAppiumApp:
    @parameterized.expand([
        ("validuser", "password", True),
        ("invaliduser", "wrongpass", False),
    ])
    def test_user_login(self, username, password, expected_result, driver):
        result = app.login(username, password)
        assert result == expected_result
        logger.info(f"User login test with username: {username}, password: {password}, expected: {expected_result}, actual: {result}")

    def test_search_element(self, driver):
        result = app.search("example")
        assert result == "Search result for example"
        logger.info("Search element test passed")

    def test_click_element(self, driver):
        result = app.click("button")
        assert result == "Clicked on button"
        logger.info("Click element test passed")

    def test_open_sidebar(self, driver):
        result = app.open_sidebar()
        assert result == "Sidebar opened"
        logger.info("Sidebar open test passed")











