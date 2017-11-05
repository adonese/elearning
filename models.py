


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    confirmed_on = db.Column(db.Boolean, default=False, nullable=False)
    confirm = db.Column(db.DateTime, nullable=False)


    def __init__(self, username, email, _id, id, confirmed_on, confirmed):
        self._id = _id
        self.id = id
        self.username = username
        self.email = email
        self.confirmed_on = confirmed_on
        self.confirmed = confirmed

    def __repr__(self):
        return '<User %r>' % self.username