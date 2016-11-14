# COP5570 Term Project: Spam Analysis

### Project Breakdown
 1. Parsing raw email data.
 2. Analysis of email data for incorrect spellings.
 3. Correlation of incorrect spelling with other attributes.

## Stage 1 Linear parser assumptions:
- Parsed file will have plaintext stripped from html
   - Denoted by value text/plain
- Will terminate at end of section
   - Denoted by "--Somenumericalvalue"
- Only considers fully alpha words
   - No contractions or posessive form
