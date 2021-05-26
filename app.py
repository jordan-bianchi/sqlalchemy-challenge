# Import dependencies
from flask.globals import session
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my SQL-Alchemy API!<br/>"
        f" <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]/[end format:yyyy-mm-dd]<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()

    session.close()


    prcp_list = []
    for date,prcp  in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_data = session.query(Station.station).order_by(Station.station).all()

    session.close()

    station_list = list(station_data)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

    station_tobs = session.query(Measurement.tobs,Measurement.date).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    temp_list = list(station_tobs)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    start_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    start_list = list(start_data)
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    start_end_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_end_list = list(start_end_data)
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)