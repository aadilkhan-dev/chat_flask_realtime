import jwt
import datetime
from flask import Blueprint,request,render_template,make_response
from sqlalchemy import true
from schemas import UserSchema,FriendRequestSchema
from models import User,FriendRequest,ConectedUser
from passlib.hash import bcrypt
from functools import wraps
from flask_socketio import SocketIO



SECRET_KEY = 'eb38195ecc20b6675a4868e8f79c0d0b'


api = Blueprint('api',__name__,template_folder='/templates')
socketio = SocketIO()

def login_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            try :
                data=jwt.decode(token,SECRET_KEY,["HS256"])
                current_user = User.query.get(data['id'])
            except:
                return {'message':'Invalid Token!!'}
        else:
            return {'error':'token is missing !!'}

        return f(current_user,*args,**kwargs)
    return decorator


@api.route('/signup/',methods=['POST','GET'])
def SignupView():
    userschema = UserSchema()
    if request.method == 'POST':
        data =  request.get_json()
        encrypted_password = bcrypt.hash(data['password'])
        user = User(username=data['username'],password=encrypted_password,full_name =data['full_name'])
        user.create()
        return userschema.dump(user),201
    else:
        return render_template('signup.html')   


@api.route('/login/',methods=['GET','POST'])
def LoginView():
    if request.method == 'POST':
        auth = request.get_json()
        if auth['username'] and auth['password']:
            user=User.query.filter_by(username=auth['username']).first()
            if bcrypt.verify(auth['password'],user.password):
                jwt_token = jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)},SECRET_KEY,"HS256")
                return {'token':jwt_token}
            else:
                make_response('You are not authorized for url',401,{'message':'Please access with credential!!'})   
        else:
            return make_response('You are not authorized for url',401,{'message':'Please access with credential!!'})



@api.route('/sendrequest/<int:id>/',methods=['POST'])
@login_required
def SendRequestView(current_user,id):
    friend_schema = FriendRequestSchema()
    user = User.query.get(id)
    if user and request.method == 'POST':
        friend_user = User.query.get(id)
        friend_request = FriendRequest(user_id=current_user.id,user=current_user,friend=friend_user.username)
        friend_request.create()
        return friend_schema.dump(user),201

@api.route('/sendmessage/<string:id>/',methods=['POST'])
@login_required
def SendMessage(current_user,id):
    socketio.emit({'msg':f'hello message from {current_user}' },room=id)
    return {'success':'successfully sended'},200



@api.route('/messages/',methods=['GET'])
@login_required
def ChatFeedMessage(current_user):
    friends = FriendRequest.query.filter_by(user=current_user,accepted=True).all()
    return render_template('messages.html',friends=friends)


@api.route('/chat/<string:username>/',methods=['GET'])
@login_required
def ChatView(current_user,username):
    get_reciever_user = ConectedUser.query.filter_by(user_name=username).first()
    if get_reciever_user:
        return render_template('chat.html',id=get_reciever_user.id)

    return render_template('chat.html',friend=username)
    

@socketio.on('connect')
@login_required
def connect(current_user):
    get_connected_user  = ConectedUser.query.filter_by(user_name=current_user.username).first()
    if not get_connected_user:
        connected_user = ConectedUser(id=request.sid,user_name=current_user.username)
        connected_user.create() 

@socketio.on('disconnect')
@login_required
def disconnect(current_user):
    get_connected_user  = ConectedUser.query.get(request.sid)
    if get_connected_user:
        get_connected_user.delete()




