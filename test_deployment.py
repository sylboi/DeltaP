#!/usr/bin/env python3
"""
Script de test pour vérifier que l'application est prête pour le déploiement
"""

import sys
import importlib

def test_imports():
    """Teste l'import de tous les modules nécessaires"""
    print("🔍 Test des imports...")
    
    modules_to_test = [
        'streamlit',
        'numpy',
        'scipy',
        'pandas',
        'plotly',
        'matplotlib'
    ]
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - ERREUR: {e}")
            return False
    
    return True

def test_calculator():
    """Teste le module de calcul Black & Scholes"""
    print("\n🧮 Test du calculateur Black & Scholes...")
    
    try:
        from black_scholes_calculator import BlackScholesCalculator
        calculator = BlackScholesCalculator()
        print("✅ BlackScholesCalculator - OK")
        
        # Test d'un calcul simple
        call_price = calculator.black_scholes_call(100, 100, 1, 0.02, 0.2)
        put_price = calculator.black_scholes_put(100, 100, 1, 0.02, 0.2)
        
        print(f"✅ Calculs de test - Call: {call_price:.4f}, Put: {put_price:.4f}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans BlackScholesCalculator: {e}")
        return False

def test_streamlit_config():
    """Teste la configuration Streamlit"""
    print("\n⚙️ Test de la configuration Streamlit...")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit version: {st.__version__}")
        
        # Test de la configuration
        import os
        config_path = ".streamlit/config.toml"
        if os.path.exists(config_path):
            print("✅ Fichier config.toml trouvé")
        else:
            print("❌ Fichier config.toml manquant")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans la configuration Streamlit: {e}")
        return False

def test_requirements():
    """Teste le fichier requirements.txt"""
    print("\n📦 Test du fichier requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        if 'streamlit' in requirements:
            print("✅ requirements.txt contient streamlit")
        else:
            print("❌ requirements.txt ne contient pas streamlit")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur avec requirements.txt: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de préparation au déploiement Streamlit Cloud")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_calculator,
        test_streamlit_config,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test échoué: {test.__name__}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'application est prête pour le déploiement.")
        print("\n📋 Prochaines étapes:")
        print("1. git add .")
        print("2. git commit -m 'Préparation pour déploiement Streamlit Cloud'")
        print("3. git push origin main")
        print("4. Aller sur share.streamlit.io")
        print("5. Créer une nouvelle application")
        print("6. Configurer avec votre repository")
        print("7. Déployer !")
        return 0
    else:
        print("❌ Certains tests ont échoué. Veuillez corriger les problèmes avant le déploiement.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 