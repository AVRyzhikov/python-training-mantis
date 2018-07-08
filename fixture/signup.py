
import re
class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, password, email):
        driver=self.app.driver
        driver.get(self.app.base_url+"/signup_page.php")
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_css_selector('input[type="submit"]').click()

        mail=self.app.mail.get_mail(username,password,"[MantisBT] Account registration")
        # ивлекаем из письма ссылку
        url=self.extract_confirmation_url(mail)
        driver.get(url)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_name("password_confirm").send_keys(password)
        driver.find_element_by_css_selector('input[value="Update User"]').click()

    def extract_confirmation_url(self,text):
        s= re.search("http://.*$",text,re.MULTILINE).group(0)
        return re.search("http://.*$",text,re.MULTILINE).group(0) # http:// и какое-то количество символов до конца строки
                                              # из text извлекаем мцеликом все, что подходит  под  это регулярное выражение,
                                              # т.е group(0)






