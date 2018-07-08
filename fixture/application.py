from selenium import webdriver
from fixture.session import SessionHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import  MailHelper
from fixture.soup import  SoupHelper


class Application:

    def __init__(self,browser,config):

        if browser=="firefox":
            self.driver = webdriver.Firefox()
        elif browser=="chrome":
            self.driver = webdriver.Chrome()
        elif browser=="ie":
            self.driver = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)

        #self.driver.implicitly_wait(5)  # полезно только для динамических страниц, когда страница появилась,
                                         # а элементы еще нет.

        self.config = config
        self.base_url = config['web']['baseUrl']

        self.session=SessionHelper(self) # помощник получает ссылку на объект
                                         # класса Application
        self.james=JamesHelper(self)

        self.signup = SignupHelper(self)

        self.mail= MailHelper(self)

        self.soup = SoupHelper(self)










    def is_valid(self):
        try:
            self.driver.current_url
            return True
        except:
            return False

    def open_home_page(self):
        driver = self.driver
        driver.get(self.base_url)
        #driver.get("http://localhost/addressbook")



    def destroy(self):
        self.driver.quit()
