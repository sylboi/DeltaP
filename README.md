# Calculateur de Couverture de Prix - Black & Scholes

## 📊 Description

Cet outil calcule le delta prix entre aujourd'hui et la date de livraison d'un contrat en utilisant le modèle Black & Scholes pour déterminer la couverture de prix optimale.

## 🎯 Objectif

L'objectif est de connaître la couverture de prix à appliquer en fonction de :
- La volatilité du sous-jacent
- Le centile de couverture souhaité
- Le prix actuel du sous-jacent
- La date de livraison du contrat

## 🚀 Installation

1. **Cloner le projet** :
```bash
git clone <repository-url>
cd Pricing
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Lancer l'application** :
```bash
streamlit run app.py
```

## 📈 Fonctionnalités

### Calculs principaux
- **Delta prix** : Différence entre le prix de livraison et le prix actuel
- **Prix d'exercice (strike)** : Calculé selon le centile de couverture
- **Prix des options** : Call et Put selon Black & Scholes
- **Deltas des options** : Sensibilité des options au prix du sous-jacent

### Visualisations
- **Distribution des prix futurs** : Histogramme des scénarios
- **Évolution temporelle** : Graphique avec bandes de confiance
- **Statistiques** : Moyenne, écart-type, centiles

### Recommandations
- **Couverture haussière** : Si le prix de livraison > prix actuel
- **Couverture baissière** : Si le prix de livraison < prix actuel

## ⚙️ Paramètres d'entrée

### Prix actuel du sous-jacent
- **Type** : Nombre décimal
- **Unité** : Euros (€)
- **Plage** : 0.01 - 10,000 €

### Date de livraison
- **Type** : Date
- **Contrainte** : Doit être dans le futur
- **Format** : JJ/MM/AAAA

### Volatilité annuelle
- **Type** : Pourcentage
- **Plage** : 1% - 100%
- **Défaut** : 20%

### Centile de couverture
- **Type** : Pourcentage
- **Plage** : 1% - 99%
- **Défaut** : 95%
- **Description** : Niveau de confiance pour la couverture

### Taux d'intérêt sans risque
- **Type** : Pourcentage
- **Plage** : 0% - 10%
- **Défaut** : 2%

## 📊 Sorties

### Métriques principales
- **Prix actuel** : Prix du sous-jacent aujourd'hui
- **Prix de livraison** : Prix calculé pour la date de livraison
- **Delta prix** : Différence entre les deux prix
- **Temps jusqu'à livraison** : Nombre de jours restants

### Options de couverture
- **Option Call** : Prix et delta de l'option d'achat
- **Option Put** : Prix et delta de l'option de vente

### Analyses statistiques
- **Prix moyen futur** : Moyenne des scénarios simulés
- **Écart-type** : Dispersion des prix futurs
- **95ème centile** : Seuil de risque à 95%

## 🔧 Modèle Black & Scholes

### Formule du prix d'une option call :
```
C = S * N(d1) - K * e^(-rT) * N(d2)
```

### Formule du prix d'une option put :
```
P = K * e^(-rT) * N(-d2) - S * N(-d1)
```

Où :
- `S` = Prix actuel du sous-jacent
- `K` = Prix d'exercice
- `T` = Temps jusqu'à l'échéance
- `r` = Taux d'intérêt sans risque
- `σ` = Volatilité
- `N()` = Fonction de distribution normale

## 💡 Utilisation

1. **Saisir les paramètres** dans la barre latérale
2. **Cliquer sur "Calculer la couverture"**
3. **Analyser les résultats** :
   - Métriques principales
   - Détails des options
   - Graphiques de distribution
   - Recommandations de couverture

## 🎯 Cas d'usage

### Exemple 1 : Couverture haussière
- **Prix actuel** : 100 €
- **Prix de livraison** : 110 €
- **Recommandation** : Acheter des options call

### Exemple 2 : Couverture baissière
- **Prix actuel** : 100 €
- **Prix de livraison** : 90 €
- **Recommandation** : Acheter des options put

## 📁 Structure du projet

```
Pricing/
├── app.py                      # Application Streamlit
├── black_scholes_calculator.py # Module de calcul
├── requirements.txt            # Dépendances Python
└── README.md                  # Documentation
```

## 🔍 Détails techniques

### Calcul du prix d'exercice
Le prix d'exercice est calculé en utilisant la distribution log-normale :
```
K = S * exp((r - 0.5*σ²)T + z*σ*√T)
```
Où `z` est le quantile correspondant au centile de couverture.

### Simulation des scénarios
- **1000 scénarios** générés par simulation Monte Carlo
- **Distribution log-normale** pour l'évolution des prix
- **Seed fixe** pour la reproductibilité

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche feature
3. Implémenter les modifications
4. Soumettre une pull request

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub. 