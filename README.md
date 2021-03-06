# Video Record Parser for NTU COOL

Scripts for parsing raw video records downloaded from NTU COOL (usually `video_analytics.csv`) and calculating averge completion rate weighted by video durations.

## Environment

- python 3.6+
- numpy
- pandas

## Usage

### Parse raw records

```
python get_view_prog.py -i [raw data] -o [path for saving records] -d [path for saving duration]
```

### Calculate completion rate

As raw records are acculmulated since the first video, you can open the record csv generated at the previous step, and delete the useless columns. The columns kept in the generated records will all be used for calculating averge completion rate.

```
python get_score.py -w [records generated at the previous step] -o [path for saving result]
```

