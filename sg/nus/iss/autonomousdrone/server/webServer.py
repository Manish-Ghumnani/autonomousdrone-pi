import tornado

from sg.nus.iss.autonomousdrone.flight.flight_commands import FlightCommands


class WebServer(tornado.websocket.WebSocketHandler):

    def __init__(self, vehicle):
        self.__flight_commands = FlightCommands(vehicle)


    def check_origin(self, origin):
        return True

    def open(self):
        print ("connection opened")
        self.write_message("connection opened")

    def on_message(self, message):
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
        handlers = [
            (r'/websocket', tornado.WebSocketHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8085)
    tornado.ioloop.IOLoop.instance().start()