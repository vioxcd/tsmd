# Tab Session Deduplicator (and a little bit of analysis)

Initially: trying to answer the question of "what I've been doing on [insert period of time]"; I think the question can easily be answered by looking at my browser history. Browser history are generated from using this [session-manager](https://github.com/sienori/Tab-Session-Manager) Firefox extension.

Update for August 2022: I'm planning to create a script that would **deduplicate opened tabs** and **merge similar sessions into one**. As I'm starting to have problems with searching through my mostly duplicated and similar browsing sessions.

PS: I'm using a conda environment to do the analysis (hint: `rs` for my future self)

PPS: THIS MIGHT END UP BREAKING YOUR (current) SESSION MANAGEMENT (I'm still trying this out). Keep your last exported session intact, maybe.

## How to use

1. Export session data from Tab Session Manager
2. Run `tsmd.py [path to exported session]`
3. Message will appear on the screen if there's any sessions/windows deleted
4. Dumped data can be found on tsmd's `data` dir

## File structures

- `etl.py` are used to combine all stored sessions and dump it into a `csv` that can be analyzed.
- `fun_analysis` folders contain initial exploration and analysis notebook.
- `tsmd.py` are the script used to deduplicate.

## What I do

1. First try (26 Apr)
    - Load all the data (from json to dict) and figure out the keys (schema)
    - Figure out the ordering of dates between the file; one has weird order (swapped earliest and latest record) and another two are duplicated
    - I suspect there are some periods that are missing, so next, I join all the file and turn it into flat file format (csv)
2. Second try (14 May)
    - Turns out my dumped csv are duplicated in most entries because of a bug, so I ended up debugging. it works now!
    - Added an easily-runnable ETL script (just add more session data to the root path); I use nbconvert with tags! (more info [here](https://stackoverflow.com/a/48084050/8996974))
3. Third try (1st and 2nd week of August)
    - Tried to learn data quality toolings (GE, Deequ, Cerberus, Pydantic), and ended-up using Pydantic for this project to parse the JSON schema. The intended use-case for Pydantic was actually just to discover whether there's data type errors within the schema
    - Planning to consume and to later dump the data to its original format using Pydantic
    - Will be adding deduplicator and merger logic (— Me, 14 August 2022)
4. Fourth try (2nd week of September)
    - Doing some analysis with the data. Though not as insightful as I'd imagine.
    - Finishing the deduplicator and changing my mind about merging (maybe later?)
5. Not a try, just an update (2nd week of October) **(latest update)**
    - It's one month in and it's going pretty well so far! Can definitely say that my browsing sessions and search experience have been improving quite dramatically
    - Added friendly summary README on `fun_analysis` folder

## Next idea

- Refactor the code (maybe fix metadata while iterating the data)
- Do the merge part (if ever needed)
- I think there's a bug in Tab Session Manager's import session functionality. Maybe submit an issue?
- The analysis looks kinda bland. Some fresh ideas might be: learn possible tags category via topic modeling or NER and group tabs according to that (something like that would group tabs related to `git` or `stackoverflow` together for example)
