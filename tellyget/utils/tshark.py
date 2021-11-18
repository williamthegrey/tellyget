import json

from tellyget.utils import command


class TShark:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file

    def filter(self, display_filter, fields=None, read_filter=None):
        cmd = ['tshark', '-2', '-r', self.pcap_file]
        if read_filter is not None:
            cmd += ['-R', read_filter]
        cmd += ['-Y', display_filter]
        if fields is None:
            cmd += ['-T', 'json']
        else:
            cmd += ['-T', 'fields']
            for field in fields:
                cmd += ['-e', field]
        stdout = command.execute(*cmd)
        if fields is None:
            return json.loads(stdout)
        else:
            return self.__parse_fields_output(stdout, fields)

    @staticmethod
    def __parse_fields_output(stdout, fields):
        frames = []
        lines = stdout.splitlines()
        for i, line in enumerate(lines):
            if i % 2 == 1:
                continue
            frame = {}
            columns = line.split('\t')
            for j, column in enumerate(columns):
                frame[fields[j]] = column
            frames.append(frame)
        return frames

    def get_dhcp_requests(self, mac):
        return self.filter('dhcp.option.dhcp == 3', fields=[
            'dhcp.option.hostname',
            'dhcp.option.vendor_class_id'
        ], read_filter=self.__get_mac_filter(mac))

    def get_http_requests(self, uri, mac=None):
        return self.filter(f'http.request.uri contains "{uri}"', read_filter=self.__get_mac_filter(mac))

    def get_http_response(self, request, mac=None):
        response_frame_number = request['_source']['layers']['http']['http.response_in']
        return self.filter(f'frame.number == {response_frame_number}', read_filter=self.__get_mac_filter(mac))[0]

    @staticmethod
    def __get_mac_filter(mac):
        return f'eth.src == {mac} || eth.dst == {mac}' if mac is not None else None

    @staticmethod
    def get_http_data(frame):
        http_layer = frame['_source']['layers']['http']
        return http_layer['http.file_data'] if 'http.file_data' in http_layer else None
