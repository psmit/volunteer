from sqlalchemy import (
    Column,
    Integer,
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
    message = Column(Text)
    #slots = relationship("Slot", backref="event")

    def __init__(self,title,date):
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

    def __init__(self,name):
        self.name = name


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    email = Column(Text, unique=True)
    phone = Column(Text)

    slots = relationship("SlotUser", backref="user")

    def __init__(self,name,email=None,phone=None):
        self.name = name
        self.email = email
        self.phone = phone


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

#    def __init__(self,team,event):
#        self.team = team
#        self.event = event
#
