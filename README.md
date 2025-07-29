# Calculateur de Couverture de Prix - Black & Scholes

## 📊 Description

Application Streamlit pour calculer le delta prix entre aujourd'hui et la date de livraison d'un contrat en utilisant le modèle Black & Scholes pour déterminer la couverture de prix optimale.

## 🚀 Fonctionnalités

- **Calcul de couverture de prix** basé sur le modèle Black & Scholes
- **Simulation de scénarios** avec analyse de distribution des prix futurs
- **Analyse de volatilité** et calcul des centiles de risque
- **Recommandations de couverture** selon le type d'exposition volume
- **Visualisations interactives** avec Plotly
- **Interface intuitive** avec paramètres configurables

## 🛠️ Installation locale

```bash
# Cloner le repository
git clone <votre-repo-url>
cd Pricing

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📋 Dépendances

- `streamlit>=1.28.0` - Interface web
- `numpy>=1.24.0` - Calculs numériques
- `scipy>=1.11.0` - Fonctions statistiques
- `pandas>=2.0.0` - Manipulation de données
- `plotly>=5.15.0` - Visualisations interactives
- `matplotlib>=3.7.0` - Graphiques

## 🎯 Utilisation

1. **Paramètres d'entrée** (sidebar) :
   - Prix actuel du sous-jacent
   - Dates de début et fin du contrat
   - Volatilité annuelle
   - Centile de couverture
   - Taux d'intérêt sans risque
   - Nombre de simulations

2. **Résultats affichés** :
   - Prix de livraison (strike)
   - Delta prix
   - Détails des options (call/put)
   - Distribution des prix futurs
   - Recommandations de couverture

## 🌐 Déploiement Streamlit Cloud

Cette application est configurée pour être déployée sur Streamlit Cloud.

### Étapes de déploiement :

1. **Pousser le code sur GitHub** :
   ```bash
   git add .
   git commit -m "Préparation pour déploiement Streamlit Cloud"
   git push origin main
   ```

2. **Se connecter à Streamlit Cloud** :
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Se connecter avec votre compte GitHub
   - Cliquer sur "New app"

3. **Configurer l'application** :
   - **Repository** : Sélectionner votre repository
   - **Branch** : `main`
   - **Main file path** : `app.py`
   - **Python version** : 3.9 ou supérieur

4. **Déployer** :
   - Cliquer sur "Deploy!"
   - L'application sera disponible en quelques minutes

## 📁 Structure du projet

```
Pricing/
├── app.py                          # Application principale Streamlit
├── black_scholes_calculator.py     # Module de calcul Black & Scholes
├── requirements.txt                 # Dépendances Python
├── .streamlit/
│   └── config.toml                # Configuration Streamlit
└── README.md                       # Documentation
```

## 🔧 Configuration

Le fichier `.streamlit/config.toml` contient la configuration de l'application :
- Thème personnalisé
- Paramètres serveur optimisés
- Désactivation des statistiques d'usage

## 📈 Fonctionnalités avancées

- **Simulation Monte Carlo** pour l'analyse de risque
- **Calcul des options** (call/put) selon Black & Scholes
- **Analyse de dispersion** avec centiles et statistiques
- **Évolution temporelle** du prix avec bandes de confiance
- **Recommandations contextuelles** selon l'exposition volume

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. 