import util
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import ftplib

import os
import sys

from parse_graph import is_subject, parse_input

import shutil

REMOTE_SERVER_PORT = {}
FTP_DIRECTORY_FILES = {}
DIRECTLY_ACCESSIBLE_OBJECTS = {}
SERVER_DIRECTORY = ""

STOR_COMPLETE_FILE_PATH = ""

class AnonConnFTPHandler(FTPHandler):

    def on_connect(self):
        pass
        # self.remote_ftps = {}
        # for remote_ftp_port in REMOTE_SERVER_PORT.keys():
        #     remote_ftp = ftplib.FTP()
        #     remote_ftp.connect(util.SERVER_ADDRESS, remote_ftp_port)
        #     remote_ftp.login("anonymous", "anystring") # anonymous connection
        #     self.remote_ftps[remote_ftp_port] = remote_ftp

    def ftp_RETR(self, complete_file_path):
        print("RETR requested for: ", complete_file_path)
        complete_file_path_content = complete_file_path.split("/") # Unix-based
        file_name_with_ports = complete_file_path_content[-1]

        file_name_with_ports_content = file_name_with_ports.split(":")
        file_name = file_name_with_ports_content[0]
        remote_ftp_ports = file_name_with_ports_content[1:]
        local_file_path = SERVER_DIRECTORY + "/" + file_name

        print("Local file path: ")
        print(local_file_path)
        print("Remote ftp ports: ")
        print(remote_ftp_ports)

        if file_name in DIRECTLY_ACCESSIBLE_OBJECTS: 
            print("Directly accessible file found")
            shutil.copy(os.path.join(util.NODE_OBJECT_DIRECTORY, file_name), SERVER_DIRECTORY)
            FTP_DIRECTORY_FILES[file_name] = True

        if file_name in FTP_DIRECTORY_FILES:
            print("File found locally, retrieving")
            super().ftp_RETR(local_file_path)
        elif len(remote_ftp_ports) > 0: # forwarding request is possible
            print("forwarding")
            remote_ftp_port = int(remote_ftp_ports[0])
            remote_ftp_ports = ':'.join(remote_ftp_ports[1:])
            with open(local_file_path, "wb") as local_file_fp:
                remote_file_name = file_name
                if len(remote_ftp_ports) > 0:
                    remote_file_name = remote_file_name + ":" + remote_ftp_ports
                remote_ftp = ftplib.FTP()
                remote_ftp.connect(util.SERVER_ADDRESS, remote_ftp_port)
                remote_ftp.login("anonymous", "anystring") # anonymous connection
                remote_ftp.retrbinary("RETR " + remote_file_name, local_file_fp.write, 1024) # now local server has the file
                remote_ftp.quit()
            super().ftp_RETR(local_file_path)

        # for remote_ftp_port in REMOTE_SERVER_PORT.keys():
        #     self.remote_ftps[remote_ftp_port].quit()

    def ftp_STOR(self, complete_file_path):
        # we do this because `complete_file_path` doesn't contain the forwarding ports
        global STOR_COMPLETE_FILE_PATH
        STOR_COMPLETE_FILE_PATH = complete_file_path 

        print("STOR requested for: ", complete_file_path)
        complete_file_path_content = complete_file_path.split("/")
        file_name_with_ports = complete_file_path_content[-1]

        file_name_with_ports_content = file_name_with_ports.split(":")
        file_name = file_name_with_ports_content[0]
        remote_ftp_ports = file_name_with_ports_content[1:]
        local_file_path = SERVER_DIRECTORY + "/" + file_name

        print("Local file path: ")
        print(local_file_path)
        print("Remote ftp ports: ")
        print(remote_ftp_ports)

        super().ftp_STOR(local_file_path)
          
    def on_file_received(self, complete_file_path):
        global STOR_COMPLETE_FILE_PATH
        complete_file_path = STOR_COMPLETE_FILE_PATH
        print("on file received for: ", complete_file_path)

        complete_file_path_content = complete_file_path.split("/")
        file_name_with_ports = complete_file_path_content[-1]

        file_name_with_ports_content = file_name_with_ports.split(":")
        file_name = file_name_with_ports_content[0]
        remote_ftp_ports = file_name_with_ports_content[1:]
        local_file_path = SERVER_DIRECTORY + "/" + file_name

        if len(remote_ftp_ports) > 0: # continue to send data
            remote_ftp_port = int(remote_ftp_ports[0])
            remote_ftp_ports = ':'.join(remote_ftp_ports[1:])
            with open(local_file_path, "rb") as local_file_fp:
                remote_file_name = file_name
                if remote_ftp_ports != "":
                    remote_file_name = remote_file_name + ":" + remote_ftp_ports
                self.remote_ftps[remote_ftp_port].storbinary("STOR " + remote_file_name, local_file_fp)
        for remote_ftp_port in REMOTE_SERVER_PORT.keys():
            self.remote_ftps[remote_ftp_port].quit()

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Please provide ftp server port and directory")
        sys.exit("ftp server port and directory not found.")

    SERVER_DIRECTORY = sys.argv[1]
    ftp_server_port = int(sys.argv[2])
    graph = parse_input(util.INPUT_FILE)
    
    remote_ftp_server_ports_with_rights = sys.argv[3:]
    for i in range(0, len(remote_ftp_server_ports_with_rights), 2):
        remote_ftp_server_port = remote_ftp_server_ports_with_rights[i]
        remote_ftp_server_port_rights = util.REMOTE_FTP_PORT_RIGHT_MP[int(remote_ftp_server_ports_with_rights[i + 1])]
        if int(remote_ftp_server_port) != ftp_server_port:
            node_number = int(remote_ftp_server_port[-1])
            if is_subject(node_number, graph.num_subjects):
                REMOTE_SERVER_PORT[int(remote_ftp_server_port)] = remote_ftp_server_port_rights
            else: 
                DIRECTLY_ACCESSIBLE_OBJECTS[util.NODE_OBJECT_FILE_PREFIX + str(node_number)] = remote_ftp_server_port_rights

    FTP_DIRECTORY_FILES_list = os.listdir(SERVER_DIRECTORY)
    for file in FTP_DIRECTORY_FILES_list:
        FTP_DIRECTORY_FILES[file] = True

    print("Remote ports connected to {}: {}".format(ftp_server_port, REMOTE_SERVER_PORT))
    print("Files in FTP Directory {} for server port {}: {}".format(SERVER_DIRECTORY, ftp_server_port, FTP_DIRECTORY_FILES))
    print(f"Directly accessible objects for {ftp_server_port}: {DIRECTLY_ACCESSIBLE_OBJECTS}")

    # Local server config
    local_authorizer = DummyAuthorizer()
    local_authorizer.add_anonymous(SERVER_DIRECTORY, perm=('r', 'w'))
    local_handler = AnonConnFTPHandler # 2
    local_handler.authorizer = local_authorizer
    local_handler.log_prefix = '[server_port = {}] '.format(ftp_server_port) + '[connection = [%(username)s]@%(remote_ip)s:%(remote_port)s]'

    # create FTP server and serve
    server = FTPServer((util.SERVER_ADDRESS, ftp_server_port), local_handler) # 1 -> Change later
    server.serve_forever()