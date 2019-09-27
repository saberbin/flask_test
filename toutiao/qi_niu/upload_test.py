from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = '51DGWfSzbBws6szT3GVoZ8nMuqVVFAFV2P_StMbr'
secret_key = 'pAo3kBotA7PQLCuIF9Y2wCc7AfRs0MEss2-qdTbb'


def upload_image(file_data):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'toutiao-gz1401'
    # 上传后保存的文件名
    # key = 'my-python-logo.png'
    key = None  # 由七牛云自己管理

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)

    ret, info = put_data(token, key, file_data)
    print(info)
    return ret['key']  # 返回文件的名字


if __name__ == '__main__':
    with open('somecomic.jpg', 'rb') as f:
        print(upload_image(f.read()))

