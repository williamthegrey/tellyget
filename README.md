# TellyGet

A toolset for fetching and updating m3u playlist and xmltv guide from the IPTV network.

## Background

### Disadvantages of IPTV Set-top Boxes

IPTV set-top boxes are fully controlled by the service providers, and you do not have the freedom to do what you want,
like:

- removing unwanted TV channels (e.g. advertising channels and shopping channels)
- playback on your favorite media players (e.g. Kodi and Plex) for extra features like:
    - stopping your parents from getting confused by two remotes (one for set-top box and one for TV), and controlling
      the playback only with the TV remote
    - time shifting without VIP
    - recording the programs
    - playback on multiple TVs at the same time without purchasing extra set-top boxes
    - playback on multiple smart devices (e.g. phones, tablets and computers) at the same time
    - playback even when not at home

Now you can achieve all of them above, once you have installed TellyGet and these applications:

- Wireshark and tshark
- xTeVe
- udpxy
- media players which support xTeVe (e.g. Kodi and Plex)

### How TellyGet Works

TellyGet consists of two executable scripts:

- tellyget-config: parsing network packets sent by the set-top box and generating the config file for tellyget
- tellyget: using the config file to imitate the set-top box's booting and channel fetching behaviors

Here is the data flow for tellyget-config:

![diagram-tellyget-config](resource/diagram-tellyget-config.svg)

As we can see, tellyget-config:

- parses the pcapng file captured by Wireshark during the set-top box's booting
- generates the config file for tellyget from the parsed information
- runs once and for all

And here is the data flow for tellyget:

![diagram-tellyget](resource/diagram-tellyget.svg)

As we can see, tellyget:

- independently runs on a different setup where the set-top box is absent
- fetches and updates m3u playlist and xmltv guide from the IPTV network
- is supposed to run regularly (e.g. every day)

## Compatibility

### Service Provider Compatibility

TellyGet is compatible only with China Telecom as the IPTV service provider.

### Set-top Box Compatibility

TellyGet is currently tested on these set-top boxes:

- 华为悦盒 EC6108V9

## Hardware Requirements

tellyget is recommended to run on a router or a family server (we will refer to both of them as "the router" below)
for serving every day. If you run it on a family server, two network ports (which means two physical network interfaces)
at least on this server are recommended, in case you want this server to connect to the IPTV network and the network
called "the Internet" at the same time.

tellyget-config can run on the router mentioned above or any other machines separately (we will refer to this machine
as "the config machine").

## Install

### Install External Dependencies

On the config machine, you should install tshark as external dependency first. tshark is usually installed alongside
with Wireshark. And you should add it to PATH environment variable after installation.

### Install TellyGet

Currently, tellyget-config and tellyget are always installed together. So, if your config machine and your router are
not the same machine, you must install the whole TellyGet on both of the machines separately.

Use this command to install TellyGet from PyPI:

```shell
pip3 install tellyget
```

### Install Other Applications

On the router, install udpxy if you have not.

On any machines, install these applications if you have not:

- xTeVe
- media players which support xTeVe, like:
    - Kodi: with the installation of "PVR IPTV Simple Client" add-on required
    - Plex

## Usage

### Capture the Network Packets

There are many ways to capture network packets during the set-top box's booting. And a general approach is given here:

- Bridge two physical interfaces of the router
- Connect one interface to the modem
- Connect the other one to the turned off set-top box
- Use the "SSH remote capture" function of Wireshark to capture network packets
- The "Remote interface" option is set to either of the two interfaces mentioned above
- Turn on the set-top box and wait for it booting to its home screen
- Save the packets to a pcapng file (here we will call it iptv.pcapng)
- Disconnect the modem and the set-top box from the router
- Now the router's configuration is useless, so restore it if you don't want to waste those two interfaces

### Generate the Config File for tellyget

Find out the mac address of your set-top box at the bottom of it, and we will call it `<stb_mac>`.

On the config machine, use this command to generate the config file for tellyget:

```shell
tellyget-config iptv.pcapng <stb_mac> /etc/tellyget/tellyget.conf
```

### Connect to the IPTV Network

In order to connect to the IPTV network without the set-top box, you need to create a network interface on the router.
Use the hint given by tellyget-config at the end of its execution to accomplish that. And the fields in the hint are
given in the naming conventions of OpenWrt to help you to identify them.

The network interface mentioned above is call "logical network interface" in OpenWrt (here we call it "IPTV logical
network interface"), and is assigned to one or more physical network interfaces. In our case, assigning it to one is
enough (here we call it "IPTV physical network interface").

Before connecting the IPTV physical network interface to the modem, there are a couple of things you need to know:

The IPTV network and the Internet are different networks in many ways, and they are supposed to be separated from each
other. In fact, they cannot work together because of the overlapping IP addresses. But don't worry. On one hand, udpxy
(its configuration will be explained later) and the tellyget script you are about to execute is bound to the IPTV
physical network interface, so they will never send any packets to the Internet. On the other hand, you should set a
higher metric on the IPTV logical network interface than your WAN (another logical network interface which is connected
to the Internet) to ensure the packets intended for the Internet would not be sent to the IPTV network.

Now connect the IPTV physical network interface to the modem, as if your router is the set-top box. And when you see an
IP address is assigned to that interface, your router is successfully connected to the IPTV network.

### Fetch m3u Playlist and xmltv Guide

Modify the config file generated by tellyget-config (which is tellyget.conf), and fill in these fields according to the
following:

- iptv_logical_interface: the IPTV logical network interface
- iptv_interface: the IPTV physical network interface
- channel_url_prefix: the udpxy url prefix (need to fill in it with your router's LAN side IP address)
- channel_filters: list of filters which is used to remove matched channels by name (regular expressions are supported)
- remove_sd_candidate_channels: whether you want to remove standard definition channels if the corresponding high
  definition channels are present
- remove_empty_programme_channels: whether you want to remove the channels which have no programs
- programme_name_cleanup: fix the program names which contain unwanted characters

Upload the config file to your router, and use this command to fetch m3u playlist and xmltv guide:

```shell
tellyget /etc/tellyget/tellyget.conf
```

In order to update m3u playlist and xmltv guide, you should run tellyget regularly. And you know what to do. Just add a
cron job like this to the router:

```shell
50 22 * * * tellyget /etc/tellyget/tellyget.conf &> /var/log/tellyget.log
```

The cron job above will run and write a log after finished at 22:50 every day.

### Configure Other Applications

#### Configure udpxy

udpxy is bound to one upstream interface and one downstream interface. You should set the upstream interface to the IPTV
physical network interface by filling in the "source" (Source IP/Interface) field. And you should set the downstream
interface to your LAN bridge (e.g. br-lan in OpenWrt) by filling in the "bind" (Bind IP/Interface) field.

In order to solve the disconnection issue during playback, set the "mcsub_renew" (multicast subscription renew) field to
a value like 180. This is an empirical value, and you may try other values.

#### Configure xTeVe

Add m3u playlist and xmltv guide fetched by tellyget to xTeVe. The paths of them are defined in the playlist_path and
xmltv_path fields in tellyget.conf.

Set the update time to a value slightly later than the tellyget cron job, like 22:55. But notice that xTeVe has no
knowledge of the time zone, and it treats the time you give as if you are in UTC. So do your math to convert it.

#### Configure Media Players

The m3u playlist and xmltv guide transformed by xTeVe are shown on the top of your xTeVe home page. Add them to the
media players.

### Congratulations

Now you can lock your set-top box in the drawer and enjoy your favorite TV channels with freedom.

## Owner

[William Lu](https://github.com/williamthegrey)

## License

[GNU General Public License v3.0](LICENSE)