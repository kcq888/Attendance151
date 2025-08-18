import os
import argparse

#Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class CollectionCopy():
    sourceSeason = None
    destSeason = None
    RFIDS = "members/rfids"

    def __init__(self, source, dest):
        self.sourceSeason = source
        self.destSeason = dest

        self.fcred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self.fcred)
        self.db = firestore.client()

    def copy(self):
        source_ref = self.db.collection(self.sourceSeason + '/' + self.RFIDS)
        dest_ref = self.db.collection(self.destSeason + '/' + self.RFIDS)
        try:
            docs = source_ref.stream()

            # Use a batch for efficient writes
            batch = self.db.batch()
            write_count = 0

            for doc in docs:
                # Get the document data and ID
                doc_data = doc.to_dict()
                doc_id = doc.id

                new_doc_ref = dest_ref.document(doc_id)
                batch.set(new_doc_ref, doc_data)
                write_count += 1

                if write_count % 100 == 0:
                    print("Committing batch of {write_count} writes...")
                    batch.commit()
                    batch = self.db.batch # start a new batch
                
            # commit any remaining writes in the final batch
            batch.commit()
            print(f"Total documents duplicated: {write_count}")
            print("Collection duplicated successfully!")
        except Exception as e:
            print(f"Error copying collection: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="cellectionCopy", 
        description="Copy collection")
    parser.add_argument('-s', '--source')
    parser.add_argument('-d', '--dest')

    args = parser.parse_args()
    colcopy = CollectionCopy(args.source, args.dest)
    colcopy.copy()
