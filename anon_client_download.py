import ftplib
import util
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("FTP server port or file for client not provided")
        sys.exit("FTP server port or file for client not found")

    ftp_server_port = int(sys.argv[1])
    remote_file = sys.argv[2] # "server_50002_file.txt:50002"

    # Establishing FTP Connection using anonymous client
    ftp = ftplib.FTP()
    ftp.connect(host=util.SERVER_ADDRESS, port=ftp_server_port) # connect to server 1
    ftp.login("anonymous", "anystring")

    # # List directory contents
    # ftp.dir()

    # Download a file
    filename = "downloaded_anon_client.txt"
    localfile = open(filename, "wb")
    ftp.retrbinary("RETR " + remote_file, localfile.write, 1024)
    localfile.close()
    # Closing FTP Connection
    ftp.quit()
