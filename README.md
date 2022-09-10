# Tab Session Analysis, Deduplicator, and Merger

Trying to answer the question of "what I've been doing on [insert period of time]"; I think the question can easily be answered by looking at my browser history. Browser history are generated from using this [session-manager](https://github.com/sienori/Tab-Session-Manager) Firefox extension.

[Update for August 2022]: I'm planning to create a script that would **deduplicate opened tabs** and **merge similar sessions into one**. As I'm starting to have problems with searching through my mostly duplicated and similar browsing sessions.

PS: I'm using a conda environment to do the analysis (hint: `rs` for my future self)

## What I do.

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
    - Finishing the deduplicator and merge script (should I use pandas?).

## File structures.

- `etl.py` are used to combine all stored sessions and dump it into a `csv` that can be analyzed.
- `fun_analysis` folders contain initial exploration and analysis notebook.
- `tsmdam.py` are the script used to deduplicate and merge sessions.

