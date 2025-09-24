# Dashboard Instagram MOE

Dashboard d'analyse des posts Instagram pour MOE.

## Installation

1. Cloner le repository
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

- Le fichier CSV des données doit être placé à la racine du projet
- Le chemin du fichier est configurable via la variable `DATA_PATH` dans `app.py`
- Par défaut : `DATA_PATH = "./insta_data.csv"`

## Exécution

```bash
streamlit run app.py
```

## Notes

- Aucun widget d'upload n'est disponible, le fichier CSV doit être présent à la racine
- Le thème sombre est configuré par défaut
- Locale : FR
- Timezone : Europe/Paris 