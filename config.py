from enum import Enum

token = '1788775786:AAEzwQ8HkU46qUmXHtRsOvvz8zd3HjIcZoU'
db_file = 'database.vdb'


class States(Enum):
    S_START = "1"
    S_ENTER_FIELD = "2"
    S_TYPE_OF_INFO = "3"
    S_ENTER_TYPE_OF_CONTENT = "4"
    S_ENTER_SUBTOPICS_LIST = "5"