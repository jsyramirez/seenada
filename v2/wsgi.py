'''wsgi to call api.py'''
from api import APP

if __name__ == '__main__':
    APP.run()
