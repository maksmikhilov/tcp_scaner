from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select, update, delete
from db.connection import engine 

SyncSession = sessionmaker(bind=engine)

def update_row(Table, filter_condition, update_data):
    try:
        with SyncSession() as session:
            with session.begin():
                session.query(Table).filter(filter_condition).update(update_data, synchronize_session='fetch')
                session.commit()
    except Exception as e:
        print(e)
        session.rollback()

def get_row(Table, filter_condition=None):
    try:
        with SyncSession() as session:
            with session.begin():
                table = session.query(Table)
                if filter_condition is not None:
                    table = table.filter(filter_condition)
                    return table.first()
                print([vars(obj) for obj in list(table.all())])
                return [vars(obj) for obj in list(table.all())]
    except Exception as e:
        print(e)
        session.rollback()
        
def delete_row(Table, filter_condition):
    try:
        with SyncSession() as session:
            with session.begin():
                session.query(Table).filter(filter_condition).delete(synchronize_session='fetch')
                session.commit()
    except Exception as e:
        print(e)
        session.rollback()

def set_row(Table, set_data):
    try:
        with SyncSession() as session:
            with session.begin():
                session.add(Table(**set_data))
                session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        