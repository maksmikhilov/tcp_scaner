from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from db import models


def update_row(Table, filter_condition, update_data):
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.query(Table).filter(filter_condition).update(update_data, synchronize_session='fetch')
            session.commit()
    except Exception as e:
        print('Update: ', e)

def get_row(Table, filter_condition=None):
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            table = session.query(Table)
            if filter_condition is not None:
                table = table.filter(filter_condition)
                return table.first()
            return [vars(obj) for obj in list(table.all())]
    except Exception as e:
        print('Get: ', e)
        return None
        

def set_row(Table, set_data):
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(Table(**set_data))
            session.commit()
            
    except Exception as e:
        print('Set: ', e)
        
def delete_row(Table, filter_condition):
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.query(Table).filter(filter_condition).delete(synchronize_session='fetch')
            session.commit()
    except Exception as e:
        print('delete: ', e)
        session.rollback()