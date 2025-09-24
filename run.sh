#!/bin/bash

# Script de démarrage pour l'application MOE Instagram Analytics
echo "🚀 Démarrage de l'application MOE Instagram Analytics..."

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Vérification des dépendances
if [ ! -f "requirements.txt" ]; then
    echo "❌ Fichier requirements.txt introuvable"
    exit 1
fi

# Installation des dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip3 install -r requirements.txt --quiet

# Vérification du fichier de données
if [ ! -f "insta_data.csv" ]; then
    echo "❌ Fichier insta_data.csv introuvable"
    echo "   Placez le fichier CSV dans le dossier du projet"
    exit 1
fi

# Démarrage de l'application
echo "✅ Démarrage de Streamlit..."
echo "🌐 L'application sera accessible sur http://localhost:8501"
echo "⏹️  Appuyez sur Ctrl+C pour arrêter"

streamlit run app.py
