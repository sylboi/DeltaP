import numpy as np
import scipy.stats as stats
from datetime import datetime, timedelta
import math

class BlackScholesCalculator:
    """
    Calculateur de couverture de prix basé sur le modèle Black & Scholes
    """
    
    def __init__(self):
        pass
    
    def black_scholes_call(self, S, K, T, r, sigma):
        """
        Calcul du prix d'une option call selon Black & Scholes
        
        Args:
            S: Prix actuel du sous-jacent
            K: Prix d'exercice (strike)
            T: Temps jusqu'à l'échéance (en années)
            r: Taux d'intérêt sans risque
            sigma: Volatilité
        """
        if T <= 0:
            return max(S - K, 0)
        
        if sigma <= 0:
            # Si volatilité nulle, le prix est simplement la valeur intrinsèque
            return max(S - K * np.exp(-r * T), 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        call_price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
        return call_price
    
    def black_scholes_put(self, S, K, T, r, sigma):
        """
        Calcul du prix d'une option put selon Black & Scholes
        """
        if T <= 0:
            return max(K - S, 0)
        
        if sigma <= 0:
            # Si volatilité nulle, le prix est simplement la valeur intrinsèque
            return max(K * np.exp(-r * T) - S, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        put_price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
        return put_price
    
    def calculate_delta_call(self, S, K, T, r, sigma):
        """
        Calcul du delta d'une option call
        """
        if T <= 0:
            return 1.0 if S > K else 0.0
        
        if sigma <= 0:
            # Si volatilité nulle, le delta est binaire
            return 1.0 if S > K * np.exp(-r * T) else 0.0
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return stats.norm.cdf(d1)
    
    def calculate_delta_put(self, S, K, T, r, sigma):
        """
        Calcul du delta d'une option put
        """
        if T <= 0:
            return -1.0 if S < K else 0.0
        
        if sigma <= 0:
            # Si volatilité nulle, le delta est binaire
            return -1.0 if S < K * np.exp(-r * T) else 0.0
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return stats.norm.cdf(d1) - 1
    
    def calculate_price_hedge(self, current_price, start_date, end_date, volatility, 
                            coverage_percentile, risk_free_rate=0.0):
        """
        Calcul de la couverture de prix basée sur Black & Scholes
        
        Args:
            current_price: Prix actuel du sous-jacent
            start_date: Date de début du contrat (datetime)
            end_date: Date de fin du contrat (datetime)
            volatility: Volatilité annuelle
            coverage_percentile: Centile de couverture (0-100)
            risk_free_rate: Taux d'intérêt sans risque (défaut: 0%)
        
        Returns:
            dict: Résultats du calcul de couverture
        """
        today = datetime.now()
        
        # Calcul de la holding period (période de détention)
        if isinstance(start_date, datetime):
            start_datetime = start_date
        else:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            
        if isinstance(end_date, datetime):
            end_datetime = end_date
        else:
            end_datetime = datetime.combine(end_date, datetime.min.time())
        
        # Calcul du temps jusqu'à la fin du contrat
        time_to_delivery = (end_datetime - today).days / 365.0
        
        # Calcul du milieu de la période de livraison
        delivery_midpoint = start_datetime + (end_datetime - start_datetime) / 2
        
        # Calcul de la holding period (entre aujourd'hui et le milieu de la livraison)
        holding_period = (delivery_midpoint - today).days / 365.0
        
        if time_to_delivery <= 0:
            return {
                'error': 'La date de fin du contrat doit être dans le futur',
                'current_price': current_price,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'time_to_delivery': 0
            }
        
        # Calcul du prix d'exercice basé sur le centile de couverture
        # Utilisation de la holding period (jusqu'au milieu de la livraison)
        z_score = stats.norm.ppf(coverage_percentile / 100.0)
        strike_price = current_price * np.exp(
            (risk_free_rate - 0.5 * volatility**2) * holding_period + 
            z_score * volatility * np.sqrt(holding_period)
        )
        
        # Calcul des prix d'options (utilisant la holding period)
        call_price = self.black_scholes_call(current_price, strike_price, holding_period, 
                                           risk_free_rate, volatility)
        put_price = self.black_scholes_put(current_price, strike_price, holding_period, 
                                         risk_free_rate, volatility)
        
        # Calcul des deltas
        call_delta = self.calculate_delta_call(current_price, strike_price, holding_period, 
                                             risk_free_rate, volatility)
        put_delta = self.calculate_delta_put(current_price, strike_price, holding_period, 
                                           risk_free_rate, volatility)
        
        # Calcul du delta prix (différence entre le prix de livraison et le prix actuel)
        price_delta = strike_price - current_price
        
        return {
            'current_price': current_price,
            'start_date': start_datetime,
            'end_date': end_datetime,
            'time_to_delivery': time_to_delivery,
            'holding_period': holding_period,
            'volatility': volatility,
            'coverage_percentile': coverage_percentile,
            'strike_price': strike_price,
            'price_delta': price_delta,
            'call_price': call_price,
            'put_price': put_price,
            'call_delta': call_delta,
            'put_delta': put_delta,
            'risk_free_rate': risk_free_rate
        }
    
    def calculate_price_scenarios(self, current_price, start_date, end_date, volatility, 
                                risk_free_rate=0.0, num_scenarios=10000):
        """
        Calcul de différents scénarios de prix pour analyse de sensibilité
        """
        today = datetime.now()
        
        # Gestion des types de date
        if isinstance(start_date, datetime):
            start_datetime = start_date
        else:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            
        if isinstance(end_date, datetime):
            end_datetime = end_date
        else:
            end_datetime = datetime.combine(end_date, datetime.min.time())
        
        time_to_delivery = (end_datetime - today).days / 365.0
        
        if time_to_delivery <= 0:
            return []
        
        # Génération de scénarios de prix avec plus de dispersion
        np.random.seed(42)  # Pour la reproductibilité
        
        # Utilisation de la holding period pour les scénarios
        holding_period = (end_datetime - start_datetime).days / 365.0 / 2  # Milieu de la période
        
        # Génération de chocs plus dispersés (distribution t de Student pour plus de queues épaisses)
        degrees_of_freedom = 3  # Pour des queues plus épaisses
        random_shocks = np.random.standard_t(degrees_of_freedom, num_scenarios)
        
        # Ajout de quelques scénarios extrêmes
        extreme_shocks = np.random.normal(0, 2, num_scenarios // 10)  # 10% de scénarios extrêmes
        random_shocks = np.concatenate([random_shocks, extreme_shocks])
        
        scenarios = []
        for shock in random_shocks:
            future_price = current_price * np.exp(
                (risk_free_rate - 0.5 * volatility**2) * holding_period + 
                shock * volatility * np.sqrt(holding_period)
            )
            price_delta = future_price - current_price
            scenarios.append({
                'future_price': future_price,
                'price_delta': price_delta,
                'shock': shock
            })
        
        return scenarios 