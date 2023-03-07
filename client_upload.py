import ftplib

# Choose user
char = input("Please input your user id: ")
user_id = "user_" + char # B
password = "password_" + char # B

# Establishing FTP Connection
ftp = ftplib.FTP("0.0.0.0")
ftp.login(user_id, password)

# Upload a file
local_file = "/Users/pmh/Yun/ECS235B_computer_security/project/client/client_file.txt"
filename = "uploaded.txt"
ftp.storbinary("STOR " + filename, open(local_file, "rb"))

# Closing FTP Connection
ftp.quit()
