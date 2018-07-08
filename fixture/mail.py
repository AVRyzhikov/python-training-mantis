import poplib  # для получения
import email   # для получения текста
import time

class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):

        for i in  range(5): # делаем несколько (5) попыток прочитать  сообщение
            pop=poplib.POP3(self.app.config['james']['host'])   # устанавливаем соединение  host получаем из конфигурации
            pop.user(username)
            pop.pass_(password)
            num=pop.stat()[0]   # количество писем Метод возвращает какую-то статистичесскую информацию  о том, что у нас имеется а вочтовом ящике
                                # первый элемент возвращаемого кортежа - количество писем в порядке убывания даты
            if num > 0:
                for n in range(num):
                    msglines=pop.retr(n+1)[1]   # второй элемент возвращаемого кортежа текст письма, список строчек
                    msgtext="\n".join(map(lambda x: x.decode('utf-8'),msglines))    # склеиваем получаем текст Это байтовые строки
                                                   # Поэтому поток байтов сначала перекодируем в обычный текст стринг
                                                   #  Фунекция map для каждого элемента из этого списка строк. Будем конвертировать в обычную строку
                    msg=email.message_from_string(msgtext)
                    if msg.get("Subject") == subject:
                        pop.dele(n+1)  # помечаем это письмо на удаление
                        pop.quit()   # quit - созакрытие сессии с сохранением close - без сохранения
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None