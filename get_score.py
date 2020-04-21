import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--week', required=True)
parser.add_argument('-o', '--output', required=True)
# parser.add_argument('-n', '--names', default='students.txt') # if to sort students by ceiba list
parser.add_argument('-d', '--duration', default='duration.csv')
args = parser.parse_args()

duration = pd.read_csv(args.duration, index_col='title')
# stus = open(args.names, 'r').read().splitlines()

week = pd.read_csv(args.week, index_col=0)
names = [name[:4].strip() for name in week.index]
week.index = names

all_vid = np.sum([duration.loc[vid].values for vid in week.columns])
prog = np.sum([week[col].values * duration.loc[col].values for col in week.columns], axis=0) / all_vid

output = pd.DataFrame({'score': prog.round(2)}, index=names)
output.to_csv(args.output, encoding='utf_8_sig')
