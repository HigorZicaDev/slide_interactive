# TUTORIEL PYTHON WEBSOCKET

L'objectif principal de ce tutoriel est d'explorer le fonctionnement des WebSockets en utilisant le langage de programmation Python et de créer un exemple d'utilisation réelle pour le marché.

**IDÉE : PRÉSENTATIONS SLIDES AVEC INTERACTIONS DES PARTICIPANTS EN UTILISANT PYTHON (FASTAPI) WEBSOCKETS.**

Commençons le projet Python :

- Créer un dossier pour notre projet `slide_interactive`

```bash
mkdir slide_interactive
```

## 1ᵉʳᵈ Étape : Créer un environnement de développement venv et installer les dépendances du projet :

- Les commandes pour créer l'environnement peuvent varier en fonction du système d'exploitation. Dans cet exemple, nous utilisons Windows (si vous êtes sur un autre système, recherchez les commandes équivalentes pour votre OS).

```bash
# Créer l'environnement
python -m venv venv
# Activer l'environnement
venv\Scripts\activate
```

- Installer les dépendances nécessaires : (attention, pour utiliser WebSockets avec un serveur uvicorn, nous devons installer la version standard)

```bash
pip install "uvicorn[standard]"

pip install fastapi
```

## 2ᵉʳᵈ Étape : Créer le fichier qui contiendra la logique de notre application Python à la racine du dossier `slide_interactive`.

- Créer un fichier nommé `main.py`.
- Le code dans `main.py` est responsable d'ouvrir une connexion WebSocket à l'URL et au port : [http://localhost:8000](http://localhost:8000).
- Il stockera les connexions (utilisateurs) et les réponses dans deux variables List et Dict créées dans le code source ci-dessous. Ensuite, nous manipulerons ces réponses pour les afficher sur notre page de tableau de bord en temps réel pendant que les formulaires sont remplis.

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()

# Liste pour stocker les connexions et les réponses
connected_clients: List[WebSocket] = []
responses: List[Dict] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # Si c'est la page du tableau de bord (index.html), envoyer l'historique des réponses
    await websocket.send_json(responses)

    try:
        while True:
            data = await websocket.receive_json()
            responses.append(data)  # Enregistrer la réponse

            # Envoyer la mise à jour à tous les clients connectés
            for client in connected_clients:
                await client.send_json(responses)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
```

## 3ᵉʳᵈ Étape : Créer nos fichiers responsables du frontend (où l'utilisateur remplira le formulaire et où nous afficherons les réponses sur le tableau de bord).

- Premier fichier à créer : `form.html` (responsable de capturer les réponses et de les envoyer à notre backend déjà configuré dans `main.py`).

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remplir le Formulaire</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
    </style>
</head>
<body>
    <h2>Remplissez le Formulaire</h2>
    <form id="form">
        <input type="text" id="name" placeholder="Nom" required>
        <input type="email" id="email" placeholder="E-mail" required>

        <h3>Quel langage de programmation utilisez-vous ?</h3>
        <label><input type="checkbox" name="language" value="Python"> Python</label>
        <label><input type="checkbox" name="language" value="Nodejs"> Node.js</label>
        <label><input type="checkbox" name="language" value="C#"> C#</label>
        <label><input type="checkbox" name="language" value="Java"> Java</label>
        <label><input type="checkbox" name="language" value="PHP"> PHP</label>
        <label><input type="checkbox" name="language" value="Golang"> Golang</label>

        <h3>Quel est votre niveau d'expérience ?</h3>
        <label><input type="radio" name="experience" value="Débutant"> Débutant</label>
        <label><input type="radio" name="experience" value="Intermédiaire"> Intermédiaire</label>
        <label><input type="radio" name="experience" value="Avancé"> Avancé</label>

        <h3>Votre objectif en participant ?</h3>
        <textarea id="goal" maxlength="200"></textarea>

        <button type="submit">Envoyer</button>
    </form>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws");

        document.getElementById("form").addEventListener("submit", function(event) {
            event.preventDefault();
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;

            const languages = [...document.querySelectorAll("input[name='language']:checked")].map(el => el.value);
            const experience = document.querySelector("input[name='experience']:checked")?.value || "";
            const goal = document.getElementById("goal").value;

            const data = { name, email, languages, experience, goal };
            socket.send(JSON.stringify(data));

            document.getElementById("form").reset();
            alert("Réponse envoyée avec succès !");
        });
    </script>
</body>
</html>
```

## 4ᵉʳᵈ Étape : Tester notre application et vérifier si nous avons l'interactivité offerte par WebSocket.

- Exécuter la commande suivante pour démarrer le serveur uvicorn et lancer l'application backend :

```bash
uvicorn main:app --reload
```

- Ensuite, démarrer le serveur frontend pour voir et simuler les actions de remplissage du formulaire et afficher les réponses en temps réel sur le tableau de bord. Dans cet exemple, nous utilisons l'extension *Live Server* de VSCode, qui est simple et fonctionnelle.

```bash
Play live server.
```

