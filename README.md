# COP5570 Term Project: Spam Analysis

### Project Breakdown
1. Parsing raw email data.
2. Analysis of email data for incorrect spellings.
3. Correlation of incorrect spelling with other attributes.

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
