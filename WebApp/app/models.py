from app import db

playedGames = db.Table('playedGames', db.Model.metadata,
    db.Column('memberId', db.Integer, db.ForeignKey('member.memberId')),
    db.Column('fixtureId', db.Integer, db.ForeignKey('fixture.fixtureId')),
)


class Member(db.Model):
    memberId = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(500))
    password_hash = db.Column(db.String(128))
    position = db.Column(db.String(10))

    fixtures = db.relationship('Fixture', secondary=playedGames, overlaps="members")


    def __repr__(self):
        return self.fname + ' ' + self.lname

class Fixture(db.Model):
    fixtureId = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(50))
    home_away = db.Column(db.String(4))
    date = db.Column(db.Date)
    
    members = db.relationship('Member', secondary=playedGames)

    def __repr__(self):
        return self.team + ' ' + self.home_away
    
class FixtureInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(250))
    meet_loc = db.Column(db.String(250))
    time = db.Column(db.String(4))
    meet_time = db.Column(db.String(4))


    def __repr__(self):
        return self.date + ' ' + self.time

