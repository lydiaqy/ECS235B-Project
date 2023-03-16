import util
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import ftplib

# remote_server_number = input("Enter remote server number: ") # 2
REMOTE_SERVER_PORT = util.SERVER_PORT_MP["2"]

class AnonConnFTPHandler(FTPHandler):

    def on_connect(self):
        self.remote_ftp = ftplib.FTP()
        self.remote_ftp.connect(util.SERVER_ADDRESS, REMOTE_SERVER_PORT)
        self.remote_ftp.login("anonymous", "anystring") # anonymous connection

    def ftp_RETR(self, complete_file_path):
        print("RETR requested for: ", complete_file_path)
        file_name = complete_file_path.split("/")[-1] # Unix-based
        local_file_path = util.SERVER_DIRECTORY + "/" + file_name
        local_file_fp = open(local_file_path, "wb")
        self.remote_ftp.retrbinary("RETR " + file_name, local_file_fp.write, 1024) # now local server has the file
        local_file_fp.close()
        self.remote_ftp.quit()
        super().ftp_RETR(local_file_path)

    def ftp_STOR(self, complete_file_path):
        print("STOR requested for: ", complete_file_path)
        file_name = complete_file_path.split("/")[-1]
        local_file_path = util.SERVER_DIRECTORY + "/" + file_name
        super().ftp_STOR(local_file_path)
          
    def on_file_received(self, complete_file_path):
        print("on file received for: ", complete_file_path)
        file_name = complete_file_path.split("/")[-1]
        local_file_path = util.SERVER_DIRECTORY + "/" + file_name
        with open(local_file_path, 'rb') as local_file_fp:
            self.remote_ftp.storbinary("STOR " + file_name, local_file_fp)
        self.remote_ftp.quit()

# Local server config
local_authorizer = DummyAuthorizer()
local_authorizer.add_anonymous(util.SERVER_DIRECTORY, perm=('r', 'w'))
local_handler = AnonConnFTPHandler # 2
local_handler.authorizer = local_authorizer

# create FTP server and serve
server = FTPServer((util.SERVER_ADDRESS, util.SERVER_PORT_MP["1"]), local_handler) # 1 -> Change later
server.serve_forever()