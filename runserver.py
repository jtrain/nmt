from bottle import route, run

import settings
import urls

urls.register_urls()

if __name__ == '__main__':
    run(host=settings.HOST, port=settings.PORT)
