# TERMINAL BASED PENETRATION TESTING TOOL FOR WIFI NETWORKS AND WARDRIVING
## This tool allows for:
* `DEAUTHETICATION ATTACK`
* `FAKE AUTHENTICATION ATTACK`
* `FAKE SSID SPAM`
* `MAC ADDRESS OUI LOOKUP`
* `WARDRIVING`
* `PACKET SNIFFING`
## Necessary dependecies
### For the app to launch you need:
* `scapy` 
```bash
sudo apt install python3-scapy
``` 
* `shapely`
```bash
sudo apt install python3-shapely
``` 
* `gpsd`
```bash
sudo apt install python3-gps gpsd
``` 

## Usage:
### WARNING!!!
This app has to be launched as root or with sudo
```bash
 sudo python3 main.py -i wlan0 -o capture.csv #example command
```
### Launch options:
* `-i` specify your network interface that you know supports packet injection
* `-o` specify wardriving output file
* `-c` specify a network channel
* `-l` larp mode 
### LARP MODE?!
This mode basically allows to use the app without a network interface and a gps, it fills the data with imaginary values. This way y'all skids can use it and look cool infront of your fake friends :)
### How to traverse the UI:
While on the main screen every `10s` it refreshes the found networks. By pressing the `S` key it allows you to use `ARROW-UP` and `ARROW-DOWN` to select a desired network. You can select the network by pressing the `ENTER` key. After an attack menu will be displayed for you. You can traverse through the menu using `ARROWS` and pressing `ENTER` to select the attack. To go back you can simply press the `BACKSPACE` or `ARROW-LEFT` key.
### Other options:
* pressing `p` start the packet sniffer
* pressing `f` while packet sniffing allows for packet filtering
* pressing `r` resets filters while in packet sniffing mode
* pressing `t` shows a detailed gps info
* pressing `q` or `CTRL+c` quits the app
* pressing `g` while in deauth mode allows to deauth a chosen device
## IMAGES
<p float="left">
    <img src="./images/Screenshot 2026-07-16 at 9.28.48 PM.png" width="35%">
    <img src="./images/Screenshot 2026-07-16 at 9.31.25 PM.png" width="35%">
    <img src="./images/Screenshot 2026-07-16 at 9.29.00 PM.png" width="35%">
</p>