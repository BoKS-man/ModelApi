class ApiException(Exception):
    def __init__(self, message:str, status:int=200):
        self.__status = status
        super().__init__(message)

    @property
    def status(self):
        return self.__status