# 🚀 Guide de Déploiement - Calculateur de Couverture de Prix

## 📋 Prérequis
- Compte GitHub
- Fichiers du projet dans un repository GitHub

## 🎯 Option 1 : Streamlit Cloud (Recommandé)

### Étapes :
1. **Pousser le code sur GitHub :**
```bash
git init
git add .
git commit -m "Initial commit - Calculateur de couverture de prix"
git branch -M main
git remote add origin https://github.com/votre-username/pricing-calculator.git
git push -u origin main
```

2. **Déployer sur Streamlit Cloud :**
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Se connecter avec GitHub
   - Cliquer "New app"
   - Sélectionner le repository et le fichier `app.py`
   - Cliquer "Deploy"

### Avantages :
- ✅ **Gratuit** pour les projets publics
- ✅ **Déploiement automatique** à chaque push
- ✅ **HTTPS automatique**
- ✅ **Monitoring intégré**

---

## 🐳 Option 2 : Docker

### Créer un Dockerfile :
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Déployer :
```bash
# Construire l'image
docker build -t pricing-calculator .

# Lancer le conteneur
docker run -p 8501:8501 pricing-calculator
```

---

## ☁️ Option 3 : Cloud Platforms

### Heroku :
1. **Créer `Procfile` :**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Créer `setup.sh` :**
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. **Déployer :**
```bash
heroku create pricing-calculator-app
git push heroku main
```

### Google Cloud Run :
```bash
# Déployer sur Cloud Run
gcloud run deploy pricing-calculator \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

---

## 🏠 Option 4 : Serveur VPS

### Installation sur Ubuntu/Debian :
```bash
# Installer Python et pip
sudo apt update
sudo apt install python3 python3-pip

# Cloner le projet
git clone https://github.com/votre-username/pricing-calculator.git
cd pricing-calculator

# Installer les dépendances
pip3 install -r requirements.txt

# Lancer avec systemd
sudo nano /etc/systemd/system/pricing-calculator.service
```

### Service systemd :
```ini
[Unit]
Description=Pricing Calculator Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pricing-calculator
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

### Activer le service :
```bash
sudo systemctl enable pricing-calculator
sudo systemctl start pricing-calculator
```

---

## 🔧 Configuration pour la production

### Variables d'environnement :
```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
```

### Configuration Streamlit :
```toml
# .streamlit/config.toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

---

## 📊 Monitoring et Logs

### Streamlit Cloud :
- Logs automatiques dans l'interface
- Métriques de performance
- Alertes en cas d'erreur

### Serveur VPS :
```bash
# Voir les logs
sudo journalctl -u pricing-calculator -f

# Monitoring avec htop
htop

# Logs d'application
tail -f /var/log/streamlit.log
```

---

## 🔒 Sécurité

### Recommandations :
- ✅ **HTTPS obligatoire** en production
- ✅ **Authentification** si nécessaire
- ✅ **Rate limiting** pour éviter les abus
- ✅ **Backup régulier** des données
- ✅ **Monitoring** des performances

### Nginx (reverse proxy) :
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🎯 Recommandation Finale

**Pour un déploiement rapide et gratuit :**
1. **Streamlit Cloud** pour le prototype
2. **Docker + VPS** pour la production
3. **Google Cloud Run** pour l'évolutivité

**Pour la production :**
- Utiliser un VPS avec Docker
- Configurer Nginx comme reverse proxy
- Mettre en place HTTPS avec Let's Encrypt
- Monitorer avec des outils comme Prometheus/Grafana 