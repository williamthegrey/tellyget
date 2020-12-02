import configparser
import netifaces

from tv_guide_updater.auth import Auth
from tv_guide_updater.guide import Guide


def get_config():
    config = configparser.ConfigParser()
    config.read('etc/tv-guide-updater.conf')
    iptv_interface = config['device']['iptv_interface']
    iptv_ip = netifaces.ifaddresses(iptv_interface)[netifaces.AF_INET][0]['addr']
    print('iptv_ip: ' + iptv_ip)
    config['device']['iptv_ip'] = iptv_ip
    return config


def main():
    config = get_config()
    auth = Auth(config)
    auth.authenticate()

    guide = Guide(config, auth.session, auth.base_url, auth.get_channels_data)

    channels = guide.get_channels()
    programmes = guide.get_programmes(channels)

    playlist = guide.get_playlist(channels)
    guide.save_playlist(playlist)
    xmltv = guide.get_xmltv(channels, programmes)
    guide.save_xmltv(xmltv)