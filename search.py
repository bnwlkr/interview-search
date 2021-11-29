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
        kwrds = list(csv.reader(kwrd_csv))

    # some processing of vid/keyword data

    vids = [l[0] for l in vids]

    keywords = {c:[] for c in kwrds[0]}
    for r in kwrds[1:]:
        for i in range(len(kwrds[0])):
            if r[i]:
                keywords[kwrds[0][i]].append(r[i])

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

    results = {c:[] for c in keywords.keys()}
    for category in keywords.keys():
        for vid,t in transcripts.items():
            for i,t_unit in enumerate(t):
                for keyword in keywords[category]:
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
                        results[category].append(link)

    # write the results to a file

    with open("results.csv", "w") as result_file:
       writer = csv.writer(result_file)
       writer.writerow(results.keys())
       writer.writerows(list(itertools.zip_longest(*results.values())))

                        

if __name__=='__main__':
    sys.exit(main())
