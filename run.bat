@echo off
echo 🚀 Démarrage de l'application MOE Instagram Analytics...

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    pause
    exit /b 1
)

REM Vérification des dépendances
if not exist requirements.txt (
    echo ❌ Fichier requirements.txt introuvable
    pause
    exit /b 1
)

REM Installation des dépendances
echo 📦 Vérification des dépendances...
pip install -r requirements.txt --quiet

REM Vérification du fichier de données
if not exist insta_data.csv (
    echo ❌ Fichier insta_data.csv introuvable
    echo    Placez le fichier CSV dans le dossier du projet
    pause
    exit /b 1
)

REM Démarrage de l'application
echo ✅ Démarrage de Streamlit...
echo 🌐 L'application sera accessible sur http://localhost:8501
echo ⏹️  Appuyez sur Ctrl+C pour arrêter

streamlit run app.py
