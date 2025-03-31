import mysql.connector
from flask import Blueprint,flash
database = Blueprint('database',__name__)

def connect_to_db():
    try:
        db = mysql.connector.connect(user="#enter your username", password="#enter your password",
                                     host="localhost", port='''enter your port no.''', database='''enter your database name''')
        return db
    except mysql.connector.Error as err:
        raise err

def add_vehicle_details(vehicle_no,model,make,year,fuel_type,mileage,color,owner_name):
    db = connect_to_db()
    cur = db.cursor()
    try:
          cur.execute("insert into vehicle_details(Vehicle_no,model,make,year,fuel_type,mileage,color,owner_name) values (%s,%s,%s,%s,%s,%s,%s,%s)",(vehicle_no,model,make,year,fuel_type,mileage,color,owner_name))
          db.commit()
    except mysql.connector.Error as err:
         flash(f'{err} There was an error adding vehicle apparently. Please retry!', category='error')
         db.rollback()
         
    finally:
         db.commit()
         cur.close()
         db.close()

    return
def add_owner_details(Name,address,phone,email):
    db = connect_to_db()
    cur = db.cursor()
    try:
          cur.execute("insert into owner_details(Name,address,phone,email) values(%s,%s,%s,%s)",(Name,address,phone,email))
          db.commit()
          print("owner details added")
    except mysql.connector.Error as err:
         flash(f'{err} There was an error adding owner apparently. Please retry!', category='error')
         db.rollback()
         
    finally:
         db.commit()
         cur.close()
         db.close()
    return
def add_service_details(service_id, service_date, odometer_reading, service_type,cost,garrage_id,service_notes,vehicle_no):
    db = connect_to_db()
    cur = db.cursor()
    try:
          cur.execute("insert into service_details(service_id,service_date,odometer_reading,service_type,cost,garage_ID,service_notes,vehicle_no) values(%s,%s,%s,%s,%s,%s,%s,%s)",(service_id, service_date, odometer_reading, service_type, cost,garrage_id,service_notes,vehicle_no))
          db.commit()
          print("service details added")
    except mysql.connector.Error as err:
         flash(f'{err}There was an error adding service details apparently. Please retry!', category='error')
         db.rollback()
         
    finally:
        db.commit()
        cur.close()
        db.close()
    return
def add_garrage_details(garrage_id,service_id,garrage_name, address,phone_no,vehicle_no):
    db = connect_to_db()
    cur = db.cursor()
    try:
          cur.execute("insert into garrage_details(garrage_id,service_id,Garrage_Name,address,phone_no,Vehicle_no) values(%s,%s,%s,%s,%s,%s)",(garrage_id,service_id,garrage_name,address,phone_no,vehicle_no))
          db.commit()
          print("garrage details added")
    except mysql.connector.Error as err:
         flash(f'{err} There was an error adding garrage details apparently. Please retry!', category='error')
         db.rollback()
         
    finally:
         db.commit()
         cur.close()
         db.close()
    return
