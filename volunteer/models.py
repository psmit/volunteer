from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )
from sqlalchemy.schema import Table

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Event(Base):
    """ The SQLAlchemy declarative model class for a Event object. """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(Text)
    theme = Column(Text)
    #slots = relationship("Slot", backref="event")

    def __init__(self,title=None,date=None):
        self.title = title
        self.date = date

team_user_table = Table('team_user', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

class Team(Base):
    """ The SQLAlchemy declarative model class for a Team object. """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    leader_id = Column(Integer, ForeignKey('users.id'))
    leader = relationship("User",backref="leadteams")
    members = relationship("User",
        secondary=team_user_table,
        backref="memberteams")
#    slots = relationship("Slot", backref="team")

    def __init__(self,name=None):
        self.name = name


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    phone = Column(String)

    slots = relationship("SlotUser", backref="user")

    def __init__(self,name=None,email=None,phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def nice_phone(self):
        if self.phone is not None:
            return PhoneNumberFormatter().format(self.phone)

class SlotUser(Base):
    __tablename__ = 'slotuser'
    slot_id = Column(Integer, ForeignKey('slots.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    available = Column(Enum('Unknown','Available','NotAvailable'), nullable=False)
    selected = Column(Enum('NotSelected','NotConfirmed','Confirmed'), nullable=False)
    slot = relationship("Slot", backref="slotusers")


class Slot(Base):
    __tablename__ = 'slots'
    id = Column(Integer, primary_key=True)
    min_required = Column(Integer)
#    slotusers = relationship("SlotUser", backref="slot")
    event_id = Column(Integer, ForeignKey('events.id'))
    #slots = relationship("Slot", backref="event")
    event = relationship("Event", backref="slots")
    team_id = Column(Integer,ForeignKey('teams.id'))
    team = relationship("Team", backref="slots")

class Sms(Base):
    __tablename__ = 'sms'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    type = Column(Enum('text','binary'), nullable=False)
    to = Column(String)
    msisdn = Column(String)
    network_code = Column(String)
    message_id = Column(String)
    message_timestamp = Column(DateTime)
    text = Column(Text)
    concat = Column(String)
    concat_ref = Column(String)
    concat_total = Column(Integer)
    concat_part = Column(Integer)


class PhoneNumberFormatter(object):
    def __init__(self,default_prefix=358):
        self.default_prefix = str(default_prefix)

    def format(self,phone_number):
        if phone_number.startswith(self.default_prefix):
            phone_number = '0'+phone_number[len(self.default_prefix):]
        else:
            phone_number = '+'+phone_number

        if len(phone_number) > 9:
            for loc in [-7,-3]:
                phone_number = phone_number[:loc] + " " + phone_number[loc:]

        return phone_number

    def normalize(self,phone_number):
        phone_number = str(phone_number).strip()
        phone_number = phone_number.translate(None,'-() ')
        if len(phone_number) == 0:
            return None

        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        elif phone_number.startswith('00'):
            phone_number = phone_number[2:]
        elif phone_number.startswith('0'):
            phone_number = self.default_prefix + phone_number[1:]
        else:
            raise ValueError("Phone number should start with + or 0")

        if len(phone_number) < 10:
            raise ValueError("Phone number too short")

        return phone_number
