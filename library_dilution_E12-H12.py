#!/usr/bin/env python

import csv
import re
import argparse
import itertools
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type=str, required=True)
args = parser.parse_args()

SourcePositionSample = []
SourcePositionH2O = []
DestinationPosition = []
SourceWellSample = []
SourceWellH2O = []
Sample = []
H2O = []

DestinationWell=[]
letters=['A','B','C','D','E','F','G','H']
for i in range(1,13):
    coordinates = itertools.product(letters,[i])
    for coordinate in coordinates:
        well = ''.join(map(str, coordinate))
        DestinationWell.append(well)

with open(args.input, 'r') as file:
    lines = csv.reader(file, delimiter=',')
    next(lines)
    for line in lines:
        well = line[0]
        if re.match("^[A-H][1-9]", well):
            if well not in ('E12','F12','G12','H12'):
                Concentration = line[1].replace(">Max", "120.0")        
                Concentration = Concentration.replace("<Min", "0.0")
                Concentration = float(Concentration)
                if Concentration >= 2.0:
                    SourcePositionSample.append("P3")
                    SourcePositionH2O.append("P7")
                    SourceWellH2O.append("1")
                    SourceWellSample.append(line[0])
                    DestinationPosition.append("P6")
                    scaling_factor = ((Concentration)/0.725)
                    Sample.append(5.0)
                    H2O.append((5 * scaling_factor)-5)
Sample = [ '%.1f' % elem for elem in Sample ]
H2O = [ '%.1f' % elem for elem in H2O ]
header = ['SourcePosition','SourcePosition','DestinationPosition','DestinationWell','Volume']
sample_volume = zip(SourcePositionSample,SourceWellSample,DestinationPosition,DestinationWell,Sample)
H2O_volume = zip(SourcePositionH2O,SourceWellH2O,DestinationPosition,DestinationWell,H2O)

out_file = os.path.splitext(args.input)[0]
out_H2O = out_file + "_H2O.csv"
out_sample = out_file + "_sample.csv"

with open(out_H2O, 'wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(H2O_volume)

with open(out_sample, 'wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(sample_volume)
