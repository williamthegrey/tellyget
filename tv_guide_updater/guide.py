import json
from xml.dom import minidom

import os
import re
from bs4 import BeautifulSoup


class Guide:
    def __init__(self, config, session, base_url, get_channels_data):
        self.config = config
        self.session = session
        self.base_url = base_url
        self.get_channels_data = get_channels_data
        self.channel_filters = self.config['guide']['channel_filters'].encode('unicode_escape')
        self.channel_filters = json.loads(self.channel_filters)

    def get_channels(self):
        response = self.session.post(self.base_url + '/EPG/jsp/getchannellistHWCTC.jsp', data=self.get_channels_data)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', string=re.compile('ChannelID=".+?"'))
        print(f'Found {len(scripts)} channels')
        channels = []
        filtered_channels = 0
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
            if self.match_channel_filters(channel):
                filtered_channels += 1
            else:
                channels.append(channel)
        print(f'Filtered {filtered_channels} channels')
        removed_sd_candidate_channels = self.remove_sd_candidate_channels(channels)
        print(f'Removed {removed_sd_candidate_channels} SD candidate channels')
        print(f'Finally {len(channels)} channels left')
        return channels

    def match_channel_filters(self, channel):
        for channel_filter in self.channel_filters:
            match = re.search(channel_filter, channel['ChannelName'])
            if match:
                return True
        return False

    def remove_sd_candidate_channels(self, channels):
        if not self.config['guide'].getboolean('remove_sd_candidate_channels'):
            return 0
        channels_count = len(channels)
        channels[:] = [channel for channel in channels if not Guide.is_sd_candidate_channel(channel, channels)]
        new_channels_count = len(channels)
        return channels_count - new_channels_count

    @staticmethod
    def is_sd_candidate_channel(channel, channels):
        for c in channels:
            if c['ChannelName'] == channel['ChannelName'] + '高清':
                return True
        return False

    def get_playlist(self, channels):
        content = '#EXTM3U\n'
        for channel in channels:
            content += f"#EXTINF:-1 tvg-id=\"{channel['ChannelID']}\",{channel['ChannelName']}\n"
            channel_url = channel['ChannelURL']
            match = re.search(r'.+?://(.+)', channel_url)
            channel_url_prefix = self.config['guide']['channel_url_prefix']
            channel_url = channel_url_prefix + match.group(1)
            content += f"{channel_url}\n"
        return content

    def save_playlist(self, playlist):
        path = self.config['guide']['playlist_path']
        Guide.save_file(path, playlist)
        print(f'Playlist saved to {path}')

    def get_programmes(self, channels):
        programmes = []
        for channel in channels:
            channel_id = channel['ChannelID']
            schedule = self.get_schedule(channel_id)
            programmes_for_schedule = Guide.get_programmes_for_schedule(schedule)
            programmes.extend(programmes_for_schedule)
            print(f'Found {len(programmes_for_schedule)} programmes for channel {channel_id}')
        return programmes

    def get_schedule(self, channel_id):
        params = {'channelId': channel_id}
        response = self.session.get(self.base_url + '/EPG/jsp/liveplay_30/en/getTvodData.jsp', params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script', string=re.compile('parent.jsonBackLookStr'))[0].string
        match = re.search(r'parent.jsonBackLookStr\s*=\s*(.+?);', script, re.MULTILINE)
        return json.loads(match.group(1))

    @staticmethod
    def get_programmes_for_schedule(schedule):
        programmes = []
        schedules_by_day = schedule[1]
        for schedule_by_day in schedules_by_day:
            programmes.extend(schedule_by_day)
        return programmes

    def get_xmltv(self, channels, programmes):
        doc = minidom.Document()

        tv_node = doc.createElement('tv')
        tv_node.setAttribute('generator-info-name', 'tv-guide-updater')
        Guide.append_channels(doc, tv_node, channels)
        self.append_programmes(doc, tv_node, programmes)
        doc.appendChild(tv_node)

        return doc.toprettyxml(encoding='UTF-8').decode()

    @staticmethod
    def append_channels(doc, tv_node, channels):
        for channel in channels:
            channel_node = doc.createElement('channel')
            channel_node.setAttribute('id', channel['ChannelID'])

            display_name_node = doc.createElement('display-name')
            display_name_node.appendChild(doc.createTextNode(channel['ChannelName']))
            channel_node.appendChild(display_name_node)

            tv_node.appendChild(channel_node)

    def append_programmes(self, doc, tv_node, programmes):
        for programme in programmes:
            programme_node = doc.createElement('programme')
            programme_node.setAttribute('channel', programme['channelId'])
            programme_node.setAttribute('start', f"{programme['beginTimeFormat']} +0800")
            programme_node.setAttribute('stop', f"{programme['endTimeFormat']} +0800")

            title_node = doc.createElement('title')
            title_node.setAttribute('lang', 'zh')
            programme_name = programme['programName']
            if self.config['guide'].getboolean('programme_cleanup'):
                # noinspection SpellCheckingInspection
                programme_name = programme_name.replace('\ufffd', '')
            title_node.appendChild(doc.createTextNode(programme_name))
            programme_node.appendChild(title_node)

            tv_node.appendChild(programme_node)

    def save_xmltv(self, xmltv):
        path = self.config['guide']['xmltv_path']
        Guide.save_file(path, xmltv)
        print(f'XMLTV saved to {path}')

    @staticmethod
    def save_file(file, content):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            f.write(content)
            f.close()
