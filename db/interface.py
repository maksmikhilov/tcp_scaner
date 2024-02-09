from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import insert, select, update, delete
from db.connection import engine 

Session = sessionmaker(bind=engine)
ScopedSession = scoped_session(Session)

def update_row(Table, filter_condition, update_data):
    try:
        with ScopedSession() as session:
            session.query(Table).filter(filter_condition).update(update_data, synchronize_session='fetch')
            session.flush()
            session.commit()
            
    except Exception as e:
        print('Update: ', e)
        session.rollback()

def get_row(Table, filter_condition=None):
    try:
        with ScopedSession() as session:
            table = session.query(Table)
            if filter_condition is not None:
                table = table.filter(filter_condition)
                return table.first()
            return [vars(obj) for obj in list(table.all())]
    except Exception as e:
        print('Get: ', e)
        session.rollback()
        return None
        

def set_row(Table, set_data):
    try:
        with ScopedSession() as session:
            session.add(Table(**set_data))
            session.flush()
            session.commit()
            
    except Exception as e:
        print('Set: ', e)
        session.rollback()
        
def delete_row(Table, filter_condition):
    try:
        with ScopedSession() as session:
            session.query(Table).filter(filter_condition).delete(synchronize_session='fetch')
            session.commit()
    except Exception as e:
        print('delete: ', e)
        session.rollback()