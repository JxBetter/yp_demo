import json
import time
import base64
import hashlib
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from requests_toolbelt.multipart import MultipartEncoder


class Video:
    def __init__(self):
        self._command = ''
        self._value = ''
        self._url = 'https://www.zjstrms.com/rms_openapi/service.do'

    def aes_cbc_encrypt(self, message, key):
        '''
        use AES CBC to encrypt message, using key and init vector
        :param message: the message to encrypt
        :param key: the secret
        :return: bytes init_vector + encrypted_content
        '''
        assert type(message) in (str, bytes)
        assert type(key) in (str, bytes)
        if type(message) == str:
            message = bytes(message, 'utf-8')
        if type(key) == str:
            key = bytes(key, 'utf-8')
        backend = default_backend()
        iv = '1234567890123456'.encode()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message) + padder.finalize()
        enc_content = encryptor.update(padded_data) + encryptor.finalize()
        base_data = base64.b64encode(enc_content)
        return base_data.decode()

    def value_wrapper(self, appid, data):
        res = dict()
        res['appId'] = appid
        res['data'] = self.aes_cbc_encrypt(json.dumps(data), 'a5f17575604e91a9')
        res['timeStamp'] = int(time.time() * 1000)
        res['hashCode'] = hashlib.md5((str(res['timeStamp']) + '123abc').encode()).hexdigest()
        self._value = json.dumps(res)
        return self._value

    def upload_tpl_file(self, file_name):
        """
        上传模版文件
        :param file_name:
        :return:
        """
        cmd = 'uploadFile'

        m_data = MultipartEncoder(
            fields={
                'cmd': cmd,
                'value': self.value_wrapper('74ce89b4a5f17575604e91a906fb0e5e', ""),
                'file': (file_name, open(file_name, 'rb'), 'application/octet-stream')
            },
        )
        headers = {
            'Content-Type': m_data.content_type,
        }
        r = requests.post(self._url, data=m_data, headers=headers)
        print(r.text)
        # print(r.request.body)
        # print(r.request.headers)

    def add_tpl(self, title, tpl_type, info_list):
        """
        添加模版
        :param title:
        :param tpl_type:
        :param info_list:
        :return:
        """
        cmd = 'addTmpl'
        d = {
            'cmd': cmd,
            'value': self.value_wrapper('74ce89b4a5f17575604e91a906fb0e5e', {
                'title': title,
                'tmplType': int(tpl_type),
                'fileInfos': info_list
            })
        }
        r = requests.post(self._url, data=d)
        print(r.text)

    def send_sms(self, title, tpl_id, mobiles, params):
        """
        发送视频短信
        :param title:
        :param tpl_id:
        :param mobiles:
        :param params:
        :return:
        """
        cmd = 'sendMms'
        d = {
            'cmd': cmd,
            'value': self.value_wrapper('74ce89b4a5f17575604e91a906fb0e5e', {
                'title': title,
                'tmplId': tpl_id,
                'mobiles': mobiles,
                'params': params
            })
        }
        r = requests.post(self._url, data=d)
        print(r.text)

    def tpl_check_result(self, tpl_id):
        """
        查询模版审核结果
        :param tpl_id:
        :return:
        """
        cmd = 'qryTmplAuditResult'
        d = {
            'cmd': cmd,
            'value': self.value_wrapper('74ce89b4a5f17575604e91a906fb0e5e', {
                'tmplId': tpl_id
            })
        }
        r = requests.post(self._url, data=d)
        print(r.text)

    def send_result(self, sms_id, mobile):
        """
        查询短信发送状态
        :param sms_id:
        :param mobile:
        :return:
        """
        cmd = 'qrySendResult'
        d = {
            'cmd': cmd,
            'value': self.value_wrapper('74ce89b4a5f17575604e91a906fb0e5e', {
                'reqNo': sms_id,
                'mobile': mobile
            })
        }
        r = requests.post(self._url, data=d)
        print(r.text)


if __name__ == '__main__':
    v = Video()
    # v.upload_tpl_file('wzry.mp4')
    # v.add_tpl('叮～视频短信来啦！', 1,
    #               [{
    #                 'type': 1,
    #                 'content': '【云片网】您好它可以发送文字、图片、视频内容， 展现更丰富，用户体验更优， 带来意想不到的营销转化效果。 云片视频短信，和你一起颠覆传统短信营销！（查看视频免流量）',
    #                 'sort': 1
    #                 },
    #                 {
    #                 'type': 4,
    #                 'content': '1481ef919e0a470fa5f291142299eb5b',
    #                 'sort': 2
    #                 }
    #               ])
    # v.send_sms('jx', 1000245, '15705834033', None)
    v.tpl_check_result(1000287)
