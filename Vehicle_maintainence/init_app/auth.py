from flask import Blueprint, render_template,request,flash,redirect
import mysql.connector

from .database import add_owner_details
from .database import add_service_details
from .database import add_vehicle_details
from .database import add_garrage_details


auth= Blueprint('auth',__name__)
def connect_to_db():
    try:
        db = mysql.connector.connect(user="root", password="Dhanush@2003",
                                     host="localhost", port=3306, database="vehicles")
        return db
    except mysql.connector.Error as err:
        raise err

try:
        conn = mysql.connector.connect(user="root", password="Dhanush@2003", host = "localhost",port = 3306,database="vehicles")
except:
    print("couldn't connect to server")
    print("\n \n Possible fix: Check if server is running")
else:
    print("Connected to server")
cur=conn.cursor()


@auth.route('/base')
def base():
    return render_template('base.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password')

        # Form Validation
        if len(email) < 4:
            flash('Email must have greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must have greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must have greater than 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif not password1.isalnum():
            flash('Password must contain only alphanumeric characters.', category='error')
        else:
            # Input Sanitization and Database Operation
            try:
                cur.execute('''INSERT INTO users
                                (emailid, firstname, lastname, password)
                                VALUES (%s, %s, %s, %s)''',
                                (email,firstName, lastName,password1))
                conn.commit()
                flash('Account created successfully!', category='success')
                return redirect('/login')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', category='error')
                conn.rollback()
    return render_template('signup.html')

@auth.route('/home', methods=['GET', 'POST'])
def home():
    cur.execute("select S.service_date,V.vehicle_no,O.name,G.Garrage_name,S.service_type from vehicle_details V,service_details S,owner_details O, garrage_details G where V.owner_name=O.Name and S.vehicle_no = V.vehicle_no and S.service_id = G.service_id")
    data = cur.fetchall()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'vehicles':
            return redirect('/vehicles')
        if action == 'owners':
            return redirect('/owners')
        if action == 'garrage':
            return redirect('/garrage')
        if action == 'service':
            return redirect('/services')
    return render_template('home.html',data=data)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') 
        paswd = request.form.get('password')
        sql = '''
                SELECT password
                FROM users
                WHERE emailid = %s
            '''
        try:
            cur.execute(sql, (email,))
            data = cur.fetchone()
            if data:
                if data[0] == paswd:
                    flash('Login success', category='success')
                    return redirect('/home')
                else:
                    flash('The entered password is incorrect', category='error')
                    
            else:
                flash('The email id doesn\'t exist', category='error')
        except Exception as e:
            flash(str(e), category='error')

    return render_template('login.html')


@auth.route('/owners',methods=['GET', 'POST'])
def owner():
    cur.execute("select * from owner_details")
    data = cur.fetchall()
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        action = request.form.get('action')
        if action =='add_owner':
            add_owner_details(name,address,phone,email)
            flash('owner added successfully!', category='success')
            conn.commit()
            return redirect('/owners')
        id= request.form.get('id')
        if id:
            db1 = connect_to_db()
            cur1 = db1.cursor()
            try:
                cur1.execute("delete from owner_details where Name = %s",(id,))
                flash('Row deleted', category='success')
                db1.commit()
                conn.commit()
            except mysql.connector.Error as err:
                db1.rollback()
                flash(f'{err}error has occured successfully!', category='error')
            finally:
                cur1.execute("select * from owner_details")
                data = cur1.fetchall()
                db1.commit()
                cur1.close()
                db1.close()
                return redirect('/owners')
    cur.execute("select * from owner_details")
    data = cur.fetchall()
    return render_template('owners.html',data = data)
    


@auth.route('/vehicles',methods=['GET', 'POST'])
def vehicle():
    cur.execute("select * from vehicle_details")
    data = cur.fetchall()
    if request.method == 'POST':
        action = request.form.get('action')
        vehicle_no = request.form.get('vehicle_no')
        model = request.form.get('model')
        make = request.form.get('make')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        mileage = request.form.get('mileage')
        color = request.form.get('colour')
        owner_name = request.form.get('Owner_name')
        if action == 'vehicles':
            add_vehicle_details(vehicle_no,model,make,year,fuel_type,mileage,color,owner_name)
            flash('vehicle added successfully!', category='success')
            cur.execute("select * from vehicle_details")
            data = cur.fetchall()
            return redirect('/vehicles')
            
        id= request.form.get('id')
        if id:
            db1 = connect_to_db()
            cur1 = db1.cursor()
            try:
                cur1.execute("delete from vehicle_details where Vehicle_no = %s",(id,))
                flash('Row deleted', category='success')
                db1.commit()
            except mysql.connector.Error as err:
                db1.rollback()
                flash(f'{err}error has occured successfully!', category='error')
            finally:
                cur1.execute("select * from vehicle_details")
                data = cur1.fetchall()
                cur1.close()
                db1.close()
                return redirect('/vehicles')
    cur.execute("select * from vehicle_details")
    data = cur.fetchall()        
    return render_template('vehicles.html',data=data)



@auth.route('/garrage',methods=['GET', 'POST'])
def garrage():
    cur.execute("select * from garrage_details")
    data = cur.fetchall()
    if request.method == 'POST':
        action = request.form.get('action')
        garrage_id = request.form.get('garrage_id')
        service_id = request.form.get('service_id')
        garrage_name = request.form.get('garrage_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        vehicle_no = request.form.get('vehicle_no')
        if action == 'garrages':
            add_garrage_details(garrage_id,service_id,garrage_name,address,phone,vehicle_no)
            flash('garrage added successfully', category='success')
            return redirect('/garrage')
        id= request.form.get('id')
        if id:
            db1 = connect_to_db()
            cur1 = db1.cursor()
            try:
                cur1.execute("delete from garrage_details where garrage_id = %s",(id,))
                flash('Row deleted', category='error')
                db1.commit()
            except mysql.connector.Error as err:
                db1.rollback()
                flash(f'{err}error has occured successfully!', category='error')
            finally:
                cur1.execute("select * from garrage_details")
                data = cur1.fetchall()
                cur1.close()
                db1.close()
                return redirect('/garrage')
    cur.execute("select * from garrage_details")
    data = cur.fetchall()
    return render_template('garrage.html',data=data)


@auth.route('/services',methods=['GET', 'POST'])
def services():
    cur.execute("select * from service_details")
    data = cur.fetchall()
    if request.method == 'POST':
        action = request.form.get('action')
        service_id = request.form.get('service_id')
        service_date = request.form.get('service_date')
        odometer = request.form.get('odometer')
        service_type = request.form.get('service_type')
        cost = request.form.get('cost')
        garrage_id = request.form.get('garage_ID')
        service_notes = request.form.get('service_notes')
        vehicle_no = request.form.get('vehicle_no')
        if action == 'add_services':
            add_service_details(service_id,service_date,odometer,service_type,cost,garrage_id,service_notes,vehicle_no)
            flash('added successfully!', category='success')
            return redirect('/services')
        id= request.form.get('id')
        if id:
            db1 = connect_to_db()
            cur1 = db1.cursor()
            try:
                
                cur1.execute("delete from service_details where service_id=%s",(id,))
                flash('Row deleted', category='success')
                db1.commit()
            except mysql.connector.Error as err:
                db1.rollback()
                flash(f'{err} error has occured successfully!', category='error')
            finally:
                cur1.execute("select * from service_details")
                data = cur1.fetchall()
                cur1.close()
                db1.close()
                return redirect('/services')
    cur.execute("select * from service_details")
    data = cur.fetchall()
    return render_template('services.html',data=data)
    