from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import desc
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
# reflect the database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


# access the tables and mapped classes
Measurement = Base.classes.measurement
Station = Base.classes.station
# create session
session = Session(engine)


################### ______________   Climate App    ______________  ####################

# /
# Start at the homepage.
# All the available routes.

############ _______________ Start date is 2010-01-02 & End date is 2012-01-02 __________________ ################

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (enter date in 2010-01-02 format)<br/>"
        f"/api/v1.0/start_date/end_date (enter dates in 2012-01-02 format)"
    )

####################### ________ /api/v1.0/precipitation _______ ##########################


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the last 12 months of precipitation data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()
    session.close()
    # Convert the query results to a dictionary
    prcp_dict = {}
    for result in results:
        prcp_dict[result[0]] = result[1]

    # Return the JSON representation of the dictionary
    return jsonify(prcp_dict)


######################## _____ /api/v1.0/stations ____  ###########################

@app.route("/api/v1.0/stations")
def stations():
    # Query stations from the Station table
    results = session.query(Station.station).all()
    # Convert list of tuples into a normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

######################### _____  /api/v1.0/tobs _____   ############################


@app.route("/api/v1.0/tobs")
def tobs():
  
    latest_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_data = session.query(Measurement.tobs)\
                .filter(Measurement.station == 'USC00519281')\
                .filter(Measurement.date >= latest_date)\
                .all()
    temps = list(np.ravel(temp_data))
    return jsonify(temps)


###################### _____ /api/v1.0/<start> and /api/v1.0/<start>/<end> ____  #########################


@app.route('/api/v1.0/<start>')
def temp_summary_start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    output = list(np.ravel(result))
    return jsonify(output)


@app.route('/api/v1.0/<start>/<end>')
def temp_summary_start_end(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    output = list(np.ravel(result))
    return jsonify(output)



if __name__ == '__main__':
    app.run(debug=True)


















