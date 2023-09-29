import os

import pymongo
from dotenv import load_dotenv

dotenv_path = './.env'
load_dotenv(dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")


def insert_to_db(where_to_insert, comment_id, comment_content, page_id, user_unique_id):
    global client
    try:
        client = pymongo.MongoClient(MONGO_URL)
        database = client["users"]
        collection = database["comments"]

        comment_id = comment_id
        comment_text = comment_content

        # Recherche l'objet spécifié
        existing_comment = collection.find_one({"_id": where_to_insert})

        if existing_comment:
            if "comments" in existing_comment and any(
                    cmt.get("ID") == comment_id for cmt in existing_comment["comments"]):
                return False
            else:
                if user_unique_id != page_id:
                    collection.update_one(
                        {"_id": where_to_insert},
                        {"$push": {"comments": {"ID": comment_id, "COMMENT": comment_text}}}
                    )
                print("Réussi")
                return True

        else:
            if user_unique_id != where_to_insert:
                new_comment = {
                    "_id": where_to_insert,
                    "comments": [{"ID": comment_id, "COMMENT": comment_text}]
                }
                collection.insert_one(new_comment)
            print("Réussi")
            return True
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
    finally:
        client.close()

