# COP5570 Term Project: Spam Analysis

### Project Breakdown
1. Parsing raw email data.
2. Analysis of email data for incorrect spellings.
3. Correlation of incorrect spelling with other attributes.

## MongoDB

### Document Format
    document = {
        "filename":String,    # Unique Key of filename
        "email":String,       # The `from` field
        "words":List,         # List of unique words
	    "wordCount":Dict,     # Count of words, Str:Int
        "raw":String          # The raw email text as string.
    }

### How to Access Spams
    client = MongoClient()    # Open client connection
    db = client['spam-db']    # choose database
    spams = db.spams          # this is our collection

    spam_id = spams.insert_one(document)  # example insert
    document = spams.find_one()           # get any item
    document = spams.find_one({"email":"andrew@butts.com"})    # specific item

Additional information available at
https://api.mongodb.com/python/current/tutorial.html

## Stage 1

#### Stage 1 Linear Parser Assumptions:
- Parsed file will have plaintext stripped from html
   - Denoted by value text/plain
- Will terminate at end of section
   - Denoted by "--Somenumericalvalue"
- Only considers fully alpha words
   - No contractions or posessive form


#### Stage 1 Steps & Multithreading
1. Creating full path names for all input files.
2. Analyzing a file for a given path name.
3. Filtering out empty sets from the results.

**Small Dataset Testing**

Multithreading all 3 steps has produced a runtime 2.5s and 3.7s for a small
sample dataset.

Multithreading only step 2 has produced a runtime between 1.9s and 2.1s for
the same small sample dataset.

Using no multithreading has produced a runtime between 0.44s and 0.47s for
the sam small sample dataset.

**Full Size Dataset Testing**

Multithreading all 3 steps produced a 3m44.440s runtime.

Using no multithreading produced a 0m9.252s


## Stage 2

#### Stage 2 Steps
1. Cycles through database
2. Cycles through words list in each entry
3. Determines if each list entry is an english language word


