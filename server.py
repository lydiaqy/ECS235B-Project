import os
import socket
import threading
import util
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class AnonConnFTPHandler(FTPHandler):
    def on_connect(self):
        super().on_connect()
        # connect to remote FTP server
        self.remote_ftp = FTP("remote.server.com")
        self.remote_ftp.login()
    
    def on_file_requested(self, file):
        # retrieve file from remote FTP server
        with self.remote_ftp.open(file, "rb") as f:
            self.send_file(f, file)

# Define FTP Server Configuration
FTP_HOST = util.SERVER_ADDRESS
FTP_HOST = "0.0.0.0"
FTP_HOST = util.SERVER_ADDRESS
FTP_PORT = util.SERVER_PORT
FTP_ROOT = "./server"

# Create FTP Authorizer and User
authorizer = DummyAuthorizer()
authorizer.add_user("user_A", "password_A", FTP_ROOT, perm="r")  # only download (r) right
authorizer.add_user("user_B", "password_B", FTP_ROOT, perm="w")  # only upload (w) right
authorizer.add_anonymous(FTP_ROOT, perm=('r', 'w'))

# Define FTP Handler
handler = FTPHandler
handler.authorizer = authorizer

# Define FTP Server
server = FTPServer((FTP_HOST, FTP_PORT), handler)

# Start FTP Server
server.serve_forever()
