import ftplib
import util

# Establishing FTP Connection
ftp = ftplib.FTP()
ftp.connect("0.0.0.0", util.SERVER_PORT)
ftp.login("anonymous", "anystring")

# Upload a file
local_file = "./client/client_file.txt"
filename = "uploaded.txt"
ftp.storbinary("STOR " + filename, open(local_file, "rb"))

# Closing FTP Connection
ftp.quit()
