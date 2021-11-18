from tellyget.utils.cipher import Cipher


class Authenticator:
    def __init__(self, key):
        self.cipher = Cipher(key)

    def build(self, token, user_id, stb_id, ip, mac):
        plain_text = '$'.join(['99999', token, user_id, stb_id, ip, mac, '', 'CTC'])
        return self.cipher.encrypt(plain_text)

    def parse(self, authenticator):
        plain_text = self.cipher.decrypt(authenticator)
        items = plain_text.split('$')
        return {
            'token': items[1],
            'user_id': items[2],
            'stb_id': items[3],
            'ip': items[4],
            'mac': items[5],
        }
