# TERMINAL BASED PENETRATION TESTING TOOL FOR WIFI NETWORKS AND WARDRIVING
## This tool allows for:
* `DEAUTHETICATION ATTACK`
* `FAKE AUTHENTICATION ATTACK`
* `FAKE SSID SPAM`
* `MAC ADDRESS OUI LOOKUP`
* `WARDRIVING`
* `PACKET SNIFFING`
* `HANDSHAKE CAPTURE`
* `MISC ATTACKS`<br>
ALL JUST BY USING SCAPY!
## IMAGES
<p float="left">
    <img src="./images/Screenshot 2026-07-16 at 9.28.48 PM.png" width="30%">
    <img src="./images/Screenshot 2026-07-16 at 9.31.25 PM.png" width="30%">
    <img src="./images/Screenshot 2026-07-16 at 9.29.00 PM.png" width="30%">
</p>
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
### Why did my handshake capture window close?
The window closes 5s after a handshake was captured
### How to traverse the UI:
While on the main screen every `10s` it refreshes the found networks. By pressing the `S` key it allows you to use `ARROW-UP` and `ARROW-DOWN` to select a desired network. You can select the network by pressing the `ENTER` key. After an attack menu will be displayed for you. You can traverse through the menu using `ARROWS` and pressing `ENTER` to select the attack. To go back you can simply press the `BACKSPACE` or `ARROW-LEFT` key.
### Other options:
* pressing `p` start the packet sniffer `ARROW-KEYs` change the scroll speed
* pressing `f` while packet sniffing allows for packet filtering
* pressing `r` resets filters while in packet sniffing mode
* pressing `t` shows a detailed gps info
* pressing `q` or `CTRL+c` quits the app
* pressing `g` while in deauth mode allows to deauth a chosen device
* pressing `m` while in the main menu shows misc attacks menu
### You don't have a GPS module?
For this app to work it's not necessary to have a GPS module, but it's highly recomended. If you want to buy one that you know that works here is a link you can use to find a suitable module:

https://www.amazon.pl/Geekstory-odbiornik-satelitarnej-kompatybilny-Mikrokontroler/dp/B07PRGBLX7?__mk_pl_PL=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1OVB2C83HYNV1&dib=eyJ2IjoiMSJ9.jhvYT2SnMWd9L05Oef_jkkHcUzpN7JV9vEOk2JZ-RsytcG42gNHOnQrqIcAWzAIDjaVbcomu3Yr-BVmsuShWn6PpeCOTHWng9WG7ZoC34gLU43W3koO7RkyXDX93UhpNO-8OIPbeUo1cyXG4eXF-NnHzEUhdIeSyErGQPZOtyONcdjGsYoZvdtJ5MruaWx84OLfwaQDpLpmuR5eRnG83JgZBkGSFqb_ZDpkAD2BCvaG1aC2IlvzHp3LXISFnw3mPP0IGI9jrkWS2XGH6piU2F1o_CKJwYN05_wGhMgZh_6g.-bI934tuoMT1kVOr1h3BoN22S7ThrQB_zAWTsTwBENc&dib_tag=se&keywords=gps+module&qid=1787491430&sprefix=gps+module%2Caps%2C143&sr=8-30

