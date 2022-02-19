# ECE4564Assignment1Server

systemd file is using location /home/pi/ECE4564Assignment1Server

copy assignment1Server.service to /etc/systemd/system
```
cp assignment1Server.service /etc/systemd/system
```

install wolframalpha and yaml python3 library
```
sudo apt install python3-pip
pip3 install wolframalpha
pip3 install pyyaml
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
