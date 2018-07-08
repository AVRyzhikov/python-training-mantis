from suds.client import Client
from suds import WebFault    # это исключения, который выбрасываются в случае, если что-то пошло не так
                             # если не удалось зарегистрироваться в системе, например
class SoupHelper:
    def __init__(self,app):
        self.app=app

    def can_login(self,username,password):
        client =Client("http://localhost/mantisbt-1.2.19/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username,password)
            return True
        except WebFault:
            return False