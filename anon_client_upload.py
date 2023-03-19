import ftplib
import util
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("FTP server port or file for client not provided")
        sys.exit("FTP server port or file for client not found")

    ftp_server_port = int(sys.argv[1])
    remote_file = sys.argv[2] # "./client/client_file.txt:50002:50003"

    local_file_contents = remote_file.split(":")
    filename = local_file_contents[0] # ./client/client_file.txt
    
    local_file_contents = remote_file.split("/")
    remote_file = local_file_contents[2] # client_file.txt:50002:50003

    # Establishing FTP Connection
    ftp = ftplib.FTP()
    ftp.connect(util.SERVER_ADDRESS, ftp_server_port) # connect to server 1
    ftp.login("anonymous", "anystring")

    # Upload a file
    with open(filename, "rb") as local_file_fp:
        ftp.storbinary("STOR " + remote_file, local_file_fp)

    # Closing FTP Connection
    ftp.quit()
