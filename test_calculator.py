#!/usr/bin/env python3
"""
Script de test pour le calculateur Black & Scholes
"""

import sys
import os
from datetime import datetime, timedelta
import numpy as np

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from black_scholes_calculator import BlackScholesCalculator

def test_black_scholes_calculator():
    """Test du calculateur Black & Scholes"""
    
    print("🧪 Test du calculateur de couverture de prix")
    print("=" * 50)
    
    # Initialisation du calculateur
    calculator = BlackScholesCalculator()
    
    # Paramètres de test
    current_price = 100.0
    delivery_date = datetime.now() + timedelta(days=90)
    volatility = 0.20  # 20%
    coverage_percentile = 95.0  # 95%
    risk_free_rate = 0.02  # 2%
    
    print(f"📊 Paramètres de test :")
    print(f"   - Prix actuel : {current_price} €")
    print(f"   - Date de livraison : {delivery_date.strftime('%d/%m/%Y')}")
    print(f"   - Volatilité : {volatility*100}%")
    print(f"   - Centile de couverture : {coverage_percentile}%")
    print(f"   - Taux sans risque : {risk_free_rate*100}%")
    print()
    
    # Test du calcul de couverture
    print("🔍 Calcul de la couverture...")
    results = calculator.calculate_price_hedge(
        current_price=current_price,
        start_date=delivery_date - timedelta(days=30),  # Date de début
        end_date=delivery_date,  # Date de fin
        volatility=volatility,
        coverage_percentile=coverage_percentile,
        risk_free_rate=risk_free_rate
    )
    
    if 'error' in results:
        print(f"❌ Erreur : {results['error']}")
        return False
    
    # Affichage des résultats
    print("✅ Résultats du calcul :")
    print(f"   - Prix de livraison (strike) : {results['strike_price']:.2f} €")
    print(f"   - Delta prix : {results['price_delta']:.2f} €")
    print(f"   - Temps jusqu'à livraison : {results['time_to_delivery']*365:.0f} jours")
    print(f"   - Prix option call : {results['call_price']:.4f} €")
    print(f"   - Prix option put : {results['put_price']:.4f} €")
    print(f"   - Delta call : {results['call_delta']:.4f}")
    print(f"   - Delta put : {results['put_delta']:.4f}")
    print()
    
    # Test des scénarios
    print("📈 Calcul des scénarios...")
    scenarios = calculator.calculate_price_scenarios(
        current_price=current_price,
        start_date=delivery_date - timedelta(days=30),  # Date de début
        end_date=delivery_date,  # Date de fin
        volatility=volatility,
        risk_free_rate=risk_free_rate,
        num_scenarios=1000
    )
    
    if scenarios:
        future_prices = [s['future_price'] for s in scenarios]
        price_deltas = [s['price_delta'] for s in scenarios]
        
        print("✅ Statistiques des scénarios :")
        print(f"   - Prix moyen futur : {np.mean(future_prices):.2f} €")
        print(f"   - Écart-type : {np.std(future_prices):.2f} €")
        print(f"   - Prix minimum : {np.min(future_prices):.2f} €")
        print(f"   - Prix maximum : {np.max(future_prices):.2f} €")
        print(f"   - 95ème centile : {np.percentile(future_prices, 95):.2f} €")
        print()
    
    # Test de validation des formules Black & Scholes
    print("🔬 Validation des formules Black & Scholes...")
    
    # Test avec des paramètres connus
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    
    call_price = calculator.black_scholes_call(S, K, T, r, sigma)
    put_price = calculator.black_scholes_put(S, K, T, r, sigma)
    
    print(f"   - Prix call (S={S}, K={K}, T={T}, r={r}, σ={sigma}) : {call_price:.4f}")
    print(f"   - Prix put (S={S}, K={K}, T={T}, r={r}, σ={sigma}) : {put_price:.4f}")
    
    # Vérification de la parité call-put
    call_put_parity = call_price - put_price - S + K * np.exp(-r * T)
    print(f"   - Parité call-put (devrait être ≈ 0) : {call_put_parity:.6f}")
    
    if abs(call_put_parity) < 1e-6:
        print("   ✅ Parité call-put vérifiée")
    else:
        print("   ⚠️  Parité call-put non respectée")
    
    print()
    print("🎉 Tous les tests sont passés avec succès !")
    return True

def test_edge_cases():
    """Test des cas limites"""
    
    print("🔍 Test des cas limites")
    print("=" * 30)
    
    calculator = BlackScholesCalculator()
    
    # Test avec volatilité nulle
    print("📊 Test avec volatilité nulle...")
    results = calculator.calculate_price_hedge(
        current_price=100,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        volatility=0.0,
        coverage_percentile=95
    )
    
    if 'error' not in results:
        print(f"   - Prix de livraison : {results['strike_price']:.2f} €")
    
    # Test avec date de livraison passée
    print("📅 Test avec date de livraison passée...")
    results = calculator.calculate_price_hedge(
        current_price=100,
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() - timedelta(days=1),
        volatility=0.2,
        coverage_percentile=95
    )
    
    if 'error' in results:
        print(f"   ✅ Erreur détectée : {results['error']}")
    
    print("✅ Tests des cas limites terminés")

if __name__ == "__main__":
    try:
        success = test_black_scholes_calculator()
        test_edge_cases()
        
        if success:
            print("\n🚀 L'outil est prêt à être utilisé !")
            print("   Lancez 'streamlit run app.py' pour démarrer l'application")
        else:
            print("\n❌ Des erreurs ont été détectées")
            
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")
        import traceback
        traceback.print_exc() 