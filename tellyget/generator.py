import configparser
from urllib.parse import parse_qs, unquote

from tellyget.utils.tshark import TShark
from tellyget.tellyget_decrypt import find_encryption_keys


class Generator:
    def __init__(self, pcap_file, stb_mac):
        self.pcap_file = pcap_file
        self.tshark = TShark(pcap_file)
        self.stb_mac = stb_mac
        self.dhcp_request = None
        self.auth_url_request = None
        self.login_url_request = None
        self.config = None

    def parse(self):
        print(f'Parsing {self.pcap_file}')
        self.dhcp_request = self.parse_dhcp_request()
        self.auth_url_request = self.parse_auth_url_request()
        self.login_url_request = self.parse_login_url_request()

    def parse_dhcp_request(self):
        print('Parsing dhcp request')
        return self.tshark.get_dhcp_requests(self.stb_mac)[0]

    def parse_auth_url_request(self):
        print('Parsing auth_url request')
        return self.tshark.get_http_requests('/EDS/jsp/AuthenticationURL', self.stb_mac)[0]

    def parse_login_url_request(self):
        print('Parsing login_url request')
        return self.tshark.get_http_requests('/EPG/jsp/ValidAuthenticationHWCTC.jsp', self.stb_mac)[0]

    def generate_config(self):
        print('Generating config')
        config = configparser.ConfigParser()
        config['auth'] = {}

        auth_full_url = self.auth_url_request['_source']['layers']['http']['http.request.full_uri']
        auth_url = auth_full_url[:auth_full_url.find('?')]

        config['auth']['auth_url'] = auth_url

        login_data = self.tshark.get_http_data(self.login_url_request)
        login_data = parse_qs(login_data, keep_blank_values=True)

        config['auth']['user_id'] = unquote(login_data['UserID'][0])
        config['auth']['net_user_id'] = login_data['NetUserID'][0]
        config['auth']['encryption_key'] = self.__find_encryption_key(login_data['Authenticator'][0])
        config['auth']['user_group_id'] = login_data['userGroupId'][0]
        config['auth']['user_field'] = login_data['UserField'][0]
        config['auth']['vip'] = login_data['VIP'][0]

        config['device'] = {}

        config['device']['iptv_logical_interface'] = 'XXXX'
        config['device']['iptv_interface'] = 'eth0'
        config['device']['stb_id'] = login_data['STBID'][0]
        config['device']['stb_mac'] = self.stb_mac
        config['device']['stb_type'] = login_data['STBType'][0]
        config['device']['stb_version'] = login_data['STBVersion'][0]
        config['device']['software_version'] = login_data['SoftwareVersion'][0]
        config['device']['is_smart_stb'] = login_data['IsSmartStb'][0]
        config['device']['support_hd'] = login_data['SupportHD'][0]
        config['device']['conn_type'] = login_data['conntype'][0]
        config['device']['template_name'] = login_data['templateName'][0]
        config['device']['area_id'] = login_data['areaId'][0]
        config['device']['lang'] = login_data['Lang'][0]
        config['device']['product_package_id'] = login_data['productPackageId'][0]
        config['device']['desktop_id'] = login_data['desktopId'][0]
        config['device']['stb_maker'] = login_data['stbmaker'][0]

        config['guide'] = {}

        config['guide']['channel_url_prefix'] = 'http://000.000.000.000:4022/udp/'
        config['guide']['playlist_path'] = '/etc/tellyget/playlist.m3u'
        config['guide']['xmltv_path'] = '/etc/tellyget/xmltv.xml'
        config['guide']['channel_filters'] = '["^\d+$"]'  # noqa: W605
        config['guide']['remove_sd_candidate_channels'] = 'True'
        config['guide']['remove_empty_programme_channels'] = 'True'
        config['guide']['programme_name_cleanup'] = 'True'

        self.config = config

    @staticmethod
    def __find_encryption_key(authenticator):
        return find_encryption_keys(authenticator)[0]

    def save_config(self, config_file):
        with open(config_file, 'w') as f:
            self.config.write(f)
        print(f'Config saved to {config_file}')

    def generate_hint(self):
        hostname = self.dhcp_request['dhcp.option.hostname']
        vendor_id = self.dhcp_request['dhcp.option.vendor_class_id']

        return f'Use the information below to configure your network interface:\n' \
               f'proto: dhcp\n' \
               f'macaddr: {self.stb_mac}\n' \
               f'hostname: {hostname}\n' \
               f'vendorid: {vendor_id}\n' \
               f'metric: 100'
