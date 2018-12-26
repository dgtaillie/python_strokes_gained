from round import Round



class Stroke(object):
    def __init__(self, number, club, start_loc, start_dist):
        self.number = number
        self.club = club
        self.start_loc = start_loc
        self.start_dist = start_dist
        self.end_dist = 0
        self.end_loc = 0
        self.str_gain = 0
        


        self.update_phase()
  

        
    def update_phase(self):
        if self.start_loc == 'Tee':
            self.phase = 'Tee'
        if self.start_loc == 'Green':
            self.phase = 'Green'
        if self.start_loc == 'Recovery':
            self.phase = 'Recovery'
        if all([self.start_loc != 'Tee', self.start_loc != 'Green',self.start_loc != 'Recovery']):
            if self.start_dist >=210:
                self.phase = 'APPR210+'
            if self.start_dist < 210 and self.start_dist >= 175:
                self.phase = 'APPR176-210'
            if self.start_dist < 175 and self.start_dist >= 125:
                self.phase = 'APPR125-175'
            if self.start_dist < 125 and self.start_dist >= 80:
                self.phase = 'APPR<125'
            if self.start_dist < 80:
                self.phase = 'Short Game'
    
    def stroke_print(self):
        print('Club: ' + self.club )
        print('Start Loc/Dist: ' + self.start_loc + ' ' + str(self.start_dist))
        print('End Loc/Dist: ' + self.end_loc + ' ' + str(self.end_dist))
        print('Strokes Gained: ' + str(self.str_gain))
        print('----------------------------------------')
