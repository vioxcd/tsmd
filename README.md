# Tab Session Manager Analysis

Trying to answer the question of "what I've been doing on [insert period of time]"; I think the question can easily be answered by looking at my browser history. Browser history are generated from using this [session-manager](https://github.com/sienori/Tab-Session-Manager) Firefox extension.

PS: I'm using a conda environment to do the analysis (hint: `rs` for my future self)

## What I do.

1. Load all the data (from json to dict) and figure out the keys (schema)
2. Figure out the ordering of dates between the file; one has weird order (swapped earliest and latest record) and another two are duplicated
3. I suspect there are some periods that are missing, so next, I join all the file and turn it into flat file format (csv)
