import time
import random
import json
import datetime
import os
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint



class WebSocketHandler(websocket.WebSocketHandler):

  def check_origin(self, origin):
    return True
  
  def open(self):
    print ('Connection established.')
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), self.send_data)

  def on_close(self):
    print ('Connection closed.')

  def check_origin(self, origin):
    return True

  def send_data(self):
    print ("Sending Data")

    file = open ("download.log", "r")
    for line in file:
      if line.startswith("\t\t\t\t\t\"end\""):
        x = float(line.replace("\t\t\t\t\t\"end\":", "").replace(",", ""))
      elif line.startswith("\t\t\t\t\t\"bits_per_second\""):
        y = float(line.replace("\t\t\t\t\t\"bits_per_second\":", "").replace(",", ""))

        point_data = {
          "x": x,
          "y": y,
        }

        self.write_message(json.dumps(point_data))

        print (point_data)
        time.sleep(1)

if __name__ == "__main__":
  print ("Starting websocket server program. Awaiting client requests to open websocket ...")
  application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                 (r'/websocket', WebSocketHandler)])
  application.listen(8001)
  ioloop.IOLoop.instance().start()