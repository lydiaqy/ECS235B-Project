# ECS235B-Project

## Usage: 
Server1: python server.py ./server_50000 50000 50002
Server2: python server.py ./server_50002 50002 50003
Server3: python server.py ./server_50003 50003

Donwload client for no switching: python anon_client_download.py 50000 random1 
Download client for switching: python anon_client_download.py 50000 server_50003_file.txt:50002:50003
