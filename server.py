import os
import socket
import threading
import util
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import ftplib

import threading

# remote_server_number = input("Enter remote server number: ") # 2
REMOTE_SERVER_PORT = util.SERVER_PORT_MP["2"]

class AnonConnFTPHandler(FTPHandler):

    def on_connect(self):
        self.remote_ftp = ftplib.FTP()
        self.remote_ftp.connect(util.SERVER_ADDRESS, REMOTE_SERVER_PORT)
        self.remote_ftp.login("anonymous", "anystring") # anonymous connection

    def ftp_RETR(self, file):
        print("RETR requested for: ", file)
        remote_file = file.split("/")[-1] # Unix-based
        filename = util.SERVER_DIRECTORY + "/" + "server_file_50002.txt"
        localfile = open(filename, "wb")
        self.remote_ftp.retrbinary("RETR " + remote_file, localfile.write, 1024)
        localfile.close()
        self.remote_ftp.quit()
        super().ftp_RETR("server/server_file_50002.txt")

# Local server config
local_authorizer = DummyAuthorizer()
local_authorizer.add_anonymous(util.SERVER_DIRECTORY, perm=('r', 'w'))
local_handler = AnonConnFTPHandler # 2
local_handler.authorizer = local_authorizer

# create FTP server and serve
server = FTPServer((util.SERVER_ADDRESS, util.SERVER_PORT_MP["1"]), local_handler) # 1 -> Change later
server.serve_forever()