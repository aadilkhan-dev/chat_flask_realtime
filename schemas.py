from flask_marshmallow import Marshmallow
from models import User,FriendRequest

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ['username','password']


class FriendRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FriendRequest
        fields = ['user_id','user','friend','accepted']