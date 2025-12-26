from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
Base = declarative_base()

def main(db_url, df):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    for index, row in df.iterrows():
        person = session.query(Person).filter(Person.register == row['N Registro'])
        if person.count() == 0:
            new_person = Person(register=row['N Registro'], name=row['Nombre'], position=row['Cargo'])
            session.add(new_person)
            session.flush()
        new_guard = Guard(register=row['N Registro'], disponibility=row['Estado'], registerDate=row['Fecha registro'])
        session.add(new_guard)
    session.commit()
    session.close()
class Person(Base):
    __tablename__ = 'Person'
    register = Column(Integer, primary_key=True)
    name = Column(String(255))
    position = Column(String(255))
class Guard(Base):
    __tablename__ = 'Guard'
    id = Column(Integer, primary_key=True, autoincrement=True)
    register = Column(Integer, ForeignKey('Person.register'))
    disponibility = Column(String(255))
    registerDate = Column(DateTime)
