import tornado.ioloop
import tornado.web
import socket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("You hit " + socket.gethostname() + "\n")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    port = 8080
    app = make_app()
    print("Listening on ", str(port))
    app.listen(port, address="0.0.0.0")
    tornado.ioloop.IOLoop.current().start()
