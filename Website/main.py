import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from datetime import datetime
import socket
from threading import Thread



class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        
        socket_address = ('127.0.0.1', 5000)
        self.run_socket_client(socket_address, data)

        
            
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())
    
    @staticmethod
    def run_socket_client(server_address, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.sendto(data, server_address)
        print(f'Send data: {data.decode()} to server: {server_address}')
        sock.close()


def server_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)

    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        
            with open('storage/data.json', 'r') as file:
                if file.read():
                    file.seek(0)
                    messages = json.load(file)
                else:
                    messages = {}
            
            with open('storage/data.json', 'w', newline='') as file:
                curent_time = str(datetime.now())
                messages.update([(curent_time, (data_dict))])
                json.dump(messages, file)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def run(server_class=HTTPServer, handler_class=HttpHandler):

    socket_address = ('127.0.0.1', 5000)
    thread = Thread(target=server_socket, args=(socket_address))
    thread.start()
    
    
    server_address = ('localhost', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        thread.join()
        print('thread has closed')
        http.server_close()
        print('server has closed')

if __name__ == '__main__':
    print('server has started')
    run()
    