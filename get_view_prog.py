from collections import deque
from io import StringIO
import argparse
import numpy as np
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Raw records downloaded from NTU COOL')
    parser.add_argument('-o', '--output', required=True, help='File name for output')
    parser.add_argument('-d', '--duration', default='duration.csv', help='File name for video duration')
    args = parser.parse_args()

    with open(args.input) as f:
        ana = deque(f.read().splitlines())

    videos = deque()
    students = deque()
    records = deque()

    print(f"Parsing {args.input}")
    while ana:
        line = ana.popleft()
        if line == 'videos table':
            line = ana.popleft()
            while line != 'students table':
                videos.append(line)
                line = ana.popleft()
            while line != 'viewing records table':
                students.append(line)
                line = ana.popleft()
            while ana:
                records.append(line)
                line = ana.popleft()
            records.append(line)
    students.popleft()
    records.popleft()

    videos = pd.read_csv(StringIO('\n'.join(videos))).sort_values('id')
    students = pd.read_csv(StringIO('\n'.join(students)))
    records = pd.read_csv(StringIO('\n'.join(records)))

    videos['duration'] = [int(s.strip('{}')[11:]) for s in videos['meta']]
    records = records[records['playback_rate']>0.]

    # Count progress
    print("Calculating progress")
    progress = np.zeros((len(students), len(videos)))

    for i, sid in enumerate(students['id']):
        for j, vid in enumerate(videos['id']):
            rec = records[(records['student_id']==sid) & (records['video_id']==vid)]
            done = np.zeros(videos['duration'].iloc[j])
            for k in range(len(rec)):
                done[rec['start'].iloc[k]:(rec['end'].iloc[k])] = 1
            progress[i][j] = done.mean()

    out = pd.DataFrame((progress*100).round(0).astype(int))
    out.index = students['name'].tolist()
    out.columns = videos['title'].tolist()

    out.to_csv(args.output, encoding='utf_8_sig')
    print(f'Saved result at {args.output}')
    
    pd.DataFrame({
        'title': videos['title'],
        'duration': videos['duration']
    }).to_csv(args.duration, index=False)