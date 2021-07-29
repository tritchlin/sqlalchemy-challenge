# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import datetime as dt

from dateutil.relativedelta import *
from dateutil.parser import *
from sqlalchemy.dialects.sqlite import             BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT,             INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP,             VARCHAR

# %% [markdown]
# # Reflect Tables into SQLAlchemy ORM

# %%
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct, cast, desc
import sqlite3

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite",echo=False)

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare (engine, reflect = True)

# View all of the classes that automap found
base.classes.keys()


# %%
# Save references to each table
measurement = base.classes.measurement
station = base.classes.station


# %%
# Create our session (link) from Python to the DB
session = Session(engine)
conn = engine.connect()
measurements_df = pd.read_sql_query('SELECT * from measurement',con=conn)
stations_df = pd.read_sql_query('SELECT * from station',con=conn)


# %%
inspector = inspect(engine)
inspector.get_table_names()


# %%
measurement_columns = inspector.get_columns('measurement')
for column in measurement_columns:
    print(column["name"], column["type"])


# %%
station_columns = inspector.get_columns('station')
for column in station_columns:
    print(column["name"], column["type"])

# %% [markdown]
# # Exploratory Precipitation Analysis

# %%
def precipitation():
    recent_date = session.query(measurement.date).order_by((measurement.date.desc())).first()
    end_date=dt.datetime.strptime(recent_date[0],'%Y-%m-%d')
    timestamp_end = dt.datetime.strftime(end_date,'%Y-%m-%d')
    start_date = end_date + relativedelta(months=-12)
timestamp_start = dt.datetime.strftime(start_date,'%Y-%m-%d')

# Calculate the date one year from the last date in data set.
timestamp_start


# %%
# Perform a query to retrieve the data and precipitation scores
prcp_result = engine.execute('SELECT date,prcp FROM measurement WHERE date BETWEEN :start AND :end',(timestamp_start,timestamp_end)).fetchall()

# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_df = pd.DataFrame(prcp_result)
prcp_df[0]=pd.to_datetime(prcp_df[0])
prcp_final = prcp_df.rename(columns={0:'Date',1:'Precipitation'}).set_index('Date').dropna()

# Sort the dataframe by date
prcp_chart = prcp_final.sort_values(by=['Date'])

# Use Pandas Plotting with Matplotlib to plot the data
plt.plot(prcp_chart.index, prcp_chart["Precipitation"],label="Precipitation")
plt.legend(loc="upper center")
plt.title("Precipitation in Honolulu over 12 months")
plt.xlabel("Date")
plt.ylabel("Inches")
plt.xticks(rotation=90)
plt.show()


# %%
# Perform a query to retrieve the data and precipitation scores
prcp_result = engine.execute('SELECT date,prcp FROM measurement WHERE date BETWEEN :start AND :end',(timestamp_start,timestamp_end)).fetchall()

# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_df = pd.DataFrame(prcp_result)
prcp_df[0]=pd.to_datetime(prcp_df[0])
prcp_final = prcp_df.rename(columns={0:'Date',1:'Precipitation'}).set_index('Date').dropna()

# Sort the dataframe by date
prcp_chart = prcp_final.sort_values(by=['Date'])

# Use Pandas Plotting with Matplotlib to plot the data
plt.plot(prcp_chart.index, prcp_chart["Precipitation"],label="Precipitation")
plt.legend(loc="upper center")
plt.title("Precipitation in Honolulu over 12 months")
plt.xlabel("Date")
plt.ylabel("Inches")
plt.xticks(rotation=90)
plt.show()


# %%
# Use Pandas to calcualte the summary statistics for the precipitation data
prcp_chart.describe()

# %% [markdown]
# # Exploratory Station Analysis

# %%
# Design a query to calculate the total number stations in the dataset
num_stations = session.query(func.count(distinct(station.station))).all()
num_stations


# %%
# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
count_ = func.count(measurement.station)

prcp_activity = session.query(measurement.station,count_).    group_by(measurement.station).    order_by(count_.desc()).all()
prcp_activity


# %%
active_station_id = prcp_activity[0]
active_station_id


# %%
# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
active_stats = session.query(measurement.tobs).    filter_by(station = active_station_id[0]).all()
max_temp = session.query(func.max(measurement.tobs)).    filter_by(station = active_station_id[0]).all()
max_temp


# %%
min_temp = session.query(func.min(measurement.tobs)).    filter_by(station = active_station_id[0]).all()
min_temp


# %%
avg_temp = session.query(func.avg(measurement.tobs)).    filter_by(station = active_station_id[0]).all()
avg_temp


# %%
annual_activestn_tobs = engine.execute('SELECT date,tobs FROM measurement WHERE date BETWEEN :start AND :end AND station == :station_id',(timestamp_start,timestamp_end,active_station_id[0])).fetchall()
# annual_activestn_tobs


# %%
# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
annual_activestn_tobs = engine.execute('SELECT tobs FROM measurement WHERE date BETWEEN :start AND :end AND station == :station_id',(timestamp_start,timestamp_end,active_station_id[0])).fetchall()
tobs_df = pd.DataFrame(annual_activestn_tobs)
tobs_renamed = tobs_df.rename(columns={0:'Temperature'}).dropna()
maxtobs = int(tobs_renamed.max())
mintobs = int(tobs_renamed.min())


# %%
# Use Pandas Plotting with Matplotlib to plot the data
tobs_renamed.plot.hist(bins=12, range=(mintobs,maxtobs))
plt.legend(loc="upper left")
plt.title("Temp Ranges of "+ str(active_station_id[0]) + " over 12 months")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()

# %% [markdown]
# # Close session

# %%
# Close Session
session.close()


