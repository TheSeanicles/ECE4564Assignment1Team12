# ECE4564Assignment1Server

systemd file is using location /home/pi/ECE4564Assignment1Server

copy assignment1Server.service to /etc/systemd/system
```
cp assignment1Server.service /etc/systemd/system
```

install wolframalpha and yaml python3 library
```
sudo apt install python3-pip
sudo pip3 install wolframalpha
sudo pip3 install pyyaml
```

reload systemd daemon
```
sudo systemctl daemon-reload
```

enable service
```
sudo systemctl enable assignment1Server.service
```

start service
```
sudo systemctl start assignment1Server.service
```

config.yml needs created following exampleconfig.yml format

```
server:
  host: 127.0.0.1
  port: 5555
  app_id:
  socketSize: 2048
client:
  host: 127.0.0.1
  port: 5555
  bearer_token: 
  socketSize: 1024
```
