import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
from dronekit import Vehicle
from sg.nus.iss.autonomousdrone.flight.flight_commands import FlightCommands

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebServer(tornado.websocket.WebSocketHandler):
    #def __init__(self):
     #   vehicle = Vehicle()
      #  self.__flight_commands = FlightCommands(vehicle)
    #handle = HandleCommands()
    def check_origin(self, origin):
        return True

    def open(self):
        print ("connection opened")
        self.write_message("connection opened")

    def on_message(self, message):
        self.__flight_commands = FlightCommands()
        print (message)
        if(message == "arm"):
            print ("Arming")
            self.__flight_commands.arm()

        if(message == "disarm"):
            print ("Disarm")
            self.__flight_commands.disarm()

    def on_close(self):
        print ("connection closed")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', IndexHandler),
            (r'/websocket', WebServer)
        ]

        tornado.web.Application.__init__(self, handlers)

if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8085)
    tornado.ioloop.IOLoop.instance().start()
