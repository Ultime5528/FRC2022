# FRC2022

## Vision

### Setup
1. `pip install python-dotenv opencv-python supervisely tqdm eel watchdog`
2. Copier son API Token de Supervise.ly : Cliquer sur le menu avec votre nom (en haut à droite) > Account settings > API Token
3. À la racine du projet, créer un fichier nommé ".env" avec le contenu suivant :
```
SERVER_ADDRESS="https://app.supervise.ly"
API_TOKEN="Votre API Token"
```

### Télécharger le dataset
`python -m vision.dataset download`

### Mettre à jour (retélécharger) le dataset
`python -m vision.dataset update`
