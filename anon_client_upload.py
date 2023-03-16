import ftplib
import util

# Establishing FTP Connection
ftp = ftplib.FTP()
ftp.connect(util.SERVER_ADDRESS, util.SERVER_PORT_MP["1"]) # connect to server 1
ftp.login("anonymous", "anystring")

# Upload a file
local_file = "./client/client_file.txt"
filename = "client_file.txt"
with open(local_file, "rb") as local_file_fp:
    ftp.storbinary("STOR " + filename, local_file_fp)

# Closing FTP Connection
ftp.quit()
