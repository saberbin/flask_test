from flask import Flask, jsonify, g, current_app, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from toutiao.qi_niu.my_jwt import generate_jwt, verify_jwt
from toutiao.qi_niu.upload_test import upload_image
from datetime import datetime, timedelta


app = Flask(__name__)


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'fdasfsafdasfsadfsadf'


app.config.from_object(Config)

api = Api(app)
db = SQLAlchemy(app)


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


class Login(Resource):
    def post(self, mobile):
        user = User.query.filter(User.mobile == mobile).first()
        if user is None:
            user = User(mobile=mobile, name=mobile+'_name')
            db.session.add(user)
            db.session.commit()
        payload = {
            'user_id': user.id
        }
        expiry = datetime.utcnow() + timedelta(hours=2)
        token = generate_jwt(payload, expiry, current_app.config['JWT_SECRET_KEY'])
        return {'token': token}


class Profile(Resource):
    def patch(self):
        token = request.headers.get('Authorization')
        photo = request.files.get('photo')
        payload = verify_jwt(token, current_app.config['JWT_SECRET_KEY'])
        if payload is None:
            return {'msg': 'login first'}, 401
        user = User.query.get(payload.get('user_id'))

        filename = upload_image(photo.read())
        user.profile_photo = filename
        db.session.add(user)
        db.session.commit()
        return {'filename':  'http://pyguq9ykq.bkt.clouddn.com/'+filename}


@app.route('/path')
def url_path():
    data = {}
    for rule in app.url_map.iter_rules():
        data[rule.endpoint] = rule.rule
    return jsonify(data)


api.add_resource(Login, '/login/<mobile>')
api.add_resource(Profile, '/v1_0/user/profile')

if __name__ == '__main__':
    app.run(host='192.168.9.149', debug=True)
