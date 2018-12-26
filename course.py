import pandas as pd

class Course(object):
    def __init__(self,data_file):
        filename = 'courses\\' + data_file +'.txt'
        loc_data = pd.read_csv(filename, nrows = 1, header = None)
        self.name = loc_data[0]
        self.city_state = loc_data[1] + ',' + loc_data[2]
        self.hole_par = pd.read_csv(filename, header = 1, index_col = 0)

