# ECE4564Assignment1Server

systemd file is using location /home/pi/ECE4564Assignment1Server

Install python3 libraries
```
sudo apt install python3-pip
sudo pip3 install wolframalpha
sudo pip3 install pyyaml
sudo pip3 install tweepy
sudo pip3 install fernet
```
config.yml needs created following exampleconfig.yml format
```
server:
  host: 127.0.0.1
  port: 5555
  app_id:<YOUR_ID>
  socketSize: 2048
client:
  host: 127.0.0.1
  port: 5555
  bearer_token:<YOUR_TOKEN>
  socketSize: 1024
```
Copy assignment1Server.service to /etc/systemd/system
```
cp assignment1Server.service /etc/systemd/system
```
Reload systemd daemon
```
sudo systemctl daemon-reload
```
Enable service
```
sudo systemctl enable assignment1Server.service
```
Start service
```
sudo systemctl start assignment1Server.service
```
