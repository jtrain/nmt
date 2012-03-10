from bottle import route, run

import settings

@route('/')
def index():
    return "helo world"

if __name__ == '__main__':
    run(host=settings.HOST, port=settings.PORT)
