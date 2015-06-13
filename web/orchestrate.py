import os

from concurrent.futures import ThreadPoolExecutor

import tornado
from tornado import gen, web
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

import github3


class GistHandler(RequestHandler):
    @gen.coroutine
    def get(self, gist_id=None):
        # betatim/c4af33d04542f4306d38 -> c4af33d04542f4306d38
        gist_id = gist_id.split("/")[-1]
        gist = yield self.fetcher_pool.submit(github3.gist, gist_id)
        
        self.render("gist_display.html",
                    gist_id=gist_id,
                    description=gist.description,
                    files=[f for f in gist.iter_files()])

    @property
    def fetcher_pool(self):
        return self.settings['fetcher_pool']


def make_app():
    docker_host = os.environ.get('DOCKER_HOST', 'unix://var/run/docker.sock')
    
    handlers = [
        # match /gist/betatim/c4af33d04542f4306d38 or /gist/c4af33d04542f4306d38
        url(r"/gist/(\w+(?:/\w+)?)", GistHandler),
    ]

    settings = dict(fetcher_pool=ThreadPoolExecutor(4),
                )
    
    return Application(handlers, **settings)

def main():
    app = make_app()
    app.listen(7777)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
