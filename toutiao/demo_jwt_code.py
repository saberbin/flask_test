from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from rediscluster import StrictRedisCluster
import random
from datetime import datetime, timedelta
from toutiao.demo_jwt_generate import generate_jwt, verify_jwt

app = Flask(__name__)


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis集群配置
    REDIS_CLUSTER = [
        {'host': '127.0.0.1', 'port': '7000'},
        {'host': '127.0.0.1', 'port': '7001'},
        {'host': '127.0.0.1', 'port': '7002'},
    ]

    JWT_SECRET_KEY = 'hfoiuahsdoifuhoiuhfshfkjh'


app.config.from_object(Config)
app.redis_cluster = StrictRedisCluster(startup_nodes=app.config['REDIS_CLUSTER'])
db = SQLAlchemy(app)


class Mobile(BaseConverter):
    regex = r'1[3-9]\d{9}'


app.url_map.converters['mobile'] = Mobile


class User(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')


@app.route('/')
def url_path():
    data = {}
    for rule in app.url_map.iter_rules():
        data[rule.endpoint] = rule.rule
    return jsonify(data)


@app.route('/user_info')
def user_info():
    return User.query.get(1).name


@app.route('/sms/<mobile:mobile>')
def sms_send(mobile):
    code = "%6d" % (random.randint(10000, 999999))
    app.redis_cluster.set(mobile, code)
    return code


@app.route('/login')
def login():
    mobile = request.args.get('mobile')
    code = request.args.get('code')
    print(code)
    redis_code = app.redis_cluster.get(mobile)
    print(redis_code)
    if code is None or code != redis_code.decode():
        return "Error Code"
    user = User.query.filter_by(mobile=mobile).first()
    if user is None:
        user = User(mobile=mobile, name=mobile+'_name')
        db.session.add(user)
        db.session.commit()
    else:
        pass
    payload = {
        'user_id': user.id
    }
    expiey = datetime.utcnow() + timedelta(hours=2)
    token = generate_jwt(payload, expiey, app.config['JWT_SECRET_KEY'])
    return token


@app.route('index')
def index():
    pass


if __name__ == '__main__':
    app.run(host='192.168.9.149', debug=True)
