# interview-search
Search Youtube Vids by Keyword

## Instructions

1. [Install Python 3](https://www.youtube.com/watch?v=UvcQlPZ8ecA)

2. [Install Git](https://www.youtube.com/watch?v=2j7fD92g-gE) (up to 1:32)

3. Launch `Git Bash`

4. Run the following commands in `Git Bash`:
```
cd ~
git clone https://github.com/bnwlkr/interview-search.git
cd interview-search
python3 -m pip install -r requirements.txt
```

5. Export [Keywords](https://docs.google.com/spreadsheets/d/1IrMRHmNc6RAfxVdBYDyUlH7gShlVlJ_27JUqF3n3gw4/edit#gid=1593203162) from Sheets as csv, and rename the file to `keywords.csv`.
6. Export [Video Ids](https://docs.google.com/spreadsheets/d/1IrMRHmNc6RAfxVdBYDyUlH7gShlVlJ_27JUqF3n3gw4/edit#gid=1574739161) from Sheets as csv, and rename the file to `<athlete>.csv` (e.g. `phelps.csv`).
7. Move both of these files into the `interview-search` directory. Should be somewhere like `C:\Users\Andres\interview-search`.

6. Go back to Git Bash and run:
`python3 search.py -k keywords.csv -v <athlete>.csv`
8. Import the resulting `results.csv` into Sheets.

[Video Demo](https://youtu.be/nRNpe17WUn4) for steps 5-8 (on a Mac).

