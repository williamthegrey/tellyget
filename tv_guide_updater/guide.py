import json

import re
from bs4 import BeautifulSoup


class Guide:
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

    def get_schedules(self, channels):
        schedules = []
        for channel in channels:
            schedule = self.get_schedule(channel['ChannelID'])
            schedules.append(schedule)
        return schedules

    def get_schedule(self, channel_id):
        params = {'channelId': channel_id}
        response = self.session.get(self.base_url + '/EPG/jsp/liveplay_30/en/getTvodData.jsp', params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script', string=re.compile('parent.jsonBackLookStr'))[0].string
        match = re.search(r'parent.jsonBackLookStr\s*=\s*(.+?);', script, re.MULTILINE)
        return json.loads(match.group(1))
