import mysql.connector
import streamlit as st
import pandas as pd

def getData():
    dataBase = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="test1234",
        database="powerplant"
    )

    cursorObject = dataBase.cursor()
    cursorObject.execute("SELECT DATE_TIME, AVG(DAILY_YIELD) AS X FROM powerplant.planttest GROUP BY DATE_TIME  HAVING X != 0 ORDER BY DATE_TIME ASC")
    response = cursorObject.fetchall()

    average = {}
    counter = {}


    for i in range(len(response)):
        datetime = response[i][0]
        time = str(datetime.hour) + ":" + str(datetime.minute)
        if not time in average:
            average[time] = response[i][1]
            counter[time] = 1
        else:
            average[time] += response[i][1]
            counter[time] += 1

    for i in average.keys():
        average[i] = average[i] / counter[i]

    average_per_hour = pd.DataFrame.from_dict(average, orient='index')

    cursorObject = dataBase.cursor()
    cursorObject.execute("SELECT DC_POWER FROM powerplant.planttest")
    response = cursorObject.fetchall()
    dataBase.close()

    all_dc_power = pd.DataFrame.from_dict(response)
    
    return average_per_hour, all_dc_power

def makeCharts(average_per_hour, all_dc_power):
    st.title("Powerplant")
    st.bar_chart(average_per_hour)

    st.title("DC Power Total")
    st.line_chart(all_dc_power)



average_per_hour, all_dc_power = getData()
makeCharts(average_per_hour, all_dc_power)
