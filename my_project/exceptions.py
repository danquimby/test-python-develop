class NotFondUserException(Exception):
    def __init__(self, phone):
        super().__init__(f'Not found user by phone:{phone}')


class NotFondCountryException(Exception):
    def __init__(self, name):
        super().__init__(f'Not found country name:{name}')
