from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

#test endpoint for start
@app.route('/')
def index():
    return 'Hello guys!'

#endpoint for show drivers
#additional function for date creation
def toDate(dateString): 
    return datetime.strptime(dateString, "%Y-%m-%d").date()

@app.route('/drivers/driver')
def get_drivers():
    start_dt=request.args.get('created_at__gte', type = toDate)
    end_dt=request.args.get('created_at__lte', type = toDate)
    if start_dt==None and end_dt==None:
        drivers=Driver.query.all()
        driver_result=[]
        for driver in drivers:
            driver_data={'id':driver.id, 'first_name':driver.first_name, 'last_name':driver.last_name,'created_at':driver.created_at,'updated_at':driver.updated_at}
            driver_result.append(driver_data)
        return {"driver":driver_result}
    elif start_dt!=None and end_dt==None:
        drivers=Driver.query.filter(Driver.created_at>=start_dt)
        driver_result=[]
        for driver in drivers:
            driver_data={'id':driver.id, 'first_name':driver.first_name, 'last_name':driver.last_name,'created_at':driver.created_at,'updated_at':driver.updated_at}
            driver_result.append(driver_data)
        return {"driver":driver_result}
    elif start_dt==None and end_dt!=None:
        drivers=Driver.query.filter(Driver.created_at<=end_dt)
        driver_result=[]
        for driver in drivers:
            driver_data={'id':driver.id, 'first_name':driver.first_name, 'last_name':driver.last_name,'created_at':driver.created_at,'updated_at':driver.updated_at}
            driver_result.append(driver_data)
        return {"driver":driver_result}
#show info by specific driver
@app.route('/drivers/driver/<driver_id>')
def get_driver_info(driver_id):
    driver=Driver.query.get_or_404(driver_id)
    return {'id':driver.id, 'first_name':driver.first_name, 'last_name':driver.last_name,'created_at':driver.created_at,'updated_at':driver.updated_at}
#endpoint for create new driver
@app.route("/drivers/driver", methods=["POST"])
def add_driver():
    driver = Driver(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        created_at=datetime.now(),
        updated_at=datetime.now()
        )
    db.session.add(driver)
    db.session.commit()
    return {'first_name':driver.first_name, 'last_name':driver.last_name,'created_at':driver.created_at,'updated_at':driver.updated_at}
#endpoint for delete driver
@app.route("/drivers/driver/<driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    driver=Driver.query.get(driver_id)
    if driver is None:
        return {"driver":"wasn't found"}
    db.session.delete(driver)
    db.session.commit()
    return {"Was delete driver":"success"}
    #endpoint for update driver
@app.route("/drivers/driver", methods=["PUT"])
def update_driver():
    update_data=request.get_json()
    driver=Driver.query.get(update_data['id'])
    if driver is None:
        return {"driver":"wasn't found"}
    driver = Driver(
    first_name=update_data['first_name'],
    last_name=update_data['last_name'],
    created_at=datetime.now(),
    updated_at=datetime.now()
    )
    db.session.add(driver)
    db.session.commit()
    return {"Was updated driver":"success"}
#####Create class Driver##################
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    created_at=db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at=db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, first_name, last_name, created_at,updated_at):
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'{self.id};{self.first_name};{self.last_name};{self.created_at};{self.updated_at}'
    
    db.drop_all()
    db.create_all()
############################################
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer)
    make = db.Column(db.String(120))
    model = db.Column(db.String(120))
    plate_number=db.Column(db.String(120))
    created_at=db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at=db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, driver_id, make, model,plate_number,created_at,updated_at):
        self.driver_id = driver_id
        self.make = make
        self.model = model
        self.plate_number = plate_number
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
       return f'{self.id};{self.driver_id};{self.make};{self.model};{self.plate_number};{self.created_at};{self.updated_at}'

from application import db
from application import Driver
from application import Vehicle

driver = Driver('Hennadii', 'Borysov', datetime(2021, 12, 5, 8, 10, 10, 10),datetime(2021, 12, 11, 4, 10, 10, 10))
driver2 = Driver('Gal', 'Doron', datetime(2021, 11, 5, 8, 10, 10, 10),datetime(2021, 12, 11, 6, 10, 10, 10))
db.session.add(driver)
db.session.add(driver2)

vehicle=Vehicle(1,'make','Ford','AA 1234 OO',datetime(2021, 11, 5, 8, 10, 10, 10),datetime(2021, 12, 11, 6, 10, 10, 10))
vehicle2=Vehicle(1,'make','KIA','AA 2345 CA',datetime(2021, 11, 5, 8, 10, 10, 10),datetime(2021, 12, 11, 6, 10, 10, 10))
db.session.add(vehicle)
db.session.add(vehicle2)

db.session.commit()
db.session.flush()

#start point of application
if(__name__ == "__main__"):
    app.run()

