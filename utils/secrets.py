# store some Secrets
class Secrets:
    class Email:
        emailHost = 'smtp.126.com'
        emailPort = 25
        emailAddr = 'DovahkiinGA@126.com'
        emailPasswd = ''

    class RootUrl:
        Frontend = 'http://127.0.0.1:8080'
        Backend = 'http://127.0.0.1:8080'


class Settings:
    SECRET_KEY = 'django-insecure-j$25)6it^$87hp7x(9!khs#^3ng&u%cloka*kdotv*shpvm7y1'
    # todo:check secret key

class Database:
    ENGINE = 'django.db.backends.mysql'
    NAME = 'backend'
    USER = 'meowmeow'
    PASSWORD = ''
    HOST = ''
    PORT = '3306'
