``/etc/network/interfaces``를 수정하도록 한다.

```bash
sudo vi /etc/network/interfaces 
# This file describes the network interfaces available on your system 
# and how to activate them. For more information, see interfaces(5). 

# The loopback network interface 
auto lo 
iface lo inet loopback 

# The primary network interface 
# auto eth0 
# iface eth0 inet dhcp 

# menual 
auto eth0 
iface eth0 inet static 
address 192.168.0.20 
netmask 255.255.255.0 
network 192.168.0.0 
broadcast 192.168.0.255 
gateway 192.168.0.1 

dns-nameservers 168.126.63.1 168.126.63.2 8.8.8.8 
```
이런 식으로 설정하면 된다.
