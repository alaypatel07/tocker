import argparse
import socket
from json import dumps, loads
from pprint import pprint

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("You hit " + socket.gethostname() + "\n")


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Hostname for binding the server", type=str, default="localhost")
    parser.add_argument("port", help="Port number for binding the server", default=8080, type=int)
    parser.add_argument("reflect", help="Set this flag to true to reflect the request", type=bool, default=False)
    return parser


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


class ReflectHandler(tornado.web.RequestHandler):
    def post(self):
        response = {
            "endpoint": self.request.uri,
            "body": loads(self.request.body.decode())
        }
        self.write(dumps(response))


def make_reflect_app():
    return tornado.web.Application([
        ("/.*", ReflectHandler),
    ])


if __name__ == "__main__":
    args = get_arg_parser().parse_args()
    port = int(args.port)
    if args.reflect:
        app = make_reflect_app()
    else:
        app = make_app()
    print("Listening on hostname", args.host, "port", args.port)
    app.listen(port, address=args.host)
    tornado.ioloop.IOLoop.current().start()
