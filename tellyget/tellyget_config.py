import sys

from tellyget.generator import Generator


def usage():
    print('Usage:')
    print('\t\ttellyget-config -h')
    print('\t\ttellyget-config <pcap_file> <stb_mac> <config_file>')


def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    if sys.argv[1] == '-h':
        usage()
        sys.exit()

    pcap_file = sys.argv[1]
    stb_mac = sys.argv[2]
    config_file = sys.argv[3]

    generator = Generator(pcap_file, stb_mac)
    generator.parse()
    generator.generate_config()
    generator.save_config(config_file)
    print(f'\n{generator.generate_hint()}')
