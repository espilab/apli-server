#
#  apli-server.py --- 
#
# sample code from Bing chat.
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

import datetime
import shutil

# global var.
disk_name = "C:/"
homepage_file = 'home.html'


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # in here, do any process with using form
        if "cmd" in form:
          cmd = form.getvalue('cmd')
          response = make_response(cmd, form)
        else: 
          response = "This is the POST request.  cmd ot found."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        #response = "This is the POST request. Data: %s" % postvars, 'utf-8')
        self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        #self.end_headers()
        #response = bytes("This is the GET request.", 'utf-8')
        #self.wfile.write(response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = make_response_homepage()
        self.wfile.write(response.encode('utf-8'))

def run():
    print('apli-server starting...(press Ctrl-C to abort)')
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


# -------- functions for your application --------
def current_date():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%H:%M:%S")
    return (formatted_date, formatted_time)


# return home-page contents
def make_response_homepage():
    global homepage_file
    with open(homepage_file, 'r', encoding='utf-8') as f:
        response = f.read()
    return response


def make_response(command_str, form):
    response_str = 'cmd=' + command_str + "\n"

    if command_str == 'datetime':
        (date_str, time_str) = current_date()
        response_str += 'datetime=' + date_str + ',' + time_str + "\n"
    if command_str == 'disk_usage':
        (total, used, free) = check_disk_usage()
        response_str += 'total=' +  str(total) + "\n"
        response_str += 'used=' +  str(used) + "\n"
        response_str += 'free=' +  str(free) + "\n"

    return response_str


def check_disk_usage():
  global disk_name
  usage = shutil.disk_usage(disk_name)
  total = usage.total
  used = usage.used
  free = usage.free
  return (total, used, free)


if __name__ == '__main__':
    run()
