---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**

A clear and concise description of what the bug is.

**To Reproduce**

Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**

A clear and concise description of what you expected to happen.

**Screenshots**

If applicable, add screenshots to help explain your problem.

**Set-top Box:**

- Device model: [e.g. 华为悦盒 EC6108V9]
- Service provider: [e.g. China Telecom]

**Router:**

- OS: [e.g. OpenWrt]
- Python version: [e.g. 3.8]
- TellyGet version: [e.g. 1.0.0]

**Config Machine:**

- OS: [e.g. Ubuntu]
- Python version: [e.g. 3.8]
- TellyGet version: [e.g. 1.0.0]

**Media Player Machine:**

- OS: [e.g. LibreELEC]
- Media player: [e.g. Kodi with PVR IPTV Simple Client]

**IPTV Network Interface Config**

Please find and provide the corresponding section of router's network interface config file (e.g. /etc/config/network in
OpenWrt) with these fields removed:

- macaddr
- hostname

like this:

```text
config interface 'iptv_client'
        option proto 'dhcp'
        option macaddr '*****************'
        option hostname '********************************'
        option vendorid 'SCITV'
        option delegate '0'
        option ifname 'eth4'
        option metric '100'
```

**udpxy Config**

Please provide the config file of udpxy (e.g. /etc/config/udpxy in OpenWrt), like this:

```text
config udpxy
        option respawn '1'
        option status '1'
        option port '4022'
        option disabled '0'
        option source 'eth4'
        option bind 'br-lan'
        option log_file '/var/log/udpxy.log'
        option verbose '0'
        option max_clients '4'
        option mcsub_renew '180'
```

**TellyGet Config**

Please provide the config file of TellyGet (tellyget.conf) with these fields removed:

- user_id
- net_user_id
- encryption_key
- stb_id
- stb_mac

like this:

```text
[auth]
auth_url = http://182.138.3.142:8082/EDS/jsp/AuthenticationURL
user_id = **************
net_user_id = ******************
encryption_key = ********
user_group_id = 1
user_field = 2
vip = 

[device]
iptv_logical_interface = iptv_client
iptv_interface = eth4
stb_id = ********************************
stb_mac = *****************
stb_type = EC6108V9U_pub_sccdx
stb_version = HWV207013P0000
software_version = V100R003C88LSCD07B013
is_smart_stb = 0
support_hd = 1
conn_type = 4
template_name = yszhibo
area_id = 10105
lang = 1
product_package_id = 
desktop_id = 
stb_maker = 

[guide]
channel_url_prefix = http://192.168.1.1:4022/udp/
playlist_path = /etc/tellyget/playlist.m3u
xmltv_path = /etc/tellyget/xmltv.xml
channel_filters = ["^\d+$", "单音轨", "画中画", "购物", "体验", "直播室"]
remove_sd_candidate_channels = True
remove_empty_programme_channels = True
programme_name_cleanup = True
```

**tellyget-config Console Output**

Please provide the console output of tellyget-config script with these fields removed:

- macaddr
- hostname

like this:

```text
Parsing iptv.pcapng
Parsing dhcp request
Parsing auth_url request
Parsing login_url request
Generating config
Config saved to /etc/tellyget/tellyget.conf

Use the information below to configure your network interface:
proto: dhcp
macaddr: *****************
hostname: ********************************
vendorid: SCITV
metric: 100
```

**tellyget Console Output**

Please provide the console output of tellyget script with these fields removed:

- iptv_ip

like this:

```text
Bringing up logical interface: iptv_client
iptv_ip: ************
base_url: http://182.138.40.196:33200
Found 327 channels
Filtered 154 channels
Removed 1 SD candidate channels
Found 327 programmes for channel 3954
...
Removed 42 empty programme channels
Finally 130 channels left
Playlist saved to /etc/tellyget/playlist.m3u
XMLTV saved to /etc/tellyget/xmltv.xml
```

**Additional context**

Add any other context about the problem here.
