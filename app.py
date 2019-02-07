from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np 
import pandas as pd  

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#Reflect an existing database into a new model
Base = automap_base()
#Reflect the tables
Base.prepare(engine, reflect=True)

#Save the references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#CLIMATE APP
app = Flask(__name__)

@app.route('/')
def welcome():
    return (
    f'Available Routes:<br><br>'
    f'/api/v1.0/precipitation<br>'
    f'Returns the amount of precipitation from the last year available in the data set<br><br>'
    f'/api/v1.0/stations<br>'
    f'Retuns a list of the stations available from the data set<br><br>'
    f'/api/v1.0/tobs<br>'
    f'Returns a list of the temperature observations and the dates the temperatures were taken on<br><br>'
    f'/api/v1.0/yyyy-mm-dd<br>'
    f'Returns the minimum, maximum, and average temperatures from the start date inserted (yyyy-mm-dd) to the end of the data set (2017-08-23)<br><br>'
    f'/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br>'
    f'Returns the minimum, maximum, and average temperatures for the time frame between the inserted start and end dates (yyyy-mm-dd) <br><br>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    sel = [Measurement.date, Measurement.prcp]

    ly_data = session.query(*sel).\
    filter (Measurement.date >= dt.date(2016,8,23)).all()
    
    return jsonify(ly_data)


@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    
    dictionary = []
    for station in stations:
        name = station[0]
        dictionary.append(name)
    
    return jsonify(dictionary)


@app.route('/api/v1.0/tobs')
def tobs():
    sel = [Measurement.date, Measurement.tobs]

    results = session.query(*sel).\
    filter (Measurement.date >= dt.date(2016,8,23)).all()

    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Temperature'] = int(result[1])
        data_list.append(result)
    return jsonify(data_list)

@app.route('/api/v1.0/<start>')
def start(start):
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).all()

    data_list = []
    for result in results:
        row = {}
        row['Minimum Temperature'] = result[0]
        row['Maximum Temperature'] = result[1]
        row['Average Temperature'] = result[2]
        data_list.append(row)
    
    return jsonify(data_list)


@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).\
    filter(Measurement.date<=end).all()

    data_list = []
    for result in results:
        row = {}
        row['Minimum Temperature'] = result[0]
        row['Maximum Temperature'] = result[1]
        row['Average Temperature'] = result[2]
        data_list.append(row)
    
    return jsonify(data_list)

if __name__ == "__main__":
    app.run(debug=True)