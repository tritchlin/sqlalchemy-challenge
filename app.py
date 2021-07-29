import numpy as np
import pandas as pd
import json

import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct, cast, desc

import datetime as dt
from dateutil.relativedelta import *
from dateutil.parser import *

from flask import Flask, request, render_template, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    recent_date = session.query(measurement.date).order_by((measurement.date.desc())).first()
    end_date = dt.datetime.strptime(recent_date[0],'%Y-%m-%d')
    timestamp_end = dt.datetime.strftime(end_date,'%Y-%m-%d')
    start_date = end_date + relativedelta(months=-12)
    timestamp_start = dt.datetime.strftime(start_date,'%Y-%m-%d')

    prcp_result = engine.execute('SELECT date,prcp FROM measurement WHERE date BETWEEN :start AND :end',(timestamp_start,timestamp_end)).fetchall()

    prcp_df = pd.DataFrame(prcp_result)
    prcp_df2 = prcp_df.rename(columns={0:'Date',1:'Precipitation'})
    prcp_na = prcp_df2.dropna()
    prcp_final = prcp_na.set_index('Date').astype(str)

    prcp_chart = prcp_final.sort_values(by=['Date'])

    session.close()

    return jsonify (prcp_chart.to_dict())

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(distinct(station.station)).all()
    
    session.close()

    station_ids = list(np.ravel(results))

    return jsonify(station_ids)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    recent_date = session.query(measurement.date).order_by((measurement.date.desc())).first()
    end_date = dt.datetime.strptime(recent_date[0],'%Y-%m-%d')
    timestamp_end = dt.datetime.strftime(end_date,'%Y-%m-%d')
    start_date = end_date + relativedelta(months=-12)
    timestamp_start = dt.datetime.strftime(start_date,'%Y-%m-%d')

    count_ = func.count(measurement.station)
    prcp_activity = session.query(measurement.station,count_).\
        group_by(measurement.station).\
        order_by(count_.desc()).all()
    active_station_id = prcp_activity[0]
    most_active = engine.execute('SELECT date,tobs FROM measurement WHERE date BETWEEN :start AND :end AND station == :station_id',(timestamp_start,timestamp_end,active_station_id[0])).fetchall()

    session.close()

    tobs_list = []    
    for date,tobs in most_active:
        tobs_str = str(tobs)
        tobs_list.append(tobs_str)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temp_stats(start):

    begin = dt.datetime.strftime(start,'%Y-%m-%d')

    session = Session(engine)

    results = engine.execute('SELECT date,tobs FROM measurement WHERE date BETWEEN :start AND :end', (begin,end).fetchall()
    
    session.close()

    beg_date = dt.datetime.strftime(start,'%Y-%m-%d')
    for date in 



if __name__ == "__main__":
    app.run(debug=True)
