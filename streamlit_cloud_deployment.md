# 🚀 Guide de Déploiement Streamlit Cloud

## 📋 Prérequis

1. **Compte GitHub** : Votre code doit être sur GitHub
2. **Compte Streamlit Cloud** : Créer un compte sur [share.streamlit.io](https://share.streamlit.io)
3. **Code prêt** : Votre application doit fonctionner localement

## 🔧 Préparation du Code

### 1. Vérifier la structure du projet
```
Pricing/
├── app.py                          # ✅ Point d'entrée principal
├── black_scholes_calculator.py     # ✅ Module de calcul
├── requirements.txt                 # ✅ Dépendances
├── .streamlit/
│   └── config.toml                # ✅ Configuration
├── README.md                       # ✅ Documentation
└── .gitignore                      # ✅ Fichiers ignorés
```

### 2. Vérifier le fichier `requirements.txt`
```txt
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
```

### 3. Vérifier le fichier `app.py`
- ✅ Point d'entrée principal : `streamlit run app.py`
- ✅ Pas de chemins absolus
- ✅ Pas de variables d'environnement locales

## 🌐 Déploiement sur Streamlit Cloud

### Étape 1 : Pousser le code sur GitHub

```bash
# Vérifier le statut
git status

# Ajouter tous les fichiers
git add .

# Commiter les changements
git commit -m "Préparation pour déploiement Streamlit Cloud"

# Pousser sur GitHub
git push origin main
```

### Étape 2 : Se connecter à Streamlit Cloud

1. Aller sur [share.streamlit.io](https://share.streamlit.io)
2. Cliquer sur "Sign in with GitHub"
3. Autoriser l'accès à vos repositories

### Étape 3 : Créer une nouvelle application

1. Cliquer sur **"New app"**
2. Remplir les informations :
   - **Repository** : Sélectionner votre repository `Pricing`
   - **Branch** : `main`
   - **Main file path** : `app.py`
   - **Python version** : `3.9` (recommandé)

### Étape 4 : Configurer l'application

#### Paramètres recommandés :
- **Repository** : `votre-username/Pricing`
- **Branch** : `main`
- **Main file path** : `app.py`
- **Python version** : `3.9`
- **Advanced settings** : Laisser par défaut

### Étape 5 : Déployer

1. Cliquer sur **"Deploy!"**
2. Attendre 2-5 minutes pour le déploiement
3. Votre application sera disponible à l'URL fournie

## 🔍 Vérification du Déploiement

### ✅ Points à vérifier :

1. **Page de chargement** : L'application se charge sans erreur
2. **Interface** : Tous les widgets s'affichent correctement
3. **Calculs** : Les calculs fonctionnent comme en local
4. **Graphiques** : Les visualisations Plotly s'affichent
5. **Performance** : L'application répond rapidement

### ❌ Problèmes courants :

#### Erreur "Module not found"
- Vérifier que toutes les dépendances sont dans `requirements.txt`
- Vérifier les versions des packages

#### Erreur "File not found"
- Vérifier que `app.py` est bien le point d'entrée
- Vérifier le chemin dans la configuration

#### Erreur de calcul
- Vérifier que le code fonctionne en local
- Tester avec des valeurs simples

## 🛠️ Maintenance

### Mises à jour automatiques
- Chaque push sur la branche `main` déclenche un redéploiement
- Les changements sont visibles en 2-5 minutes

### Logs et debugging
- Accéder aux logs via l'interface Streamlit Cloud
- Vérifier les erreurs dans les logs

### Variables d'environnement
- Si nécessaire, ajouter des secrets via l'interface Streamlit Cloud
- Utiliser `st.secrets` dans le code

## 📊 Monitoring

### Métriques disponibles :
- **Temps de chargement** : Performance de l'application
- **Utilisation** : Nombre d'utilisateurs
- **Erreurs** : Logs d'erreurs

### Optimisations :
- **Cache** : Utiliser `@st.cache_data` pour les calculs lourds
- **Lazy loading** : Charger les données à la demande
- **Compression** : Optimiser les graphiques

## 🔗 URLs utiles

- **Streamlit Cloud** : [share.streamlit.io](https://share.streamlit.io)
- **Documentation** : [docs.streamlit.io](https://docs.streamlit.io)
- **Community** : [discuss.streamlit.io](https://discuss.streamlit.io)

## 🆘 Support

### En cas de problème :
1. Vérifier les logs dans Streamlit Cloud
2. Tester en local avec `streamlit run app.py`
3. Consulter la documentation Streamlit
4. Poster sur le forum Streamlit Community

### Ressources d'aide :
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

## ✅ Checklist de déploiement

- [ ] Code poussé sur GitHub
- [ ] `requirements.txt` à jour
- [ ] `app.py` fonctionne en local
- [ ] Pas de chemins absolus dans le code
- [ ] Pas de variables d'environnement locales
- [ ] Application déployée sur Streamlit Cloud
- [ ] Interface fonctionne correctement
- [ ] Calculs fonctionnent
- [ ] Graphiques s'affichent
- [ ] Performance satisfaisante

🎉 **Félicitations ! Votre application est maintenant déployée sur Streamlit Cloud !** 