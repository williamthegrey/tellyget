import re
from bs4 import BeautifulSoup


class ChannelList:
    def __init__(self, session, base_url, get_channel_list_data):
        self.session = session
        self.base_url = base_url
        self.get_channel_list_data = get_channel_list_data

    def get_channels(self):
        response = self.session.post(self.base_url + '/EPG/jsp/getchannellistHWCTC.jsp',
                                     data=self.get_channel_list_data)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', string=re.compile('ChannelID=".+?"'))
        channels = []
        for script in scripts:
            match = re.search(r'Authentication.CTCSetConfig\(\'Channel\',\'(.+?)\'\)', script.string, re.MULTILINE)
            channel_params = match.group(1)
            channel = {}
            for channel_param in channel_params.split(','):
                pair = channel_param.split('=')
                key = pair[0]
                value = pair[1]
                value = value[1:len(value) - 1]
                channel[key] = value
            channels.append(channel)
        return channels
