#!/bin/bash

# 🚀 Script de déploiement - Calculateur de Couverture de Prix

echo "🚀 Déploiement du calculateur de couverture de prix..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Construire l'image Docker
echo "📦 Construction de l'image Docker..."
docker build -t pricing-calculator .

# Arrêter le conteneur existant s'il existe
echo "🛑 Arrêt du conteneur existant..."
docker stop pricing-calculator 2>/dev/null || true
docker rm pricing-calculator 2>/dev/null || true

# Lancer le nouveau conteneur
echo "🚀 Lancement du nouveau conteneur..."
docker run -d \
    --name pricing-calculator \
    -p 8501:8501 \
    --restart unless-stopped \
    pricing-calculator

# Vérifier que l'application démarre
echo "⏳ Attente du démarrage de l'application..."
sleep 10

# Vérifier le statut
if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
    echo "✅ Application déployée avec succès !"
    echo "🌐 Accessible sur : http://localhost:8501"
    echo "📊 Health check : http://localhost:8501/_stcore/health"
else
    echo "❌ Erreur lors du déploiement"
    echo "📋 Logs du conteneur :"
    docker logs pricing-calculator
    exit 1
fi

echo ""
echo "📋 Commandes utiles :"
echo "  - Voir les logs : docker logs -f pricing-calculator"
echo "  - Arrêter : docker stop pricing-calculator"
echo "  - Redémarrer : docker restart pricing-calculator"
echo "  - Supprimer : docker rm -f pricing-calculator" 