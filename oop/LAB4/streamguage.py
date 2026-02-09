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
        date, time, hgt = np.loadtxt(self.fid, skiprows=28, usecols=[2,3,5], 
                                     dtype=str).T

        hgt = hgt.astype(float)
        days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
        hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
        mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

        timestamps = []
        for d, h, m in zip(days, hours, mins):
            timestamp = (d * 24 * 60) + (h * 60) + m
            timestamps.append(timestamp)

        # ? Is there another way to do this?
        self.time = timestamps
        self.data = hgt

    def plot(self):
        """Plot USGS gauge data"""
        plt.plot(self.time, self.data)
        plt.xlabel("Time [min]")
        plt.ylabel(f"Gauge Height [{self.units}]")
        plt.title(f"Stream Gauge {self.station_id} {self.station_name} "
                  f"{self.data.max()} {self.units}")
        plt.show()


if __name__ == "__main__":
    fid = "phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt"
    sg = StreamGauge(fid=fid, station_id="15478040", 
                     station_name="PHELAN CREEK", starttime="2024-09-07 00:00")
    assert(len(sg.data) == 0)  # check that we haven't read data yet
    
    sg.read_gauge_file()
    assert(len(sg.time) == len(sg.data))  # check that data and time are equal

    sg.plot()
