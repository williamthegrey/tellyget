import sys
import time

import configparser
import netifaces

from tv_guide_updater.auth import Auth
from tv_guide_updater.guide import Guide
from tv_guide_updater.utils import command


def usage():
    print('Usage:')
    print('\t\ttv-guide-updater -h')
    print('\t\ttv-guide-updater <config_file>')


def get_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    bring_up_iptv_logical_interface(config)
    get_iptv_ip(config)
    return config


def bring_up_iptv_logical_interface(config):
    iptv_logical_interface = config['device']['iptv_logical_interface']
    print(f'Bringing up logical interface: {iptv_logical_interface}')
    output, error = command.execute(f'ifup {iptv_logical_interface}')
    print(output, end='')
    time.sleep(10)


def get_iptv_ip(config):
    iptv_interface = config['device']['iptv_interface']
    iptv_ip = netifaces.ifaddresses(iptv_interface)[netifaces.AF_INET][0]['addr']
    print('iptv_ip: ' + iptv_ip)
    config['device']['iptv_ip'] = iptv_ip


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == '-h':
        usage()
        sys.exit()

    config = get_config(sys.argv[1])
    auth = Auth(config)
    auth.authenticate()

    guide = Guide(config, auth.session, auth.base_url, auth.get_channels_data)

    channels = guide.get_channels()
    programmes = guide.get_programmes(channels)

    playlist = guide.get_playlist(channels)
    guide.save_playlist(playlist)
    xmltv = guide.get_xmltv(channels, programmes)
    guide.save_xmltv(xmltv)
