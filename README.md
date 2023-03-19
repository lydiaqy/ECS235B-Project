# ECS235B-Project

## Usage - Server: 
1. Server1: python server.py ./server_50000 50000 50002
2. Server2: python server.py ./server_50002 50002 50003
3. Server3: python server.py ./server_50003 50003

## Usage - Client Download:
1. Download client for no switching: python anon_client_download.py 50000 random1 
2. Download client for switching: python anon_client_download.py 50000 server_50003_file.txt:50002:50003

## Usage - Client Upload:
1. Upload client for no switching: python anon_client_upload.py 50000 ./client/client_file.txt
2. Upload client for switching: python anon_client_upload.py 50000 ./client/client_file.txt:50002:50003

## To clean objects and subject_* directories:

```
make clean
```

## To verify existence of FTP servers:

In a different terminal tab, run:

```
ps u | grep subject
```
