#__init__.py
from presentation.ua_lang_controller import Controller

if __name__ == '__main__':
    c = Controller()
    while True:
        c.execute()
