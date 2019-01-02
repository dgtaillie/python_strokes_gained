# python_strokes_gained

Python code aimed to perform strokes gained analysis on a round of golf. Strokes gained is the measure of how effectively a particular shot advanced the ball down the fairway. 

For example, for a golfer standing in the fairway 140 yards away from the hole, it takes an average of 2.91 strokes for the ball to be holed (using PGA Tour metrics). If the golfer hits a shot to 10 ft, it would take an average of 1.626 strokes for the ball to be holed.  Subtracting 1.626 from 2.91 and subtracting the stroke we took to get to that location, we can see that we gained .284 strokes with that  shot. This procedure can be performed on all shots, using different standards for shots from the Tee, Fairway, Rough, Sand, and Recovery  type shots. 

Required for the analysis is a .csv file of a round, listing each shot. The format is:
club, location, distance from hole

The software then calculates the strokes gained for each shot throughout the round and adds the round to the set of master data. 
Different visualization is provided in the secondary processing of the master data. 
