import os

import requests
from dotenv import load_dotenv

from insert_to_db import insert_to_db
from respond_to import respond_To

dotenv_path = './.env'
load_dotenv(dotenv_path)

token = os.getenv("FACEBOOK_PAGE_ACCES_TOKEN")
page_id = os.getenv("PAGE_ID")
access_token_get_comments = token


def handle_comments(reel_id, message):
    graph_get_comments = f'https://graph.facebook.com/v13.0/{reel_id}/comments?limit=25&filter=stream&access_token={access_token_get_comments}'
    liste_response = []
    liste = []
    try:
        response = requests.get(graph_get_comments)
        data = response.json()

        while True:
            comments = data.get('data', [])
            paging = data.get('paging', {})
            nexts = paging.get("next")

            for comment in comments:
                comment_id = comment['id']
                comment_message = comment.get('message')
                comment_author_id = comment.get('from', {}).get('id')
                liste.append(comment_id)
                if comment_author_id != page_id and insert_to_db(f"reel_{reel_id}", comment_id, comment_message,
                                                               page_id, comment_author_id):
                    respond_To(comment_id, access_token_get_comments, message)
                    liste_response.append(f"Répondu à {comment_id}")
                else:
                    liste_response.append(f"Pas moyen de répondre, déjà répondu à {comment_id}")

            if nexts:
                response = requests.get(nexts)
                data = response.json()
            else:
                break
        liste_response.append(f"Nombre total de commentaires récupérés : {len(liste)}")

    except Exception as e:
        liste_response.append(f"Une erreur s'est produite : {str(e)}")

    return liste_response

