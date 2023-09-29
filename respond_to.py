import requests
import json


def respond_To(comment_id, access_token, message_to_respond):
    url = f"https://graph.facebook.com/v13.0/{comment_id}/comments"

    access_token_get_comments = ""

    # Token d'accès
    # Commentaire ID

    # Corps du message au format JSON
    message_data = {
        f"message": f"""
        {message_to_respond}
        """
    }

    # Convertir le corps en JSON
    message_json = json.dumps(message_data)

    # Paramètres de la requête
    params = {
        "access_token": access_token,
        "comment_id": comment_id
    }

    # Envoi de la requête POST avec le corps JSON
    response = requests.post(url, params=params, data=message_json, headers={'Content-Type': 'application/json'})

    # Vérification de la réponse
    if response.status_code == 200:
        print("Le commentaire a été posté avec succès.")
    else:
        print("Une erreur s'est produite lors de la publication du commentaire.")
        print("Code d'erreur :", response.status_code)
        print("Réponse de l'API :", response.text)
