#!/usr/bin/env python3
"""
Script de démonstration du calculateur de couverture de prix
"""

import sys
import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from black_scholes_calculator import BlackScholesCalculator

def demo_basic_calculation():
    """Démonstration d'un calcul de base"""
    
    print("🎯 DÉMONSTRATION : Calcul de couverture de prix")
    print("=" * 60)
    
    calculator = BlackScholesCalculator()
    
    # Scénario : Contrat de livraison de pétrole
    current_price = 80.0  # Prix actuel du baril
    delivery_date = datetime.now() + timedelta(days=180)  # 6 mois
    volatility = 0.35  # 35% de volatilité (typique pour le pétrole)
    coverage_percentile = 90.0  # 90% de couverture
    risk_free_rate = 0.03  # 3%
    
    print("📊 Scénario : Contrat de livraison de pétrole")
    print(f"   - Prix actuel du baril : {current_price} €")
    print(f"   - Date de livraison : {delivery_date.strftime('%d/%m/%Y')}")
    print(f"   - Volatilité : {volatility*100}%")
    print(f"   - Niveau de couverture : {coverage_percentile}%")
    print()
    
    results = calculator.calculate_price_hedge(
        current_price=current_price,
        delivery_date=delivery_date,
        volatility=volatility,
        coverage_percentile=coverage_percentile,
        risk_free_rate=risk_free_rate
    )
    
    print("📈 Résultats :")
    print(f"   - Prix de livraison calculé : {results['strike_price']:.2f} €")
    print(f"   - Delta prix : {results['price_delta']:.2f} €")
    print(f"   - Variation en % : {(results['price_delta']/current_price*100):.1f}%")
    print(f"   - Prix option call : {results['call_price']:.4f} €")
    print(f"   - Prix option put : {results['put_price']:.4f} €")
    print()
    
    if results['price_delta'] > 0:
        print("💡 Recommandation : Couverture haussière")
        print("   Achetez des options call pour vous protéger contre la hausse")
    else:
        print("💡 Recommandation : Couverture baissière")
        print("   Achetez des options put pour vous protéger contre la baisse")
    
    print()

def demo_sensitivity_analysis():
    """Analyse de sensibilité"""
    
    print("🔍 ANALYSE DE SENSIBILITÉ")
    print("=" * 40)
    
    calculator = BlackScholesCalculator()
    
    # Paramètres de base
    current_price = 100.0
    delivery_date = datetime.now() + timedelta(days=90)
    base_volatility = 0.20
    base_coverage = 95.0
    risk_free_rate = 0.02
    
    # Test de différentes volatilités
    volatilities = [0.10, 0.20, 0.30, 0.40, 0.50]
    print("📊 Impact de la volatilité sur le prix de livraison :")
    print("   Volatilité | Prix livraison | Delta prix")
    print("   " + "-" * 40)
    
    for vol in volatilities:
        results = calculator.calculate_price_hedge(
            current_price=current_price,
            delivery_date=delivery_date,
            volatility=vol,
            coverage_percentile=base_coverage,
            risk_free_rate=risk_free_rate
        )
        print(f"   {vol*100:6.0f}%    | {results['strike_price']:12.2f} € | {results['price_delta']:8.2f} €")
    
    print()
    
    # Test de différents centiles de couverture
    coverages = [80.0, 85.0, 90.0, 95.0, 99.0]
    print("📊 Impact du niveau de couverture :")
    print("   Couverture | Prix livraison | Delta prix")
    print("   " + "-" * 40)
    
    for coverage in coverages:
        results = calculator.calculate_price_hedge(
            current_price=current_price,
            delivery_date=delivery_date,
            volatility=base_volatility,
            coverage_percentile=coverage,
            risk_free_rate=risk_free_rate
        )
        print(f"   {coverage:8.0f}%  | {results['strike_price']:12.2f} € | {results['price_delta']:8.2f} €")
    
    print()

def demo_scenario_comparison():
    """Comparaison de différents scénarios"""
    
    print("🔄 COMPARAISON DE SCÉNARIOS")
    print("=" * 40)
    
    calculator = BlackScholesCalculator()
    
    scenarios = [
        {
            "name": "Pétrole (haute volatilité)",
            "current_price": 80.0,
            "volatility": 0.35,
            "delivery_days": 180
        },
        {
            "name": "Or (volatilité moyenne)",
            "current_price": 2000.0,
            "volatility": 0.20,
            "delivery_days": 90
        },
        {
            "name": "Blé (volatilité saisonnière)",
            "current_price": 300.0,
            "volatility": 0.25,
            "delivery_days": 120
        }
    ]
    
    print("📊 Comparaison de différents sous-jacents :")
    print("   Sous-jacent | Prix actuel | Volatilité | Prix livraison | Delta")
    print("   " + "-" * 70)
    
    for scenario in scenarios:
        delivery_date = datetime.now() + timedelta(days=scenario["delivery_days"])
        
        results = calculator.calculate_price_hedge(
            current_price=scenario["current_price"],
            delivery_date=delivery_date,
            volatility=scenario["volatility"],
            coverage_percentile=95.0,
            risk_free_rate=0.02
        )
        
        print(f"   {scenario['name']:15} | {scenario['current_price']:10.0f} € | {scenario['volatility']*100:9.0f}% | {results['strike_price']:13.0f} € | {results['price_delta']:5.0f} €")
    
    print()

def demo_risk_management():
    """Démonstration de gestion des risques"""
    
    print("⚠️  GESTION DES RISQUES")
    print("=" * 30)
    
    calculator = BlackScholesCalculator()
    
    # Scénario de risque
    current_price = 100.0
    delivery_date = datetime.now() + timedelta(days=60)
    volatility = 0.30
    risk_free_rate = 0.02
    
    print("📊 Analyse de risque pour différents niveaux de couverture :")
    print("   Niveau | Prix livraison | Probabilité | Coût option")
    print("   " + "-" * 50)
    
    coverage_levels = [80, 85, 90, 95, 99]
    
    for coverage in coverage_levels:
        results = calculator.calculate_price_hedge(
            current_price=current_price,
            delivery_date=delivery_date,
            volatility=volatility,
            coverage_percentile=coverage,
            risk_free_rate=risk_free_rate
        )
        
        # Calcul de la probabilité de dépassement
        probability = (100 - coverage) / 100
        
        print(f"   {coverage:6.0f}% | {results['strike_price']:13.1f} € | {probability*100:10.1f}% | {results['call_price']:10.4f} €")
    
    print()
    print("💡 Interprétation :")
    print("   - Plus le niveau de couverture est élevé, plus le prix de livraison est élevé")
    print("   - Le coût de l'option augmente avec le niveau de protection")
    print("   - Il faut trouver le bon équilibre entre protection et coût")

def main():
    """Fonction principale de démonstration"""
    
    print("🚀 DÉMONSTRATION DU CALCULATEUR DE COUVERTURE DE PRIX")
    print("=" * 70)
    print()
    
    try:
        # Démonstrations
        demo_basic_calculation()
        demo_sensitivity_analysis()
        demo_scenario_comparison()
        demo_risk_management()
        
        print("✅ Démonstration terminée avec succès !")
        print("📱 Lancez 'streamlit run app.py' pour utiliser l'interface graphique")
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 