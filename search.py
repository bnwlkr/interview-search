import sys
import argparse
import csv
import re
import itertools


from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api._errors import TranscriptsDisabled
from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import VideosSearch


def main():
    arg_parser = argparse.ArgumentParser(description="YouTube Interview  Search")

    arg_parser.add_argument('-v', metavar='VIDEO_IDS', required=True,
            help="YouTube Video Id .csv file")

    arg_parser.add_argument('-k', metavar='KEYWORDS', required=True,
            help="Keywords .csv file")


    args = arg_parser.parse_args()

    # open vid/keyword csv files

    with open(args.v) as vid_csv:
        vids = list(csv.reader(vid_csv))

    with open(args.k) as kwrd_csv:
        kwrds = [k for row in list(csv.reader(kwrd_csv))[1:] 
                 for k in row if k != '']

    # some processing of vid/keyword data

    vids = [l[0] for l in vids]

    # get vid transcripts from youtube api

    transcripts = {}
    for vid in vids:
        try:
            t = YouTubeTranscriptApi.get_transcript(vid) 
        except TranscriptsDisabled:
            print(f"Transcripts disabled for {vid}")
            continue
        except NoTranscriptFound:
            print(f"No transcripts found for {vid}")
            continue

        transcripts[vid] = t


    # find keyword matches in transcripts and format output rows

    results = []
    for vid,t in transcripts.items():
        for i,t_unit in enumerate(t):
            for keyword in kwrds:
                regex = fr'\b\w*({keyword})\w*\b'
                res = t_unit['text']
                timestamp = int(t_unit['start']) - 5
                found = False
                for match in re.finditer(regex, t_unit['text'], re.IGNORECASE):
                    found = True
                    res = (res[0:match.start()] + 
                           res[match.start():match.end()].upper() +
                           res[match.end():])
                if found:
                    link = (f"=HYPERLINK(\"http://youtu.be/{vid}?t={timestamp}\","
                            f"\"{res}\")")
                    results.append(link)

    # write the results to a file

    with open("results.csv", "w") as result_file:
       writer = csv.writer(result_file)
       for r in results:
           writer.writerow([r])

                        

if __name__=='__main__':
    sys.exit(main())
