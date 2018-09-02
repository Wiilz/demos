# https://www.youtube.com/watch?v=WxGBoY5iNXY
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt   # json web token, pip install pyJWT
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/apis'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # put the public id in the tolek you'll be able to see it if decode the token
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


def token_required(func):  # decoration
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            corrent_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'})
        return func(corrent_user, *args, **kwargs)
    return decorated



@app.route('/user', methods=['get'])
@token_required
def get_all_uers(current_user):
    if not current_user.admin:  # only admin call get all user
        return jsonify({'message': 'Cannot perform that function'})

    users = User.query.all()
    output = []  # create the output list and loop over the users
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:  # only admin call get all user
        return jsonify({'message': 'Cannot perform that function'})
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        password=hashed_password,
        admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})


@app.route('/user/<public_id>', methods=['PUT'])  # promote admin to True
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:  # only admin call get all user
        return jsonify({'message': 'Cannot perform that function'})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No found user'})
    user.admin = True
    db.session.commit()  # 通过提交会话(事务),将对象写入数据库
    return jsonify({'message': 'The user has been promoted'})


@app.route('/user/<putlic_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, putlic_id):
    user = User.query.filter_by(public_id=putlic_id).first()
    if not user:
        return jsonify({'message': 'No found user'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted'})

# token
@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization
    # 是否输入了帐户名和密码
    if not auth or not auth.username or not auth.password:
        return make_response(
            'Could not verify', 401,
            {'WWW-Authencate': 'Basic realm = "Login Required!"'})
    user = User.query.filter_by(name=auth.username).first()
    # 是否存在该用户
    if not user:
        return make_response(
            'Could not verify', 401,
            {'WWW-Authencate': 'Basic realm = "Login Required!"'})
    # 验证用户的密码和request.authorization中的密码
    if check_password_hash(user.password, auth.password):
        payload = {
            'public_id': user.public_id,
            'exp': datetime.now() + timedelta(minutes=10)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf8')})
    return make_response(
                'Could not verify', 401,
                {'WWW-Authencate': 'Basic realm = "Login Required!"'})


@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    output = []
    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)
    return jsonify({'todos': output})


@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    if not todo:
        return jsonify({'message': 'No found todo'})
    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete
    return jsonify({'todo': todo_data})

@app.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()
    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created'})

@app.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def comelete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    if not todo:
        return jsonify({'message': 'No found todo'})
    todo.complete = True
    db.session.commit()
    return jsonify({'message': 'Todo is completed'})


@app.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    if not todo:
        return jsonify({'message': 'No found todo'})
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo is deleted'})

if __name__ == '__main__':
    app.run(debug=True)