import os
import pymongo

from dotenv import load_dotenv

dotenv_path = './.env'
load_dotenv(dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")


def check_telegram_user_id(user_id):
    global client
    try:
        client = pymongo.MongoClient(MONGO_URL)
        database = client["users"]
        collection = database["telegram_admin"]
        existing_user = collection.find_one({"user_id": user_id})
        if existing_user:
            return True
        else:

            return False
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
    finally:
        client.close()
