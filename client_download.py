import ftplib
import util

# Choose user
char = input("Please input your user id: ")
user_id = "user_" + char # A
password = "password_" + char # A

# Establishing FTP Connection
ftp = ftplib.FTP()
ftp.connect(host="0.0.0.0", port=util.SERVER_PORT)
ftp.login(user_id, password)

# # List directory contents
# ftp.dir()

# Download a file
remote_file = "server_file.txt"
filename = "downloaded.txt"
localfile = open(filename, "wb")
ftp.retrbinary("RETR " + remote_file, localfile.write, 1024)
localfile.close()

# Closing FTP Connection
ftp.quit()
