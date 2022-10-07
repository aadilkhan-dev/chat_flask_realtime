from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique = True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class FriendRequest(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("User", uselist=False))
    friend = db.Column(db.String(20))
    accepted = db.Column(db.Boolean,default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self,accepted=False,set_accepted=False):
        if accepted:
            self.accepted = set_accepted
            db.session.commit()
            return self



class ConectedUser(db.Model):
    id = db.Column(db.String(50),primary_key=True)
    user_name = db.Column(db.String(20))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self,id=False,username=False,set_id=None,set_username=None):
        if id :
            self.id = set_id
            db.session.commit()
        if username:
            self.user_name = set_username
            db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self