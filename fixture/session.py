from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SessionHelper:

    # конструктор класса
    def __init__(self,app):
        self.app=app
        self.app.open_home_page()

    def loginm(self, username, password):
        driver = self.app.driver
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        driver = self.app.driver
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        #element=driver.find_element_by_link_text("Logout")
        element.click()
        #driver.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        driver = self.app.driver
        # проверяем а мы все еще находимся внутри активной сессии  или уже снаружи
        # есть ли на странице ссылка logout
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        driver = self.app.driver
        elements=driver.find_elements_by_link_text("Logout")
        return len(elements) > 0

    def is_logged_in_as(self,username):
        driver = self.app.driver
        return self.get_logged_user()==username
        #return driver.find_element_by_xpath("//div/div[1]/form/b").text=="("+username+")"

    def get_logged_user(self):
        driver = self.app.driver
        return driver.find_element_by_css_selector("td.login-info-left span").text # обрезка первого и последнего символа

    def ensure_login(self, username,password):
        driver = self.app.driver
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()

        self.loginm(username,password)

