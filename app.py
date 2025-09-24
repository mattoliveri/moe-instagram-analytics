import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import locale
from datetime import datetime
import pytz

# Configuration locale FR
try:
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
except:
    # Locale française non disponible sur Streamlit Cloud - utiliser formatage manuel
    pass

# Configuration Streamlit
st.set_page_config(
    page_title="MOE Instagram Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================== SYSTÈME D'AUTHENTIFICATION ========================

# Initialisation de l'état de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Fonction d'authentification
def authenticate_user(username, password):
    """Vérifier les identifiants utilisateur"""
    return username == "admin" and password == "AdminMOE13"

# Écran de connexion
def show_login_screen():
    """Afficher l'écran de connexion avec le thème MOE"""
    
    # CSS pour l'écran de connexion
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #262730 0%, #1E2028 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 75, 75, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            margin-top: 10vh;
        }
        
        .login-title {
            text-align: center;
            color: #FFFFFF;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #FFFFFF 0%, #FF4B4B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .login-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        .login-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .login-input {
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background-color: rgba(255, 255, 255, 0.05);
            color: #FFFFFF;
            font-size: 1rem;
        }
        
        .login-input:focus {
            outline: none;
            border-color: #FF4B4B;
            box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2);
        }
        
        .login-button {
            padding: 12px 16px;
            border-radius: 8px;
            border: none;
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
            color: #FFFFFF;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
        }
        
        .login-error {
            background-color: rgba(255, 75, 75, 0.1);
            border: 1px solid rgba(255, 75, 75, 0.3);
            border-radius: 8px;
            padding: 12px;
            color: #FF6B6B;
            text-align: center;
            margin-top: 1rem;
        }
        
        /* Style global pour la page de connexion */
        .stApp {
            background: linear-gradient(135deg, #0E1117 0%, #1A1B23 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Conteneur de connexion
    st.markdown("""
    <div class="login-container">
        <h1 class="login-title">MOE Analytics</h1>
        <p class="login-subtitle">Marseille Outdoor Experiences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulaire de connexion
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Connexion")
            
            # Champs de saisie
            username = st.text_input(
                "Identifiant",
                placeholder="Entrez votre identifiant",
                key="login_username"
            )
            
            password = st.text_input(
                "Mot de passe",
                type="password",
                placeholder="Entrez votre mot de passe",
                key="login_password"
            )
            
            # Bouton de connexion
            if st.button("Se connecter", key="login_button", use_container_width=True):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Identifiant ou mot de passe incorrect")
            
            # Message de sécurité
            st.markdown("""
            <div style="text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                🔒 Accès sécurisé - Contactez MOE pour obtenir vos identifiants
            </div>
            """, unsafe_allow_html=True)

# Fonction de déconnexion
def logout():
    """Déconnecter l'utilisateur"""
    st.session_state.authenticated = False
    st.rerun()

# Vérification de l'authentification
if not st.session_state.authenticated:
    show_login_screen()
    st.stop()

# ======================== FIN SYSTÈME D'AUTHENTIFICATION ========================

# Configuration CSS complète pour thème sombre cohérent
st.markdown("""
<style>
    /* ================== CONFIGURATION GLOBALE ================== */
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }
    
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
        background-color: #0E1117 !important;
    }

    /* Cache complètement la sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* ================== STYLE DES MÉTRIQUES ================== */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #262730 0%, #1E2028 100%) !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.2) !important;
        border-color: rgba(255, 75, 75, 0.5) !important;
    }

    [data-testid="stMetric"] > div {
        justify-content: center !important;
    }

    [data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    [data-testid="stMetric"] [data-testid="metric-value"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    [data-testid="stMetric"] [data-testid="metric-delta"] {
        color: #FF4B4B !important;
    }

    /* ================== STYLE DE L'EN-TÊTE ================== */
    .header-container {
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(255, 75, 75, 0.3);
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, transparent 50%);
        border-radius: 12px;
    }

    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #FF4B4B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
    }

    .analytics-section {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: right;
    }

    /* ================== STYLE DES SECTIONS ================== */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    h2 {
        border-left: 4px solid #FF4B4B;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0 !important;
        color: #FFFFFF !important;
    }

    h3 {
        color: #FFFFFF !important;
        margin: 1.5rem 0 1rem 0 !important;
    }

    /* FORCER TOUS LES TEXTES EN BLANC - ULTRA AGRESSIF */
    .stMarkdown, .stMarkdown *, .stText, .stText *, 
    p, div, span, label, small, strong, em, i, b,
    .stSelectbox *, .stMultiSelect *, .stDateInput *, 
    .stTextInput *, .stSlider *, .stNumberInput *,
    .stRadio *, .stCheckbox *, .stButton *,
    [data-testid] *, [class*="st"] * {
        color: #FFFFFF !important;
    }

    /* Labels spécifiques avec contraste maximal */
    .stSelectbox label, .stMultiSelect label, .stDateInput label, 
    .stTextInput label, .stSlider label, .stNumberInput label,
    .stRadio label, .stCheckbox label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Texte dans les métriques - BLANC PUR */
    [data-testid="stMetric"] *, 
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] div {
        color: #FFFFFF !important;
    }

    /* Texte dans les inputs - BLANC PUR */
    input, select, textarea, option {
        color: #FFFFFF !important;
        background-color: #262730 !important;
    }

    /* Placeholders visibles */
    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Texte des boutons - BLANC PUR */
    button, .stButton button, [role="button"] {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* ÉLIMINER TOUT TEXTE GRIS FONCÉ */
    [style*="color: rgb(49, 51, 63)"],
    [style*="color: #31333f"],
    [style*="color: rgb(38, 39, 48)"],
    [style*="color: #262730"] {
        color: #FFFFFF !important;
    }

    /* ================== STYLE DES ONGLETS ================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: linear-gradient(135deg, #262730 0%, #1E2028 100%);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        background-color: transparent;
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.9) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(255, 75, 75, 0.3);
    }

    /* ================== STYLE DES CONTRÔLES ================== */
    /* Forcer TOUS les inputs en thème sombre */
    .stSelectbox > div > div, .stSelectbox div[data-baseweb="select"], 
    .stMultiSelect > div > div, .stMultiSelect div[data-baseweb="select"],
    .stDateInput > div > div, .stDateInput input,
    .stTextInput > div > div, .stTextInput input,
    .stNumberInput > div > div, .stNumberInput input,
    .stSlider > div > div,
    input, select, textarea {
        background-color: #262730 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }

    /* Forcer les options des dropdowns */
    [data-baseweb="popover"] {
        background-color: #262730 !important;
    }

    [data-baseweb="menu"] {
        background-color: #262730 !important;
    }

    [data-baseweb="menu"] li {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: #1E2028 !important;
        color: #FFFFFF !important;
    }

    /* Forcer les tags des multiselect */
    [data-baseweb="tag"] {
        background-color: #FF4B4B !important;
        color: #FFFFFF !important;
    }

    /* ================== STYLE DES GRAPHIQUES ================== */
    [data-testid="stPlotlyChart"] {
        background: linear-gradient(135deg, #262730 0%, #1E2028 100%) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    /* ================== STYLE DU TABLEAU ================== */
    .dataframe {
        background-color: #262730 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }

    .dataframe th {
        background-color: #1E2028 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #FF4B4B !important;
        padding: 12px 8px !important;
    }

    .dataframe td {
        background-color: #262730 !important;
        color: #FFFFFF !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 8px !important;
    }

    .dataframe tr:hover td {
        background-color: rgba(255, 75, 75, 0.1) !important;
    }

    /* Style pour le DataFrame Streamlit - AVEC CONTRASTES */
    [data-testid="stDataFrame"] {
        background-color: #1E2028 !important;
        background: #1E2028 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Container du tableau */
    [data-testid="stDataFrame"] div {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Forcer spécifiquement les cellules du tableau */
    [data-testid="stDataFrame"] table {
        background-color: transparent !important;
        background: transparent !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        width: 100% !important;
    }

    /* EN-TÊTES avec contraste fort */
    [data-testid="stDataFrame"] th {
        background-color: #0D1117 !important;
        background: #0D1117 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border-bottom: 2px solid #FF4B4B !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 12px 8px !important;
        text-align: left !important;
    }

    /* CELLULES avec contraste modéré */
    [data-testid="stDataFrame"] td {
        background-color: #262730 !important;
        background: #262730 !important;
        color: #E6E6E6 !important;
        font-size: 0.85rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 10px 8px !important;
        text-align: left !important;
    }

    /* LIGNES alternées pour meilleure lisibilité */
    [data-testid="stDataFrame"] tr:nth-child(even) td {
        background-color: #2A2D3A !important;
        background: #2A2D3A !important;
    }

    [data-testid="stDataFrame"] tr:nth-child(odd) td {
        background-color: #262730 !important;
        background: #262730 !important;
    }

    /* HOVER avec couleur distinctive */
    [data-testid="stDataFrame"] tr:hover td {
        background-color: rgba(255, 75, 75, 0.15) !important;
        background: rgba(255, 75, 75, 0.15) !important;
        color: #FFFFFF !important;
    }

    /* Forcer TOUS les containers du DataFrame */
    [data-testid="stDataFrame"] [data-testid="stTable"],
    [data-testid="stDataFrame"] .element-container,
    [data-testid="stDataFrame"] .stTable,
    [data-testid="stDataFrame"] .dataframe-container {
        background-color: #262730 !important;
        background: #262730 !important;
    }

    /* Règle d'urgence pour TOUT élément dans stDataFrame */
    [data-testid="stDataFrame"] [style*="background"] {
        background-color: #262730 !important;
        background: #262730 !important;
    }

    /* RÈGLES ULTRA-AGRESSIVES POUR LE TABLEAU */
    /* Cibler tous les tableaux possibles */
    table, .stDataFrame table, [data-testid="stDataFrame"] table {
        background-color: #262730 !important;
        background: #262730 !important;
        color: #FFFFFF !important;
    }

    /* Cibler TOUS les éléments de tableau */
    thead, tbody, tr, th, td,
    .stDataFrame thead, .stDataFrame tbody, .stDataFrame tr, .stDataFrame th, .stDataFrame td,
    [data-testid="stDataFrame"] thead, [data-testid="stDataFrame"] tbody, 
    [data-testid="stDataFrame"] tr, [data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
        background-color: #262730 !important;
        background: #262730 !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Force spéciale pour les en-têtes */
    th, .stDataFrame th, [data-testid="stDataFrame"] th {
        background-color: #1E2028 !important;
        background: #1E2028 !important;
        color: #FFFFFF !important;
        border-bottom: 2px solid #FF4B4B !important;
    }

    /* FORCER avec des sélecteurs CSS très spécifiques */
    div[data-testid="stDataFrame"] > div > div > div > table {
        background-color: #262730 !important;
        background: #262730 !important;
    }

    div[data-testid="stDataFrame"] > div > div > div > table > thead {
        background-color: #1E2028 !important;
        background: #1E2028 !important;
    }

    div[data-testid="stDataFrame"] > div > div > div > table > thead > tr {
        background-color: #1E2028 !important;
        background: #1E2028 !important;
    }

    div[data-testid="stDataFrame"] > div > div > div > table > thead > tr > th {
        background-color: #1E2028 !important;
        background: #1E2028 !important;
        color: #FFFFFF !important;
    }

    /* ================== STYLE DES BOUTONS ================== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4) !important;
    }

    /* ================== STYLE DES ALERTES ================== */
    .stAlert {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 8px !important;
        color: #FFC107 !important;
    }

    /* ================== STYLE DES SLIDERS ================== */
    .stSlider > div > div > div {
        background-color: #262730 !important;
    }

    /* ================== FORCER THÈME SOMBRE PARTOUT ================== */
    /* Règles ultra-agressives pour éliminer TOUT fond blanc */
    * {
        scrollbar-color: #FF4B4B #262730 !important;
    }

    /* Forcer tous les conteneurs possibles */
    div, section, main, header, footer, article, aside, nav {
        background-color: transparent !important;
    }

    /* Forcer les éléments Streamlit spécifiques */
    .element-container, .stContainer, .block-container {
        background-color: transparent !important;
    }

    /* Forcer tous les widgets avec fond blanc */
    [class*="st"] div[style*="background-color: white"],
    [class*="st"] div[style*="background-color: #ffffff"],
    [class*="st"] div[style*="background-color: #FFFFFF"],
    [class*="st"] div[style*="background: white"],
    [class*="st"] div[style*="background: #ffffff"],
    [class*="st"] div[style*="background: #FFFFFF"] {
        background-color: #262730 !important;
        background: #262730 !important;
    }

    /* Forcer les popups et modales */
    [role="dialog"], [role="tooltip"], [role="menu"], [role="listbox"] {
        background-color: #262730 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
    }

    /* Forcer les scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        background-color: #1E2028 !important;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #FF4B4B !important;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background-color: #262730 !important;
    }

    /* Forcer les éléments avec background blanc inline */
    [style*="background-color: white"] {
        background-color: #262730 !important;
    }

    [style*="background-color: #ffffff"] {
        background-color: #262730 !important;
    }

    [style*="background-color: #FFFFFF"] {
        background-color: #262730 !important;
    }

    [style*="background: white"] {
        background: #262730 !important;
    }

    [style*="background: #ffffff"] {
        background: #262730 !important;
    }

    [style*="background: #FFFFFF"] {
        background: #262730 !important;
    }

    /* Forcer les listes déroulantes */
    ul[role="listbox"], li[role="option"] {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }

    /* ================== RESPONSIVE ================== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }
        
        .analytics-section {
            font-size: 1.4rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript pour forcer le thème sombre sur tous les éléments dynamiques
st.markdown("""
<script>
// Fonction pour forcer le thème sombre sur tous les éléments
function forceDarkTheme() {
    // Forcer tous les éléments avec background blanc
    const whiteElements = document.querySelectorAll('*');
    whiteElements.forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.backgroundColor === 'rgb(255, 255, 255)' || 
            style.backgroundColor === 'white' ||
            style.backgroundColor === '#ffffff' ||
            style.backgroundColor === '#FFFFFF') {
            el.style.backgroundColor = '#262730';
            el.style.color = '#FFFFFF';
        }
        
        // FORCER TOUS LES TEXTES GRIS FONCÉ EN BLANC
        if (style.color === 'rgb(49, 51, 63)' ||  // #31333f
            style.color === 'rgb(38, 39, 48)' ||  // #262730
            style.color === 'rgb(30, 32, 40)' ||  // #1E2028
            style.color === '#31333f' ||
            style.color === '#262730' ||
            style.color === '#1E2028') {
            el.style.setProperty('color', '#FFFFFF', 'important');
        }
    });
    
    // Forcer les inputs spécifiquement
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.style.setProperty('background-color', '#262730', 'important');
        input.style.setProperty('color', '#FFFFFF', 'important');
        input.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.2)', 'important');
    });
    
    // Forcer TOUS les labels en blanc
    const labels = document.querySelectorAll('label, .stMarkdown p, .stText');
    labels.forEach(label => {
        label.style.setProperty('color', '#FFFFFF', 'important');
    });
    
    // Forcer les boutons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.setProperty('color', '#FFFFFF', 'important');
        button.style.setProperty('font-weight', '600', 'important');
    });
    
    // FORCE MODÉRÉE pour les DataFrames de Streamlit
    const dataframes = document.querySelectorAll('[data-testid="stDataFrame"]');
    dataframes.forEach(df => {
        // Forcer seulement le style de base sans toucher au contenu
        if (df.style.backgroundColor !== '#262730') {
            df.style.backgroundColor = '#262730';
            df.style.color = '#FFFFFF';
        }
    });
}

// Exécuter au chargement et à chaque modification
document.addEventListener('DOMContentLoaded', forceDarkTheme);
new MutationObserver(forceDarkTheme).observe(document.body, {
    childList: true,
    subtree: true
});

// Exécuter avec une fréquence modérée pour éviter les conflits
setInterval(forceDarkTheme, 1000);

// FONCTION SPÉCIALE pour appliquer les contrastes du tableau
function forceTableTheme() {
    // Cibler uniquement les DataFrames de Streamlit
    const dataframes = document.querySelectorAll('[data-testid="stDataFrame"]');
    
    dataframes.forEach(df => {
        // Container principal avec bordure
        df.style.setProperty('background-color', '#1E2028', 'important');
        df.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.1)', 'important');
        df.style.setProperty('border-radius', '8px', 'important');
        
        // Tableaux transparents
        const tables = df.querySelectorAll('table');
        tables.forEach(table => {
            table.style.setProperty('background-color', 'transparent', 'important');
            table.style.setProperty('border-collapse', 'separate', 'important');
            table.style.setProperty('border-spacing', '0', 'important');
        });
        
        // EN-TÊTES avec contraste maximal
        const headers = df.querySelectorAll('th');
        headers.forEach(header => {
            header.style.setProperty('background-color', '#0D1117', 'important');
            header.style.setProperty('color', '#FFFFFF', 'important');
            header.style.setProperty('font-weight', '700', 'important');
            header.style.setProperty('border-bottom', '2px solid #FF4B4B', 'important');
            header.style.setProperty('border-right', '1px solid rgba(255, 255, 255, 0.1)', 'important');
            header.style.setProperty('padding', '12px 8px', 'important');
        });
        
        // CELLULES avec alternance de couleurs
        const cells = df.querySelectorAll('td');
        cells.forEach((cell, index) => {
            const row = cell.parentElement;
            const rowIndex = Array.from(row.parentElement.children).indexOf(row);
            
            // Couleurs alternées
            if (rowIndex % 2 === 0) {
                cell.style.setProperty('background-color', '#262730', 'important');
            } else {
                cell.style.setProperty('background-color', '#2A2D3A', 'important');
            }
            
            cell.style.setProperty('color', '#E6E6E6', 'important');
            cell.style.setProperty('font-size', '0.85rem', 'important');
            cell.style.setProperty('border-bottom', '1px solid rgba(255, 255, 255, 0.08)', 'important');
            cell.style.setProperty('border-right', '1px solid rgba(255, 255, 255, 0.05)', 'important');
            cell.style.setProperty('padding', '10px 8px', 'important');
        });
        
        // LIGNES avec effet hover
        const rows = df.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                const cells = row.querySelectorAll('td');
                cells.forEach(cell => {
                    cell.style.setProperty('background-color', 'rgba(255, 75, 75, 0.15)', 'important');
                    cell.style.setProperty('color', '#FFFFFF', 'important');
                });
            });
            
            row.addEventListener('mouseleave', () => {
                const cells = row.querySelectorAll('td');
                const rowIndex = Array.from(row.parentElement.children).indexOf(row);
                cells.forEach(cell => {
                    if (rowIndex % 2 === 0) {
                        cell.style.setProperty('background-color', '#262730', 'important');
                    } else {
                        cell.style.setProperty('background-color', '#2A2D3A', 'important');
                    }
                    cell.style.setProperty('color', '#E6E6E6', 'important');
                });
            });
        });
    });
}

// Exécuter la fonction spéciale table moins souvent pour éviter les conflits
setInterval(forceTableTheme, 200);
</script>
""", unsafe_allow_html=True)

# En-tête principal avec bouton de déconnexion
col_title, col_logout = st.columns([6, 1])

with col_title:
    st.markdown("""
    <div class="header-container">
        <div class="title-section">
            <h1 class="main-title">MOE - Marseille Outdoor Experiences</h1>
        </div>
        <div class="analytics-section">
            Instagram Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_logout:
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)  # Espacement
    if st.button("🚪 Déconnexion", key="logout_button", help="Se déconnecter du dashboard"):
        logout()

# Chemin du fichier de données
DATA_PATH = "./insta_data.csv"

# Mapping des colonnes FR vers snake_case
COLUMN_MAPPING = {
    'Date': 'date',
    'Heure': 'heure',
    'Periode': 'periode',
    'Lien': 'lien',
    'Titre': 'titre',
    'Type': 'type',
    'Durée (Reels)': 'duree_reels',
    'Nb Image (Carrousel)': 'nb_images_carousel',
    'Contenue': 'contenu',
    'Collaboration': 'collab',
    'Vues': 'vues',
    'Vues Followers': 'vues_followers',
    'Vues Non Followers': 'vues_non_followers',
    'Nb Interaction': 'nb_interactions',
    'Likes': 'likes',
    'Commentaires': 'commentaires',
    'Partage': 'partages',
    'Enregistrement': 'enregistrements',
    'Activté du Profil': 'activite_profil',
    'Visites du profil': 'visites_profil',
    'Followers en plus': 'followers_plus',
    'Appuis sur des liens externes': 'clics_externes',
    'Hashtags': 'hashtags'
}

# Mapping des jours de la semaine en français
JOURS_SEMAINE = {
    0: 'Lun',
    1: 'Mar',
    2: 'Mer',
    3: 'Jeu',
    4: 'Ven',
    5: 'Sam',
    6: 'Dim'
}

# Fonction pour formater les grands nombres
def format_number(x):
    if pd.isna(x):
        return ""
    if isinstance(x, (int, float)):
        if x >= 1_000_000:
            return f"{x/1_000_000:.1f}M"
        elif x >= 1_000:
            return f"{x/1_000:.1f}k"
        else:
            return f"{x:,.0f}".replace(',', ' ')
    return str(x)

# Fonction pour configurer le thème des graphiques Plotly
def configure_plotly_theme(fig, title=None):
    """Configure un graphique Plotly avec le thème sombre MOE"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family="Arial", size=12),
        title_font=dict(color='#FFFFFF', size=18, family="Arial Black"),
        legend=dict(
            bgcolor='rgba(38, 39, 48, 0.8)',
            bordercolor='rgba(255,255,255,0.3)',
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11)
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.15)',
            linecolor='rgba(255,255,255,0.3)',
            tickfont=dict(color='#FFFFFF', size=11),
            title_font=dict(color='#FFFFFF', size=12)
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.15)',
            linecolor='rgba(255,255,255,0.3)',
            tickfont=dict(color='#FFFFFF', size=11),
            title_font=dict(color='#FFFFFF', size=12)
        ),
        # Configuration des couleurs de survol
        hoverlabel=dict(
            bgcolor='rgba(38, 39, 48, 0.9)',
            bordercolor='rgba(255, 75, 75, 0.5)',
            font_color='#FFFFFF'
        )
    )
    if title:
        fig.update_layout(title=title)
    return fig

# Fonction pour déterminer la période de la journée
def get_heure_bin(heure):
    if pd.isna(heure):
        return None
    try:
        if ':' in str(heure):
            h = int(str(heure).split(':')[0])
        else:
            h = int(float(str(heure)))
        
        if 0 <= h <= 5:
            return 'Nuit'
        elif 6 <= h <= 9:
            return 'Matin'
        elif 10 <= h <= 13:
            return 'Midi'
        elif 14 <= h <= 17:
            return 'Après-midi'
        elif 18 <= h <= 21:
            return 'Soir'
        else:
            return 'Tard'
    except:
        return None

# Vérification de l'existence du fichier
if not Path(DATA_PATH).exists():
    st.error(
        "⚠️ Le fichier de données est introuvable.\n\n"
        "Pour utiliser cette application :\n"
        "1. Placez le fichier 'insta_data.csv' à la racine du projet\n"
        "2. Vérifiez que le fichier est au format CSV avec séparateur ';'\n"
        "3. Assurez-vous que le fichier contient les colonnes requises\n\n"
        "Aucun widget d'upload n'est disponible pour des raisons de sécurité."
    )
    st.stop()

# Chargement des données
df = pd.read_csv(DATA_PATH, sep=';')

# Suppression de la ligne d'en-tête si elle apparaît dans les données
df = df[~df['Date'].astype(str).str.contains('Date', na=False)]

# Renommage des colonnes
df = df.rename(columns=COLUMN_MAPPING)

# Conversion des colonnes numériques
numeric_columns = ['vues', 'vues_followers', 'vues_non_followers', 'nb_interactions',
                   'likes', 'commentaires', 'partages', 'enregistrements',
                   'activite_profil', 'visites_profil', 'followers_plus',
                   'clics_externes']  # Retrait de 'hashtags' des colonnes numériques

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.').replace('', np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Traitement spécial pour les hashtags (remplacement des valeurs manquantes par 0)
df['hashtags'] = df['hashtags'].fillna(0)
df['hashtags'] = pd.to_numeric(df['hashtags'], errors='coerce')

# Traitement des dates et heures
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

# Création du timestamp
df['timestamp'] = df['date'].copy()
mask_heure = df['heure'].notna()

for idx in df[mask_heure].index:
    try:
        heure = str(df.loc[idx, 'heure'])
        if ':' in heure:
            h, m = map(int, heure.split(':'))
        else:
            h = int(float(heure))
            m = 0
        if pd.notna(df.loc[idx, 'date']):
            df.loc[idx, 'timestamp'] = df.loc[idx, 'date'].replace(hour=h, minute=m)
    except:
        continue

# Colonnes temporelles dérivées
df['jour_semaine'] = df['date'].dt.dayofweek.map(JOURS_SEMAINE)
df['semaine'] = df['date'].dt.isocalendar().week
df['mois'] = df['date'].dt.month
df['heure_bin'] = df['heure'].apply(get_heure_bin)

# Création des colonnes type spécifiques
df['is_reels'] = df['type'].fillna('').str.strip() == 'Reels'
df['is_photo'] = df['type'].fillna('').str.strip() == 'Photo'
df['is_carousel'] = df['type'].fillna('').str.strip() == 'Carrousel'

# Conversion de la colonne collaboration en booléen
df['collab'] = df['collab'].fillna('Non').str.strip() == 'Oui'

# Recalcul des KPIs manquants
# nb_interactions = likes + commentaires + enregistrements + partages
df['nb_interactions_calc'] = df['likes'].fillna(0) + df['commentaires'].fillna(0) + \
                               df['enregistrements'].fillna(0) + df['partages'].fillna(0)

# taux_engagement = nb_interactions / vues
df['taux_engagement'] = (df['nb_interactions'] / df['vues']).fillna(
    df['nb_interactions_calc'] / df['vues'])

# activite_profil = visites_profil + followers_plus + clics_externes
df['activite_profil_calc'] = df['visites_profil'].fillna(0) + \
                              df['followers_plus'].fillna(0) + \
                              df['clics_externes'].fillna(0)

# taux_attraction = activite_profil / vues
df['taux_attraction'] = (df['activite_profil'] / df['vues']).fillna(
    df['activite_profil_calc'] / df['vues'])

# Autres taux
df['profile_visit_rate'] = df['visites_profil'] / df['vues']
df['follow_rate'] = df['followers_plus'] / df['vues']
df['external_ctr'] = df['clics_externes'] / df['vues']
df['pct_non_followers'] = df['vues_non_followers'] / (df['vues_followers'] + df['vues_non_followers'])

# Contrôles qualité
warnings = []

# Vérification des colonnes manquantes
expected_columns = set(COLUMN_MAPPING.values())
missing_columns = expected_columns - set(df.columns)
if missing_columns:
    warnings.append(f"Colonnes manquantes : {', '.join(missing_columns)}")

# Vérification des valeurs manquantes
na_cols = df[numeric_columns].isna().sum()
na_cols = na_cols[na_cols > 0]
if not na_cols.empty:
    pass  # On ignore cet avertissement car normal d'avoir des valeurs manquantes

# Vérification des incohérences dans les KPIs calculés
mask_diff = (df['nb_interactions'].notna() & 
            (abs(df['nb_interactions'] - df['nb_interactions_calc']) > 0.1))
if mask_diff.any():
    pass  # On ignore cet avertissement car normal d'avoir des différences

# Vérification des outliers simples (> 3 écarts-types)
outliers = {}
for col in ['vues', 'likes', 'commentaires', 'partages', 'enregistrements']:
    if col in df.columns:
        mean = df[col].mean()
        std = df[col].std()
        count = len(df[abs(df[col] - mean) > 3 * std])
        if count > 0:
            outliers[col] = count

# Si des colonnes sont manquantes (cas critique), on affiche l'avertissement
if missing_columns:
    st.warning(warnings[0])

# Création des DataFrames spécifiques
df_reels = df[df['type'] == 'Reels'].copy()
df_photos = df[df['type'] == 'Photo'].copy()
df_carousel = df[df['type'] == 'Carrousel'].copy()

# Sidebar - Filtres globaux
with st.sidebar:
    st.header("Filtres")
    
    # Filtre de dates
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = st.date_input(
        "Plage de dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask_date = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        df = df[mask_date]
    
    # Filtre de période
    periodes = ['Tous'] + sorted(df['periode'].unique().tolist())
    periode_filter = st.selectbox("Période", periodes)
    if periode_filter != 'Tous':
        df = df[df['periode'] == periode_filter]
    
    # Filtre de contenu
    contenus = ['Tous'] + sorted(df['contenu'].unique().tolist())
    contenu_filter = st.selectbox("Contenu", contenus)
    if contenu_filter != 'Tous':
        df = df[df['contenu'] == contenu_filter]
    
    # Filtre de collaboration
    collab_filter = st.selectbox("Collaboration", ['Tous', 'Oui', 'Non'])
    if collab_filter != 'Tous':
        df = df[df['collab'] == (collab_filter == 'Oui')]
    
    # Filtre de hashtags
    hashtags_range = st.slider("Nombre de hashtags", 0, 3, (0, 3))
    df = df[df['hashtags'].between(hashtags_range[0], hashtags_range[1])]
    
    # Filtre d'heure
    st.subheader("Période de la journée")
    heures_bin = ['Tous'] + ['Nuit', 'Matin', 'Midi', 'Après-midi', 'Soir', 'Tard']
    heure_filter = st.selectbox("Moment de la journée", heures_bin)
    if heure_filter != 'Tous':
        df = df[df['heure_bin'] == heure_filter]
    
    # Séparateur
    st.markdown("---")
    
    # Résumé des posts analysés
    total_posts = len(df)
    reels_count = int(df['is_reels'].sum())
    photos_count = int(df['is_photo'].sum())
    carousel_count = int(df['is_carousel'].sum())
    
    st.markdown(f"""
    **Posts analysés : {total_posts}**
    - Reels : {reels_count}
    - Photos : {photos_count}
    - Carrousels : {carousel_count}
    """)

# Affichage du nombre de posts filtrés
st.sidebar.metric("Posts sélectionnés", len(df))



# Informations sur le dataset
st.subheader("Informations sur le dataset")
col1, col2, col3, col4 = st.columns(4)

# Calcul des métriques
total_posts = len(df)  # Nombre total de posts
reels_count = df['is_reels'].sum()
photos_count = df['is_photo'].sum()
carousel_count = df['is_carousel'].sum()

# Vérification que la somme des types correspond au total
if (reels_count + photos_count + carousel_count) != total_posts:
    st.warning(f"⚠️ Incohérence détectée dans le comptage des posts : {reels_count} + {photos_count} + {carousel_count} ≠ {total_posts}")

with col1:
    st.metric(
        "Nombre total de posts",
        int(total_posts)
    )
with col2:
    st.metric(
        "Reels",
        int(reels_count)
    )
with col3:
    st.metric(
        "Photos",
        int(photos_count)
    )
with col4:
    st.metric(
        "Carrousels",
        int(carousel_count)
    )

# KPIs moyens
st.subheader("KPIs moyens")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Taux d'engagement moyen",
        f"{df['taux_engagement'].mean()*100:.1f}%"
    )
with col2:
    st.metric(
        "Taux d'attraction moyen",
        f"{df['taux_attraction'].mean()*100:.1f}%"
    )
with col3:
    st.metric(
        "% Non-followers moyen",
        f"{df['pct_non_followers'].mean()*100:.1f}%"
    )

# Création des onglets
overview, reels, photos, carousel, charts, explorer = st.tabs([
    "Overview", "Reels", "Photos", "Carrousel", "Charts", "Explorer"
])

# Onglet Overview
with overview:
    st.header("Vue d'ensemble")
    
    # KPI Cards
    st.subheader("KPIs Globaux")
    
    # Première ligne de KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        total_vues = df['vues'].sum()
        st.metric("Vues totales", f"{total_vues:,.0f}".replace(',', ' '))
    
    with col2:
        total_interactions = df['nb_interactions'].sum()
        st.metric("Interactions totales", f"{total_interactions:,.0f}".replace(',', ' '))
    
    with col3:
        total_followers = df['followers_plus'].sum()
        st.metric("Nouveaux followers", f"{total_followers:,.0f}".replace(',', ' '))
    
    # Deuxième ligne de KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        median_engagement = df['taux_engagement'].median()
        st.metric("Taux d'engagement médian", f"{median_engagement*100:.1f}%")
    
    with col2:
        median_attraction = df_reels['taux_attraction'].median()
        st.metric("Taux d'attraction médian", f"{median_attraction*100:.1f}%")
    
    with col3:
        median_non_followers = df['pct_non_followers'].median()
        st.metric("% Non-followers médian", f"{median_non_followers*100:.1f}%")
    
    # Séries temporelles
    st.subheader("Évolution temporelle")
    
    # Sélection des métriques à afficher
    metrics = {
        'Vues': 'vues',
        'Likes': 'likes',
        'Commentaires': 'commentaires',
        'Partages': 'partages',
        'Enregistrements': 'enregistrements'
    }
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_metrics = st.multiselect(
            "Métriques à afficher",
            options=list(metrics.keys()),
            default=['Vues', 'Likes']
        )
    
    with col2:
        # Sélection de la résolution temporelle
        resolution = st.selectbox(
            "Résolution",
            options=['Jour', 'Semaine', 'Mois'],
            index=0
        )
        
        # Sélection de l'agrégation
        aggregation = st.selectbox(
            "Agrégation",
            options=['Somme', 'Moyenne'],
            index=0
        )
    
    if selected_metrics:
        # Préparation des données pour le graphique
        df_plot = df.copy()
        
        # Groupement selon la résolution
        if resolution == 'Jour':
            df_plot['period'] = df_plot['date']
        elif resolution == 'Semaine':
            df_plot['period'] = df_plot['date'] - pd.to_timedelta(df_plot['date'].dt.dayofweek, unit='D')
        else:  # Mois
            df_plot['period'] = df_plot['date'].dt.to_period('M').astype(str)
        
        # Création du graphique avec Plotly
        fig = px.line(
            template="plotly_dark"
        )
        
        # Configuration du thème sombre uniforme
        fig = configure_plotly_theme(fig, "Évolution des métriques dans le temps")
        
        # Ajout des séries
        for metric_name in selected_metrics:
            metric_col = metrics[metric_name]
            
            # Agrégation des données
            if aggregation == 'Somme':
                grouped_data = df_plot.groupby('period')[metric_col].sum()
            else:  # Moyenne
                grouped_data = df_plot.groupby('period')[metric_col].mean()
            
            # Ajout de la série au graphique
            fig.add_scatter(
                x=grouped_data.index,
                y=grouped_data.values,
                name=metric_name,
                hovertemplate="%{y:,.0f}"
            )
        
        # Configuration du graphique
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Valeur",
            hovermode='x unified',
            showlegend=True,
            height=500
        )
        
        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap Jour × Heure
    st.subheader("Distribution des vues par jour et heure")
    
    # Préparation des données pour la heatmap
    df_heatmap = df.copy()
    
    # Extraction de l'heure (conversion en entier)
    df_heatmap['hour'] = df_heatmap['heure'].apply(
        lambda x: int(float(str(x).split(':')[0])) if pd.notna(x) and ':' in str(x)
        else int(float(x)) if pd.notna(x)
        else None
    )
    
    # Création de la matrice pour la heatmap
    heatmap_data = pd.pivot_table(
        df_heatmap,
        values='vues',
        index='jour_semaine',
        columns='hour',
        aggfunc='median',
        fill_value=0
    )
    
    # Réorganisation des jours dans l'ordre
    correct_order = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    heatmap_data = heatmap_data.reindex(correct_order)
    
    # Création de la heatmap avec Plotly
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Heure", y="Jour", color="Vues (médiane)"),
        aspect="auto",
        template="plotly_dark",
        color_continuous_scale="Reds"
    )
    
    # Configuration de la heatmap
    fig_heatmap = configure_plotly_theme(fig_heatmap, "Heatmap des vues par jour et heure")
    fig_heatmap.update_layout(
        height=400,
        xaxis_title="Heure",
        yaxis_title="Jour"
    )
    
    # Affichage de la heatmap
    st.plotly_chart(fig_heatmap, use_container_width=True) 

with reels:
    st.header("Analyse des Reels")
    
    if len(df_reels) == 0:
        st.warning("Aucun Reel ne correspond aux filtres sélectionnés.")
    else:
        # Informations sur les Reels
        st.subheader("Informations sur les Reels")
        
        # Conversion de la durée en secondes
        def convert_to_seconds(duree):
            if pd.isna(duree):
                return None
            try:
                if '.' in str(duree):
                    minutes, seconds = map(float, str(duree).split('.'))
                    return minutes * 60 + seconds
                elif ':' in str(duree):
                    minutes, seconds = map(float, str(duree).split(':'))
                    return minutes * 60 + seconds
                return float(duree) * 60  # Si c'est juste un nombre, on considère que ce sont des minutes
            except:
                return None

        # Calcul des durées en secondes
        df_reels['duree_secondes'] = df_reels['duree_reels'].apply(convert_to_seconds)
        
        # Calculs des statistiques
        duree_moyenne = df_reels['duree_secondes'].mean()
        duree_mediane = df_reels['duree_secondes'].median()
        nb_reels_plus_1min = len(df_reels[df_reels['duree_secondes'] > 60])
        pct_reels_plus_1min = (nb_reels_plus_1min / len(df_reels)) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nombre de Reels", len(df_reels))
        with col2:
            st.metric("Durée moyenne", f"{duree_moyenne:.0f} sec")
        with col3:
            st.metric("Durée médiane", f"{duree_mediane:.0f} sec")
        with col4:
            st.metric("Reels > 1 min", f"{pct_reels_plus_1min:.1f}%")
        
        # KPI Cards spécifiques aux Reels
        st.subheader("KPIs des Reels")
        
        # Première ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            total_vues_reels = df_reels['vues'].sum()
            st.metric("Vues totales", f"{total_vues_reels:,.0f}".replace(',', ' '))
        
        with col2:
            total_interactions_reels = df_reels['nb_interactions'].sum()
            st.metric("Interactions totales", f"{total_interactions_reels:,.0f}".replace(',', ' '))
        
        with col3:
            total_followers_reels = df_reels['followers_plus'].sum()
            st.metric("Nouveaux followers", f"{total_followers_reels:,.0f}".replace(',', ' '))
        
        # Deuxième ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            median_engagement_reels = df_reels['taux_engagement'].median()
            st.metric("Taux d'engagement médian", f"{median_engagement_reels*100:.1f}%")
        
        with col2:
            median_attraction_reels = df_reels['taux_attraction'].median()
            st.metric("Taux d'attraction médian", f"{median_attraction_reels*100:.1f}%")
        
        with col3:
            median_non_followers_reels = df_reels['pct_non_followers'].median()
            st.metric("% Non-followers médian", f"{median_non_followers_reels*100:.1f}%")
        
        # Séries temporelles des Reels
        st.subheader("Évolution temporelle des Reels")
        
        # Sélection des métriques à afficher
        metrics = {
            'Vues': 'vues',
            'Likes': 'likes',
            'Commentaires': 'commentaires',
            'Partages': 'partages',
            'Enregistrements': 'enregistrements'
        }
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_metrics = st.multiselect(
                "Métriques à afficher",
                options=list(metrics.keys()),
                default=['Vues', 'Likes'],
                key="reels_metrics"
            )
        
        with col2:
            # Sélection de la résolution temporelle
            resolution = st.selectbox(
                "Résolution",
                options=['Jour', 'Semaine', 'Mois'],
                index=0,
                key="reels_resolution"
            )
            
            # Sélection de l'agrégation
            aggregation = st.selectbox(
                "Agrégation",
                options=['Somme', 'Moyenne'],
                index=0,
                key="reels_aggregation"
            )
        
        if selected_metrics:
            # Préparation des données pour le graphique
            df_plot = df_reels.copy()
            
            # Groupement selon la résolution
            if resolution == 'Jour':
                df_plot['period'] = df_plot['date']
            elif resolution == 'Semaine':
                df_plot['period'] = df_plot['date'] - pd.to_timedelta(df_plot['date'].dt.dayofweek, unit='D')
            else:  # Mois
                df_plot['period'] = df_plot['date'].dt.to_period('M').astype(str)
            
            # Création du graphique avec Plotly
            fig = px.line(template="plotly_dark")
            
            # Ajout des séries
            for metric_name in selected_metrics:
                metric_col = metrics[metric_name]
                
                # Agrégation des données
                if aggregation == 'Somme':
                    grouped_data = df_plot.groupby('period')[metric_col].sum()
                else:  # Moyenne
                    grouped_data = df_plot.groupby('period')[metric_col].mean()
                
                # Ajout de la série au graphique
                fig.add_scatter(
                    x=grouped_data.index,
                    y=grouped_data.values,
                    name=metric_name,
                    hovertemplate="%{y:,.0f}"
                )
            
            # Configuration du thème sombre
            fig = configure_plotly_theme(fig, "Évolution des métriques dans le temps (Reels)")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Valeur",
                hovermode='x unified',
                showlegend=True,
                height=400
            )
            
            # Affichage du graphique
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse durée vs KPI
        st.subheader("Impact de la durée sur les performances")
        
        # Conversion de la durée en secondes
        df_reels['duree_secondes'] = df_reels['duree_reels'].apply(
            lambda x: int(str(x).split('.')[0])*60 + int(str(x).split('.')[1]) 
            if pd.notna(x) and '.' in str(x)
            else int(float(str(x).split(':')[0])*60 + float(str(x).split(':')[1])) 
            if pd.notna(x) and ':' in str(x)
            else None
        )
        
        # Sélection du KPI à analyser
        kpi_options = {
            "Vues": "vues",
            "Taux d'engagement": "taux_engagement",
            "Taux d'attraction": "taux_attraction",
            "% Non-followers": "pct_non_followers"
        }
        
        selected_kpi = st.selectbox(
            "KPI à analyser",
            options=list(kpi_options.keys()),
            key="reels_kpi"
        )
        
        # Modification des scatter plots pour retirer LOWESS
        fig_scatter = px.scatter(
            df_reels,
            x='duree_secondes',
            y=kpi_options[selected_kpi],
            labels={
                'duree_secondes': 'Durée (secondes)',
                kpi_options[selected_kpi]: selected_kpi
            },
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_scatter = configure_plotly_theme(fig_scatter, f"Relation entre la durée et {selected_kpi}")
        fig_scatter.update_layout(height=400)
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Analyse par segments
        st.subheader("Analyse par segments")
        
        # Sélection du segment
        segment_options = {
            "Contenu": "contenu",
            "Période": "periode",
            "Hashtags": "hashtags"
        }
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_segment = st.selectbox(
                "Segment à analyser",
                options=list(segment_options.keys()),
                key="reels_segment"
            )
        
        with col2:
            selected_metric = st.selectbox(
                "Métrique à analyser",
                options=list(kpi_options.keys()),
                key="reels_segment_metric"
            )
        
        # Calcul des moyennes par segment
        segment_col = segment_options[selected_segment]
        metric_col = kpi_options[selected_metric]
        
        segment_means = df_reels.groupby(segment_col)[metric_col].mean().sort_values(ascending=False)
        
        # Création du graphique en barres
        fig_bars = px.bar(
            segment_means,
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_bars = configure_plotly_theme(fig_bars, f"Moyenne de {selected_metric} par {selected_segment}")
        fig_bars.update_layout(
            xaxis_title=selected_segment,
            yaxis_title=f"Moyenne de {selected_metric}",
            height=400,
            showlegend=False
        )
        
        # Formatage des valeurs selon le type de métrique
        if "taux" in metric_col.lower() or "pct" in metric_col.lower():
            fig_bars.update_traces(
                hovertemplate="%{y:.1%}"
            )
            fig_bars.update_layout(
                yaxis_tickformat=".1%"
            )
        else:
            fig_bars.update_traces(
                hovertemplate="%{y:,.0f}"
            )
        
        st.plotly_chart(fig_bars, use_container_width=True) 

with photos:
    st.header("Analyse des Photos")
    
    if len(df_photos) == 0:
        st.warning("Aucune Photo ne correspond aux filtres sélectionnés.")
    else:
        # Informations sur les Photos
        st.subheader("Informations sur les Photos")
        
        # Calculs des statistiques
        photos_avec_hashtags = len(df_photos[df_photos['hashtags'] > 0])
        pct_photos_hashtags = (photos_avec_hashtags / len(df_photos)) * 100
        photos_avec_collab = df_photos['collab'].sum()
        pct_photos_collab = (photos_avec_collab / len(df_photos)) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nombre de Photos", len(df_photos))
        with col2:
            st.metric("% avec hashtags", f"{pct_photos_hashtags:.1f}%")
        with col3:
            st.metric("% collaborations", f"{pct_photos_collab:.1f}%")
        with col4:
            st.metric("Moyenne hashtags", f"{df_photos['hashtags'].mean():.1f}")
        
        # KPI Cards spécifiques aux Photos
        st.subheader("KPIs des Photos")
        
        # Première ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            total_vues_photos = df_photos['vues'].sum()
            st.metric("Vues totales", f"{total_vues_photos:,.0f}".replace(',', ' '))
        
        with col2:
            total_interactions_photos = df_photos['nb_interactions'].sum()
            st.metric("Interactions totales", f"{total_interactions_photos:,.0f}".replace(',', ' '))
        
        with col3:
            total_followers_photos = df_photos['followers_plus'].sum()
            st.metric("Nouveaux followers", f"{total_followers_photos:,.0f}".replace(',', ' '))
        
        # Deuxième ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            median_engagement_photos = df_photos['taux_engagement'].median()
            st.metric("Taux d'engagement médian", f"{median_engagement_photos*100:.1f}%")
        
        with col2:
            median_attraction_photos = df_photos['taux_attraction'].median()
            st.metric("Taux d'attraction médian", f"{median_attraction_photos*100:.1f}%")
        
        with col3:
            median_non_followers_photos = df_photos['pct_non_followers'].median()
            st.metric("% Non-followers médian", f"{median_non_followers_photos*100:.1f}%")
        
        # Séries temporelles des Photos
        st.subheader("Évolution temporelle des Photos")
        
        # Sélection des métriques à afficher
        metrics = {
            'Vues': 'vues',
            'Likes': 'likes',
            'Commentaires': 'commentaires',
            'Partages': 'partages',
            'Enregistrements': 'enregistrements'
        }
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_metrics = st.multiselect(
                "Métriques à afficher",
                options=list(metrics.keys()),
                default=['Vues', 'Likes'],
                key="photos_metrics"
            )
        
        with col2:
            # Sélection de la résolution temporelle
            resolution = st.selectbox(
                "Résolution",
                options=['Jour', 'Semaine', 'Mois'],
                index=0,
                key="photos_resolution"
            )
            
            # Sélection de l'agrégation
            aggregation = st.selectbox(
                "Agrégation",
                options=['Somme', 'Moyenne'],
                index=0,
                key="photos_aggregation"
            )
        
        if selected_metrics:
            # Préparation des données pour le graphique
            df_plot = df_photos.copy()
            
            # Groupement selon la résolution
            if resolution == 'Jour':
                df_plot['period'] = df_plot['date']
            elif resolution == 'Semaine':
                df_plot['period'] = df_plot['date'] - pd.to_timedelta(df_plot['date'].dt.dayofweek, unit='D')
            else:  # Mois
                df_plot['period'] = df_plot['date'].dt.to_period('M').astype(str)
            
            # Création du graphique avec Plotly
            fig = px.line(template="plotly_dark")
            
            # Ajout des séries
            for metric_name in selected_metrics:
                metric_col = metrics[metric_name]
                
                # Agrégation des données
                if aggregation == 'Somme':
                    grouped_data = df_plot.groupby('period')[metric_col].sum()
                else:  # Moyenne
                    grouped_data = df_plot.groupby('period')[metric_col].mean()
                
                # Ajout de la série au graphique
                fig.add_scatter(
                    x=grouped_data.index,
                    y=grouped_data.values,
                    name=metric_name,
                    hovertemplate="%{y:,.0f}"
                )
            
            # Configuration du thème sombre
            fig = configure_plotly_theme(fig, "Évolution des métriques dans le temps (Photos)")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Valeur",
                hovermode='x unified',
                showlegend=True,
                height=400
            )
            
            # Affichage du graphique
            st.plotly_chart(fig, use_container_width=True)
        
        # Distribution des enregistrements pour 1000 vues
        st.subheader("Distribution des enregistrements")
        
        # Calcul du taux d'enregistrement pour 1000 vues
        df_photos['enregistrements_1k'] = (df_photos['enregistrements'] / df_photos['vues']) * 1000
        
        # Création de l'histogramme
        fig_hist = px.histogram(
            df_photos,
            x='enregistrements_1k',
            nbins=20,
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_hist = configure_plotly_theme(fig_hist, "Distribution des enregistrements pour 1000 vues")
        fig_hist.update_layout(
            xaxis_title="Enregistrements pour 1000 vues",
            yaxis_title="Nombre de photos",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Analyse par segments
        st.subheader("Analyse par segments")
        
        # Sélection du segment et de la métrique
        col1, col2 = st.columns([2, 1])
        
        segment_options = {
            "Contenu": "contenu",
            "Période": "periode",
            "Hashtags": "hashtags"
        }
        
        kpi_options = {
            "Vues": "vues",
            "Taux d'engagement": "taux_engagement",
            "Taux d'attraction": "taux_attraction",
            "% Non-followers": "pct_non_followers",
            "Enregistrements/1k vues": "enregistrements_1k"
        }
        
        with col1:
            selected_segment = st.selectbox(
                "Segment à analyser",
                options=list(segment_options.keys()),
                key="photos_segment"
            )
        
        with col2:
            selected_metric = st.selectbox(
                "Métrique à analyser",
                options=list(kpi_options.keys()),
                key="photos_segment_metric"
            )
        
        # Calcul des moyennes par segment
        segment_col = segment_options[selected_segment]
        metric_col = kpi_options[selected_metric]
        
        segment_means = df_photos.groupby(segment_col)[metric_col].mean().sort_values(ascending=False)
        
        # Création du graphique en barres
        fig_bars = px.bar(
            segment_means,
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_bars = configure_plotly_theme(fig_bars, f"Moyenne de {selected_metric} par {selected_segment}")
        fig_bars.update_layout(
            xaxis_title=selected_segment,
            yaxis_title=f"Moyenne de {selected_metric}",
            height=400,
            showlegend=False
        )
        
        # Formatage des valeurs selon le type de métrique
        if "taux" in metric_col.lower() or "pct" in metric_col.lower():
            fig_bars.update_traces(
                hovertemplate="%{y:.1%}"
            )
            fig_bars.update_layout(
                yaxis_tickformat=".1%"
            )
        else:
            fig_bars.update_traces(
                hovertemplate="%{y:,.1f}"
            )
        
        st.plotly_chart(fig_bars, use_container_width=True) 

with carousel:
    st.header("Analyse des Carrousels")
    
    if len(df_carousel) == 0:
        st.warning("Aucun Carrousel ne correspond aux filtres sélectionnés.")
    else:
        # Informations sur les Carrousels
        st.subheader("Informations sur les Carrousels")
        
        # Calculs des statistiques
        nb_images_moyen = df_carousel['nb_images_carousel'].mean()
        nb_images_median = df_carousel['nb_images_carousel'].median()
        carousel_max_images = df_carousel['nb_images_carousel'].max()
        carousel_plus_5_images = len(df_carousel[df_carousel['nb_images_carousel'] > 5])
        pct_carousel_plus_5 = (carousel_plus_5_images / len(df_carousel)) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nombre de Carrousels", len(df_carousel))
        with col2:
            st.metric("Images moyennes", f"{nb_images_moyen:.1f}")
        with col3:
            st.metric("Images médianes", f"{nb_images_median:.0f}")
        with col4:
            st.metric("Carrousels > 5 imgs", f"{pct_carousel_plus_5:.1f}%")
        
        # KPI Cards spécifiques aux Carrousels
        st.subheader("KPIs des Carrousels")
        
        # Première ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            total_vues_carousel = df_carousel['vues'].sum()
            st.metric("Vues totales", f"{total_vues_carousel:,.0f}".replace(',', ' '))
        
        with col2:
            total_interactions_carousel = df_carousel['nb_interactions'].sum()
            st.metric("Interactions totales", f"{total_interactions_carousel:,.0f}".replace(',', ' '))
        
        with col3:
            total_followers_carousel = df_carousel['followers_plus'].sum()
            st.metric("Nouveaux followers", f"{total_followers_carousel:,.0f}".replace(',', ' '))
        
        # Deuxième ligne de KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            median_engagement_carousel = df_carousel['taux_engagement'].median()
            st.metric("Taux d'engagement médian", f"{median_engagement_carousel*100:.1f}%")
        
        with col2:
            median_attraction_carousel = df_carousel['taux_attraction'].median()
            st.metric("Taux d'attraction médian", f"{median_attraction_carousel*100:.1f}%")
        
        with col3:
            median_non_followers_carousel = df_carousel['pct_non_followers'].median()
            st.metric("% Non-followers médian", f"{median_non_followers_carousel*100:.1f}%")
        
        # Séries temporelles des Carrousels
        st.subheader("Évolution temporelle des Carrousels")
        
        # Sélection des métriques à afficher
        metrics = {
            'Vues': 'vues',
            'Likes': 'likes',
            'Commentaires': 'commentaires',
            'Partages': 'partages',
            'Enregistrements': 'enregistrements'
        }
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_metrics = st.multiselect(
                "Métriques à afficher",
                options=list(metrics.keys()),
                default=['Vues', 'Likes'],
                key="carousel_metrics"
            )
        
        with col2:
            # Sélection de la résolution temporelle
            resolution = st.selectbox(
                "Résolution",
                options=['Jour', 'Semaine', 'Mois'],
                index=0,
                key="carousel_resolution"
            )
            
            # Sélection de l'agrégation
            aggregation = st.selectbox(
                "Agrégation",
                options=['Somme', 'Moyenne'],
                index=0,
                key="carousel_aggregation"
            )
        
        if selected_metrics:
            # Préparation des données pour le graphique
            df_plot = df_carousel.copy()
            
            # Groupement selon la résolution
            if resolution == 'Jour':
                df_plot['period'] = df_plot['date']
            elif resolution == 'Semaine':
                df_plot['period'] = df_plot['date'] - pd.to_timedelta(df_plot['date'].dt.dayofweek, unit='D')
            else:  # Mois
                df_plot['period'] = df_plot['date'].dt.to_period('M').astype(str)
            
            # Création du graphique avec Plotly
            fig = px.line(template="plotly_dark")
            
            # Ajout des séries
            for metric_name in selected_metrics:
                metric_col = metrics[metric_name]
                
                # Agrégation des données
                if aggregation == 'Somme':
                    grouped_data = df_plot.groupby('period')[metric_col].sum()
                else:  # Moyenne
                    grouped_data = df_plot.groupby('period')[metric_col].mean()
                
                # Ajout de la série au graphique
                fig.add_scatter(
                    x=grouped_data.index,
                    y=grouped_data.values,
                    name=metric_name,
                    hovertemplate="%{y:,.0f}"
                )
            
            # Configuration du thème sombre
            fig = configure_plotly_theme(fig, "Évolution des métriques dans le temps (Carrousels)")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Valeur",
                hovermode='x unified',
                showlegend=True,
                height=400
            )
            
            # Affichage du graphique
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse nombre d'images vs KPI
        st.subheader("Impact du nombre d'images sur les performances")
        
        # Sélection du KPI à analyser
        kpi_options = {
            "Vues": "vues",
            "Taux d'engagement": "taux_engagement",
            "Taux d'attraction": "taux_attraction",
            "% Non-followers": "pct_non_followers"
        }
        
        selected_kpi = st.selectbox(
            "KPI à analyser",
            options=list(kpi_options.keys()),
            key="carousel_kpi"
        )
        
        # Modification des scatter plots pour retirer LOWESS
        fig_scatter = px.scatter(
            df_carousel,
            x='nb_images_carousel',
            y=kpi_options[selected_kpi],
            labels={
                'nb_images_carousel': "Nombre d'images",
                kpi_options[selected_kpi]: selected_kpi
            },
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_scatter = configure_plotly_theme(fig_scatter, f"Relation entre le nombre d'images et {selected_kpi}")
        fig_scatter.update_layout(height=400)
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Analyse par segments
        st.subheader("Analyse par segments")
        
        # Sélection du segment et de la métrique
        col1, col2 = st.columns([2, 1])
        
        segment_options = {
            "Contenu": "contenu",
            "Période": "periode",
            "Hashtags": "hashtags"
        }
        
        with col1:
            selected_segment = st.selectbox(
                "Segment à analyser",
                options=list(segment_options.keys()),
                key="carousel_segment"
            )
        
        with col2:
            selected_metric = st.selectbox(
                "Métrique à analyser",
                options=list(kpi_options.keys()),
                key="carousel_segment_metric"
            )
        
        # Calcul des moyennes par segment
        segment_col = segment_options[selected_segment]
        metric_col = kpi_options[selected_metric]
        
        segment_means = df_carousel.groupby(segment_col)[metric_col].mean().sort_values(ascending=False)
        
        # Création du graphique en barres
        fig_bars = px.bar(
            segment_means,
            template="plotly_dark"
        )
        
        # Configuration du thème sombre
        fig_bars = configure_plotly_theme(fig_bars, f"Moyenne de {selected_metric} par {selected_segment}")
        fig_bars.update_layout(
            xaxis_title=selected_segment,
            yaxis_title=f"Moyenne de {selected_metric}",
            height=400,
            showlegend=False
        )
        
        # Formatage des valeurs selon le type de métrique
        if "taux" in metric_col.lower() or "pct" in metric_col.lower():
            fig_bars.update_traces(
                hovertemplate="%{y:.1%}"
            )
            fig_bars.update_layout(
                yaxis_tickformat=".1%"
            )
        else:
            fig_bars.update_traces(
                hovertemplate="%{y:,.0f}"
            )
        
        st.plotly_chart(fig_bars, use_container_width=True) 

with charts:
    st.header("Graphiques personnalisables")
    
    # Définition des métriques disponibles
    metrics = {
        "Vues": "vues",
        "Likes": "likes",
        "Commentaires": "commentaires",
        "Partages": "partages",
        "Enregistrements": "enregistrements",
        "Taux d'engagement": "taux_engagement",
        "Taux d'attraction": "taux_attraction",
        "% Non-followers": "pct_non_followers",
        "Visites profil": "visites_profil",
        "Nouveaux followers": "followers_plus",
        "Clics externes": "clics_externes"
    }
    
    # Définition des segments disponibles
    segments = {
        "Type": "type",
        "Contenu": "contenu",
        "Période": "periode",
        "Jour de la semaine": "jour_semaine",
        "Heure": "heure_bin",
        "Collaboration": "collab",
        "Hashtags": "hashtags"
    }
    
    # Définition des combinaisons de segments
    segment_combinations = {
        "Type × Contenu": ["type", "contenu"],
        "Type × Période": ["type", "periode"],
        "Contenu × Période": ["contenu", "periode"]
    }
    
    # Configuration du graphique
    st.subheader("Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sélection des métriques
        selected_metrics = st.multiselect(
            "Métriques à afficher",
            options=list(metrics.keys()),
            default=["Vues"],
            key="custom_metrics"
        )
        
        # Sélection du segment
        segment_options = list(segments.keys()) + list(segment_combinations.keys())
        selected_segment = st.selectbox(
            "Segment d'analyse",
            options=segment_options,
            key="custom_segment"
        )
    
    with col2:
        # Type de graphique
        chart_type = st.selectbox(
            "Type de graphique",
            options=["Barres", "Camembert", "Lignes"],
            key="custom_chart_type"
        )
        
        # Type d'agrégation
        aggregation = st.selectbox(
            "Agrégation",
            options=["Moyenne", "Somme"],
            key="custom_aggregation"
        )
    
    if selected_metrics and selected_segment:
        # Préparation des données
        df_plot = df.copy()
        
        # Gestion des segments combinés
        if selected_segment in segment_combinations:
            segment_cols = segment_combinations[selected_segment]
            df_plot['segment'] = df_plot[segment_cols].apply(lambda x: ' × '.join(x.astype(str)), axis=1)
        else:
            segment_cols = [segments[selected_segment]]
            df_plot['segment'] = df_plot[segments[selected_segment]]
        
        # Création du DataFrame des agrégats
        agg_data = []
        
        for metric_name in selected_metrics:
            metric_col = metrics[metric_name]
            
            # Calcul des agrégats
            if aggregation == "Moyenne":
                grouped = df_plot.groupby('segment')[metric_col].mean()
            else:  # Somme
                grouped = df_plot.groupby('segment')[metric_col].sum()
            
            # Conversion en DataFrame
            df_agg = grouped.reset_index()
            df_agg['metric'] = metric_name
            df_agg = df_agg.rename(columns={metric_col: 'value'})
            agg_data.append(df_agg)
        
        # Combinaison des agrégats
        df_agg = pd.concat(agg_data, ignore_index=True)
        
        # Création du graphique selon le type choisi
        if chart_type == "Barres":
            if len(selected_metrics) == 1:
                # Une seule métrique : barres simples
                fig = px.bar(
                    df_agg,
                    x='segment',
                    y='value',
                    template="plotly_dark"
                )
            else:
                # Plusieurs métriques : barres groupées
                fig = px.bar(
                    df_agg,
                    x='segment',
                    y='value',
                    color='metric',
                    barmode='group',
                    template="plotly_dark"
                )
        
        elif chart_type == "Camembert":
            if len(selected_metrics) > 1:
                st.warning("Le graphique en camembert n'est disponible que pour une seule métrique.")
            else:
                fig = px.pie(
                    df_agg,
                    values='value',
                    names='segment',
                    template="plotly_dark"
                )
        
        else:  # Lignes
            fig = px.line(
                df_agg,
                x='segment',
                y='value',
                color='metric',
                markers=True,
                template="plotly_dark"
            )
        
        # Configuration du thème sombre uniforme
        fig = configure_plotly_theme(fig, f"{aggregation} par {selected_segment}")
        fig.update_layout(
            height=500,
            xaxis_title=selected_segment,
            yaxis_title=f"{aggregation}"
        )
        
        # Formatage des valeurs selon le type de métrique
        has_percentage = any("taux" in m.lower() or "%" in m for m in selected_metrics)
        if has_percentage:
            fig.update_layout(yaxis_tickformat=".1%")
        
        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)
        
        # Export des données
        st.subheader("Exporter les données")
        
        # Préparation du CSV
        csv = df_agg.to_csv(index=False).encode('utf-8')
        
        # Bouton de téléchargement
        st.download_button(
            "Télécharger les données (CSV)",
            csv,
            "agregats.csv",
            "text/csv",
            key="download_custom_chart"
        ) 

# Style pour l'explorateur de données
st.markdown("""
<style>
    /* Styles existants ... */

    /* Styles pour l'explorateur de données */
    .dataframe {
        font-size: 0.9rem !important;
    }

    .dataframe td, .dataframe th {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
        padding: 8px 12px !important;
    }

    .dataframe th {
        background-color: rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
    }

    .dataframe tr:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* Style pour les liens dans le tableau */
    .dataframe a {
        color: var(--moe-pink) !important;
        text-decoration: none !important;
    }

    .dataframe a:hover {
        text-decoration: underline !important;
    }

    /* Style pour les filtres */
    .stSelectbox, .stMultiSelect {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour formater les liens Instagram
def format_instagram_link(link):
    return f'<a href="{link}" target="_blank">Voir le post</a>'

# Fonction pour formater les nombres avec séparateur de milliers
def format_number(value):
    if pd.isna(value):
        return ""
    if isinstance(value, (int, float)):
        return f"{value:,.0f}".replace(",", " ")
    return value

# Colonnes à afficher dans l'explorateur
EXPLORER_COLUMNS = [
    'date', 'heure', 'type', 'titre', 'lien', 'vues', 'nb_interactions',
    'taux_engagement', 'taux_attraction', 'duree_reels', 'nb_images_carousel'
]

# Onglet Explorer
with explorer:
    st.header("Explorateur de données")
    
    # Filtres
    col1, col2, col3 = st.columns(3)

    with col1:
        type_filter = st.multiselect(
            "Type de contenu",
            options=['Photo', 'Reels', 'Carousel'],
            default=None,
            key='explorer_type_filter'
        )

    with col2:
        date_range = st.date_input(
            "Période",
            value=(df['date'].min(), df['date'].max()),
            key='explorer_date_range'
        )

    with col3:
        search_term = st.text_input(
            "Rechercher dans les titres",
            key='explorer_search'
        )

    # Application des filtres
    filtered_df = df.copy()

    if type_filter:
        filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) &
            (filtered_df['date'].dt.date <= date_range[1])
        ]

    if search_term:
        filtered_df = filtered_df[
            filtered_df['titre'].str.contains(search_term, case=False, na=False)
        ]

    # Préparation des données pour l'affichage
    display_df = filtered_df[EXPLORER_COLUMNS].copy()

    # Formatage des colonnes
    display_df['date'] = display_df['date'].dt.strftime('%d/%m/%Y')
    
    # Renommage des colonnes pour un meilleur affichage
    column_names = {
        'date': 'Date',
        'heure': 'Heure',
        'type': 'Type',
        'titre': 'Titre',
        'lien': 'Lien',
        'vues': 'Vues',
        'nb_interactions': 'Interactions',
        'taux_engagement': "Taux d'engagement",
        'taux_attraction': "Taux d'attraction",
        'duree_reels': 'Durée',
        'nb_images_carousel': 'Images'
    }
    display_df = display_df.rename(columns=column_names)

    # Configuration de la hauteur du tableau
    height = min(400, len(display_df) * 35 + 38)

    # Affichage du tableau interactif
    st.dataframe(
        display_df,
        use_container_width=True,
        height=height,
        hide_index=True,
        column_config={
            "Lien": st.column_config.LinkColumn(
                "Lien",
                display_text="Voir le post",
                help="Cliquez pour voir le post sur Instagram"
            ),
            "Date": st.column_config.TextColumn(
                "Date",
                help="Date de publication",
                width="small"
            ),
            "Heure": st.column_config.TextColumn(
                "Heure",
                help="Heure de publication",
                width="small"
            ),
            "Type": st.column_config.TextColumn(
                "Type",
                help="Type de contenu",
                width="small"
            ),
            "Vues": st.column_config.NumberColumn(
                "Vues",
                help="Nombre de vues",
                format="%d"
            ),
            "Interactions": st.column_config.NumberColumn(
                "Interactions",
                help="Nombre total d'interactions",
                format="%d"
            ),
            "Taux d'engagement": st.column_config.NumberColumn(
                "Taux d'engagement",
                help="Taux d'engagement",
                format="%.1f%%"
            ),
            "Taux d'attraction": st.column_config.NumberColumn(
                "Taux d'attraction",
                help="Taux d'attraction",
                format="%.1f%%"
            ),
            "Durée": st.column_config.TextColumn(
                "Durée",
                help="Durée des Reels",
                width="small"
            ),
            "Images": st.column_config.NumberColumn(
                "Images",
                help="Nombre d'images dans le carousel",
                format="%d"
            )
        }
    )

    # Affichage du nombre de résultats
    st.markdown(f"*{len(display_df)} posts affichés*")
    
    # Export des données complètes
    st.subheader("Exporter les données")
    
    # Préparation du DataFrame pour l'export
    export_df = df.copy()
    
    # Renommage des colonnes pour l'export
    export_columns = {
        'date': 'Date',
        'heure': 'Heure',
        'periode': 'Période',
        'type': 'Type',
        'titre': 'Titre',
        'lien': 'Lien',
        'contenu': 'Contenu',
        'collab': 'Collaboration',
        'duree_reels': 'Durée Reels',
        'nb_images_carousel': 'Nombre Images Carrousel',
        'vues': 'Vues',
        'vues_followers': 'Vues Followers',
        'vues_non_followers': 'Vues Non-Followers',
        'nb_interactions': 'Interactions',
        'likes': 'Likes',
        'commentaires': 'Commentaires',
        'partages': 'Partages',
        'enregistrements': 'Enregistrements',
        'activite_profil': 'Activité Profil',
        'visites_profil': 'Visites Profil',
        'followers_plus': 'Nouveaux Followers',
        'clics_externes': 'Clics Externes',
        'hashtags': 'Hashtags',
        'jour_semaine': 'Jour de la Semaine',
        'heure_bin': 'Période de la Journée',
        'taux_engagement': "Taux d'Engagement",
        'taux_attraction': "Taux d'Attraction",
        'profile_visit_rate': 'Taux de Visite Profil',
        'follow_rate': 'Taux de Follow',
        'external_ctr': 'Taux de Clic Externe',
        'pct_non_followers': '% Non-Followers'
    }
    
    export_df = export_df.rename(columns=export_columns)
    
    # Formatage des colonnes pour l'export
    export_df['Date'] = export_df['Date'].dt.strftime('%Y-%m-%d')
    export_df['Collaboration'] = export_df['Collaboration'].map({True: 'Oui', False: 'Non'})
    
    # Conversion des taux en pourcentages
    rate_columns = ["Taux d'Engagement", "Taux d'Attraction", 'Taux de Visite Profil', 
                   'Taux de Follow', 'Taux de Clic Externe', '% Non-Followers']
    for col in rate_columns:
        export_df[col] = export_df[col].multiply(100).round(2)
    
    # Création du fichier CSV
    csv = export_df.to_csv(index=False, encoding='utf-8-sig', sep=';')
    
    # Bouton de téléchargement
    st.download_button(
        "📥 Télécharger toutes les données (CSV)",
        csv,
        "moe_instagram_analytics.csv",
        "text/csv",
        help="Télécharger toutes les données avec les métriques calculées au format CSV"
    ) 
