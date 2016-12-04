from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from collections import Counter

class DB_Driver:

    def __init__(self):

        # Init db connection
        self.mongo = MongoClient()
        self.db = self.mongo['spam-db']
        self.spams = self.db.spams

        # Refresh the index on our spams collection
        self.spams.create_index("filename", unique=True)

        # Tracking collection operations
        self.results = Counter()
        self.errors = Counter()

        # results contains:
        #   inserts
        #   fails
        #   duplicates
        #   updates
        #   matches

    def insert_document(self, document):
        """

        """

        # Attempt insert new document into Mongo
        try:
            spam_id = self.spams.insert_one(document)
            if spam_id is not None:
                self.results['inserts'] += 1

        # Catch if this document's index already exists
        except DuplicateKeyError:
            self.results['duplicates'] += 1

            # Attempt to update the existing document
            try:
                # Run operation on MongoDB
                result = self.spams.update_one(
                    {
                        'filename': document['filename']
                    },
                    {
                        "$set": {
                            "email": document['email'],
                            "wordCount": document['wordCount'],
                            "words": document['words'],
							"year": document['year']
                        }
                    }
                )

                # Check to see what happened
                self.results['matches'] += result.matched_count
                self.results['updates'] += result.modified_count


            # Catch any problems updating
            except Exception as e:
                self.results['fails'] += 1
                self.errors[type(e)] += 1

        # Collect data on oter problems
        except Exception as e:
            self.results['fails'] += 1
            self.errors[type(e)] += 1

db = DB_Driver()
