"""
Stream guage class for reading data
"""
import numpy as np
import matplotlib.pyplot as plt

class StreamGauge:
    """
    Docstring for StreamGuage
    """
    time = []
    data = []
    units = "ft"

    def __init__(self, fid, station_id, station_name, starttime):
        """Initialize Stream Guage instance
        """
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime

    def read_gauge_file(self):
        """
        Read USGS gauge data and convert date and time to minutes since start

        parameters
        fid (str): path to data

        returns
        timestamp (list): ???
        hgt (np.array): gauge height in ft
        """
        date, time, self.data = np.loadtxt(self.fid, skiprows=28, usecols=[2,3,5], 
                                     dtype=str).T

        self.data = self.astype(float)
        days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
        hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
        mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

        for d, h, m in zip(days, hours, mins):
            timestamp = (d * 24 * 60) + (h * 60) + m
            self.time.append(timestamp)


if __name__ == "__main__":
    sg = StreamGauge("a", "b", "c", "d")
    sg.read_gauge_file()
