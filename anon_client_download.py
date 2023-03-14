import ftplib
import util

# Establishing FTP Connection using anonymous client
ftp = ftplib.FTP()
ftp.connect(host=util.SERVER_ADDRESS, port=util.SERVER_PORT_MP["1"]) # connect to server 1
ftp.login("anonymous", "anystring")

# # List directory contents
# ftp.dir()

# Download a file
remote_file = "server_file.txt"
filename = "downloaded_anon_client.txt"
localfile = open(filename, "wb")
ftp.retrbinary("RETR " + remote_file, localfile.write, 1024)
localfile.close()
# Closing FTP Connection
ftp.quit()
