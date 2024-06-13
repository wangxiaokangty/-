from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from djangoProject5.settings import ENCRYPTION_KEY
#加密函数
def encrypt_data(data):
    #解析密钥为二进制串
    key = base64.b64decode(ENCRYPTION_KEY.encode('utf-8'))
    #定义加密器
    cipher = AES.new(key, AES.MODE_CBC)
    #加密数据并进行填充
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    #初始化向量与密文拼接
    iv_and_ct = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
    return iv_and_ct

def decrypt_data(iv_and_ct):
    key = base64.b64decode(ENCRYPTION_KEY.encode('utf-8'))
    iv_and_ct_bytes = base64.b64decode(iv_and_ct.encode('utf-8'))
    iv = iv_and_ct_bytes[:AES.block_size]
    ct_bytes = iv_and_ct_bytes[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

