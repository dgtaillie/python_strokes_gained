import numpy as np
import matplotlib.pyplot as plt
from baseline import Baseline
import pandas as pd
from course import Course
from fractions import Fraction



class Round(object):
    def __init__(self, date, course_name,tee, holes):
        self.date = date
        self.course = Course(course_name)
        self.strokes = []
        self.tee = tee
        self.holes = holes

        tee_data = self.read_data_file('tee')
        fairway_data = self.read_data_file('fairway')
        rough_data = self.read_data_file('rough')
        recovery_data = self.read_data_file('recovery')
        green_data = self.read_data_file('green')
        sand_data = self.read_data_file('sand')

        self.baselines = {
            'Tee': tee_data,
            'Fairway': fairway_data,
            'Rough': rough_data,
            'Recovery': recovery_data,
            'Sand': sand_data,
            'Green': green_data
        }
        self.int2phase = {
            1:'Tee',
            2:'Approach > 215',
            3:'Approach 210-175', 
            4:'Approach 175-125',
            5:'Approach 125-80',
            6:'Short Game',
            7:'Putting'
        }

        self.stroketoname = {
            -3:'Double Eagle',
            -2:'Eagle',
            -1:'Birdie',
            0:'Par',
            1:'Bogey',
            2:'Double Bogey',
            3:'Triple Bogey',
            4:'Quad Bogey'
        }

    def read_data_file(self, location):
        return Baseline('data/' + location + '.txt')

    def add_stroke(self, stroke):
        self.strokes.append(stroke)

    def add_end_data(self):
        for idx, stroke in enumerate(self.strokes):
            if stroke.start_loc == 'Penalty':
                stroke.end_loc = 'Penalty'
                stroke.end_dist = 0
            else:
                try:
                    if self.strokes[idx+1].end_loc == 'Tee' :
                        stroke.end_loc = 'In the Hole'
                        stroke.end_dist = 0
                except IndexError:
                    stroke.end_loc = 'In the Hole'
                    stroke.end_dist = 0
                else:
                    stroke.end_loc = self.strokes[idx+1].start_loc
                    stroke.end_dist = self.strokes[idx+1].start_dist
            
            
            
    
    def strokes_to_pandas(self):
        #convert strokes list to pandas df
        df = pd.DataFrame(columns = ['Stroke', 'Club', 'Phase', 'Start Loc', 'Start Dist', 'End Loc', 'End Dist', 
                          'Strokes Gained'], index = range(1, len(self.strokes)+1, 1))
        for idx, stroke in enumerate(self.strokes):
            df.loc[idx+1] = pd.Series({'Stroke':idx+1, 'Club':stroke.club, 'Phase': stroke.phase, 'Start Loc': stroke.start_loc, 'Start Dist': stroke.start_dist,
                  'End Loc': stroke.end_loc, 'End Dist':stroke.end_dist, 'Strokes Gained': stroke.str_gain})
        #return pandas df
        df['Tee'] = self.tee
        df['Course'] = str(self.course.name[0])
        df['Date'] = self.date
        df['Hole'] = 0
        return df
    
    
    def calculate_strokes_gained(self):
        self.add_end_data()
        
        for idx, stroke in enumerate(self.strokes):
            
            
            if stroke.club == 'Penalty':
                stroke.str_gain = 0
                stroke.end_loc = 'Penalty'
                stroke.phase = 'Penalty'
                pass
            else:
                start_data = self.baselines[stroke.start_loc]
                strokes_from_start = start_data.strokes_from(stroke.start_dist)
                
                if stroke.end_loc == 'Penalty':
                    end_data = self.baselines[self.strokes[idx+2].start_loc]
                    strokes_from_end = end_data.strokes_from(self.strokes[idx+2].start_dist)
                    stroke.str_gain = strokes_from_start - strokes_from_end - 2.0
                    
                elif stroke.end_loc == 'Tee' or stroke.end_loc == 'In the Hole':
                    strokes_from_end = 0
                    stroke.end_loc = 'In the Hole'
                    stroke.end_dist = 0
                    stroke.str_gain = round(strokes_from_start - strokes_from_end - 1.0,3)
                else:
                    end_data = self.baselines[stroke.end_loc]
                    strokes_from_end = end_data.strokes_from(stroke.end_dist)

                    stroke.str_gain = round(strokes_from_start - strokes_from_end - 1.0, 3)



                

    
    def plot_strgain_type_xy_bargraph(self):
        data_bar = []
        for label in self.int2phase.values():
            data_bar.append(self.sum_phase(label))
        labels = self.int2phase.values()
        data_bar.append(sum(data_bar))
        labels.append('Total')

        width = 0.8
        colors = []
        for value in data_bar:
            if value > 0:
                colors.append('r')
            else:
                colors.append('k')
        ax = plt.gca()
        ax.bar(range(len(labels)), data_bar, width=width, color=colors)
        ax.set_xticks(np.arange(len(labels)) + width / 2)
        ax.set_xticklabels(labels, rotation=20)
        plt.gca().yaxis.grid(True)
        plt.title('Strokes Gained Shot Type ' + self.date)

        return ax, data_bar

   


    # to be moved to a history type class
    #rewrite for pandas

    def single_round_plot(self):
        #plot scorecard
        fig, axs = plt.subplots(2,1)
        axs[0].axis('tight')
        axs[0].axis('off')
        table_data = self.course.hole_par.T    
        rows = ['Par', 'Score', 'Putts', 'FIR', 'GIR']        
        atable = axs[0].table(cellText = table_data.values, rowLabels = rows, colLabels = table_data.columns, loc = 'center', colWidths = [0.065]*19)
        atable.auto_set_font_size(False)
#        atable.set_fontsize(24)
        #plot strokes gained all strokes
        axs[1].scatter(self.strokes["Start Dist"], self.strokes["Strokes Gained"])
        plt.suptitle(self.date + ' ' + self.course.name[0])
        axs[1].set_xlabel('Distance to Hole')
        axs[1].set_ylabel('Strokes Gained')
        axs[1].grid(True)
        axs[1].axis('tight')
        
        
    def calculate_strokes_to_hole(self):
        #strokes is pandas data frame at this point
        a = self.strokes.index[self.strokes["End Loc"] == "In the Hole"].tolist()
        a.reverse()
        a.append(0)
        hole = 19
        for idx, value in enumerate(a[0:-1]):
            hole = hole - 1
            self.strokes.at[value, 'Hole'] = hole
            self.strokes.at[value, 'Strokes to Hole'] =  1.0
            idx2 = value - 1
            to_hole = 2
            while idx2 > a[idx + 1] and idx2 > 0 :
                self.strokes.at[idx2, 'Strokes to Hole'] = to_hole
                self.strokes.at[idx2, 'Hole'] = hole
                idx2 = idx2 - 1
                to_hole = to_hole + 1

    def save_round(self, filename):
        with open(filename, 'a') as f:
            self.strokes.to_csv(f, header = False)
        print('Data Uploaded')
    
    def build_scorecard(self):
        #get each hole score
        self.course.hole_par["Score"]  = self.strokes["Hole"].value_counts() 
        for value in self.course.hole_par.index:
            #filter down to each hole
            subs = self.strokes.where(self.strokes["Hole"] == value)
            subs = subs.dropna(how = 'any')
            #number of putts
            putts = subs["Phase"].value_counts()["Green"]
            #fairway in regulation
            if self.course.hole_par["Par"].loc[value] != 3:
                if subs.iloc[0]["End Loc"] == 'Fairway':
                    fairway = 'Y'
                else:
                    fairway = 'N'
            else:
                fairway = 'N/A'
            #gir
            if subs["End Loc"].iloc[self.course.hole_par["Par"].loc[value] -3] == 'Green':
                gir = 'Y'
            else:
                gir = 'N'
            
                   
            self.course.hole_par.at[value, "Putts"] = putts
            self.course.hole_par.at[value, "FIR"] = fairway
            self.course.hole_par.at[value, "GIR"] = gir
        #set totals
        self.course.hole_par.at["Total", "Par"] = self.course.hole_par["Par"].sum()
        self.course.hole_par.at["Total", "Score"] = self.course.hole_par["Score"].sum()
        self.course.hole_par.at["Total", "Putts"] = self.course.hole_par["Putts"].sum()
        try:
            made = self.course.hole_par["FIR"].value_counts()["Y"]
        except:
            made = 0
        try:
            missed = self.course.hole_par["FIR"].value_counts()["N"]
        except:
            missed = 0
        self.course.hole_par.at["Total", "FIR"] = Fraction(made, missed + made)
        
        try:
            made = self.course.hole_par["GIR"].value_counts()["Y"]
        except:
            made = 0
        try:
            missed = self.course.hole_par["GIR"].value_counts()["N"]
        except:
            missed = 0
        self.course.hole_par.at["Total", "GIR"] = Fraction(made, missed + made)
                               
        

        
       
        
        
        
        


