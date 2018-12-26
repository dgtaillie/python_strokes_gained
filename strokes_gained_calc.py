import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from stroke import Stroke
from round import Round
from course import Course
import pandas as pd

#todo create file with history of all strokes (check repeating)
#todo initialize round object from command line
#todo rewrite with hole objects
#write 


def lookup_basedon_type_str_gain(round1,phase1, strgain1):
    
    phase_search = round1.int2phase[phase1]
    a = round1.strokes_in_phase(phase_search)
    for line in a:
        if abs(line.str_gain -strgain1)<.001:
            return line

def onpick(event):
    ind = event.ind
    for i in ind:
        stroke2print = lookup_basedon_type_str_gain(round1,np.take(x,i),np.take(y,i))
        stroke2print.stroke_print()

if __name__ == '__main__':
    #run only once on a round of data unless comment out save_round()
    data_import = pd.read_csv('rounds\\Uploaded\\121418_LaurelCreek_Palmer.csv', names = ['Club', 'Loc Start', 'Dist Start'])
    round1 = Round('12/14/18', 'LaurelCreek', 'Palmer', '18')

    for idx, row in data_import.iterrows():
        a = Stroke((idx + 1), row["Club"], row["Loc Start"], row["Dist Start"])
        round1.add_stroke(a)
    
    
    round1.calculate_strokes_gained()
    round1.strokes = round1.strokes_to_pandas()
    round1.calculate_strokes_to_hole()
    round1.build_scorecard()
    round1.single_round_plot()
    #round1.save_round('rounds\Taillie_History.csv')
    
#    fig2 = round1.plot_strgain_type_bar()
#
#
#     
#    full_disp = plt.figure()
#    
#    ax1 = full_disp.add_subplot(233)
#
#    ax1,x,y = round1.plot_strokes_gained_inter()
#    full_disp.canvas.mpl_connect('pick_event', onpick)
#
#
#
#
#    # print 'Fairways hit: ' + str(round1.calc_fairways_hit()) + '%'
#
#    ax2 = full_disp.add_subplot(231)
#    ax2 = round1.pie_chart_birdieparbogey()
#    ax3 = full_disp.add_subplot(234)
#    ax3, data_to_store = round1.plot_strgain_type_xy_bargraph()
#    ax4 = full_disp.add_subplot(232)
#    ax4 = round1.plot_green_stats()
#
#    plt.suptitle('ROUND STATS ' + round1.course.name + ' ' + round1.date)
#
#
#
#
#    
#
#
#    plt.show()
