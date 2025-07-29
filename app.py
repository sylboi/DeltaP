import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from black_scholes_calculator import BlackScholesCalculator

# Configuration de la page
st.set_page_config(
    page_title="Calculateur de Couverture de Prix - Black & Scholes",
    page_icon="📊",
    layout="wide"
)

# Titre et description
st.title("📊 Calculateur de Couverture de Prix")
st.markdown("""
Cet outil calcule le delta prix entre aujourd'hui et la date de livraison d'un contrat 
en utilisant le modèle Black & Scholes pour déterminer la couverture de prix optimale.
""")

# Initialisation du calculateur
calculator = BlackScholesCalculator()

# Sidebar pour les paramètres
st.sidebar.header("⚙️ Paramètres d'entrée")

# Prix actuel du sous-jacent
current_price = st.sidebar.number_input(
    "Prix actuel du sous-jacent (€)",
    min_value=0.01,
    max_value=10000.0,
    value=100.0,
    step=0.01,
    help="Prix actuel de l'actif sous-jacent"
)

# Calcul des dates par défaut (année N+1)
current_year = datetime.now().year
next_year = current_year + 1
default_start_date = datetime(next_year, 1, 1).date()
default_end_date = datetime(next_year, 12, 31).date()

# Date de début du contrat
start_date = st.sidebar.date_input(
    "Date de début du contrat",
    value=default_start_date,
    min_value=datetime.now().date(),
    help="Date de début du contrat (incluse)"
)

# Date de fin du contrat
end_date = st.sidebar.date_input(
    "Date de fin du contrat",
    value=default_end_date,
    min_value=start_date,
    help="Date de fin du contrat (incluse)"
)

# Volatilité
volatility = st.sidebar.slider(
    "Volatilité annuelle (%)",
    min_value=1.0,
    max_value=100.0,
    value=25.0,
    step=1.0,
    help="Volatilité annuelle de l'actif sous-jacent"
) / 100.0

# Centile de couverture
coverage_percentile = st.sidebar.slider(
    "Centile de couverture (%)",
    min_value=1.0,
    max_value=99.0,
    value=75.0,
    step=1.0,
    help="Niveau de confiance pour la couverture de prix"
)

# Taux d'intérêt sans risque
risk_free_rate = st.sidebar.slider(
    "Taux d'intérêt sans risque (%)",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.1,
    help="Taux d'intérêt sans risque annuel"
) / 100.0

# Nombre de simulations
num_simulations = st.sidebar.selectbox(
    "Nombre de simulations",
    options=[1000, 5000, 10000, 20000, 50000],
    index=2,  # 10000 par défaut
    help="Nombre de scénarios à simuler"
)

# Bouton de calcul
if st.sidebar.button("🚀 Calculer la couverture", type="primary"):
    # Calcul de la couverture
    results = calculator.calculate_price_hedge(
        current_price=current_price,
        start_date=start_date,
        end_date=end_date,
        volatility=volatility,
        coverage_percentile=coverage_percentile,
        risk_free_rate=risk_free_rate
    )
    
    if 'error' in results:
        st.error(results['error'])
    else:
        # Affichage des résultats principaux
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Prix actuel",
                f"€{results['current_price']:.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Prix de livraison (strike)",
                f"€{results['strike_price']:.2f}",
                delta=f"{results['price_delta']:.2f}"
            )
        
        with col3:
            st.metric(
                "Delta prix",
                f"€{results['price_delta']:.2f}",
                delta=f"{(results['price_delta']/results['current_price']*100):.1f}%"
            )
        
        with col4:
            st.metric(
                "Milieu livraison",
                f"{results['holding_period']*365:.0f} jours",
                delta=None
            )
        
        # Détails des options
        st.subheader("📈 Détails des options de couverture")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Option Call (Achat)**")
            st.metric("Prix de l'option", f"€{results['call_price']:.4f}")
            st.metric("Delta", f"{results['call_delta']:.4f}")
        
        with col2:
            st.markdown("**Option Put (Vente)**")
            st.metric("Prix de l'option", f"€{results['put_price']:.4f}")
            st.metric("Delta", f"{results['put_delta']:.4f}")
        
        # Graphique de l'évolution du prix
        st.subheader("📊 Analyse des scénarios de prix")
        
        # Calcul des scénarios
        scenarios = calculator.calculate_price_scenarios(
            current_price=current_price,
            start_date=start_date,
            end_date=end_date,
            volatility=volatility,
            risk_free_rate=risk_free_rate,
            num_scenarios=num_simulations
        )
        
        if scenarios:
            df_scenarios = pd.DataFrame(scenarios)
            
            # Calcul des percentiles pour le graphique
            percentile_95 = df_scenarios['future_price'].quantile(0.95)
            percentile_99 = df_scenarios['future_price'].quantile(0.99)
            
            # Limitation de l'affichage aux centiles 2% et 98%
            percentile_02 = df_scenarios['future_price'].quantile(0.02)
            percentile_98 = df_scenarios['future_price'].quantile(0.98)
            
            # Filtrage des données pour l'affichage
            df_filtered = df_scenarios[
                (df_scenarios['future_price'] >= percentile_02) & 
                (df_scenarios['future_price'] <= percentile_98)
            ]
            
            # Histogramme des prix futurs (limité aux centiles 2-98%)
            fig_hist = px.histogram(
                df_filtered, 
                x='future_price',
                nbins=50,
                title="Distribution des prix futurs (centiles 2%-98%)",
                labels={'future_price': 'Prix futur (€)', 'count': 'Fréquence'}
            )
            # Ajout des lignes verticales (seulement si elles sont dans la plage visible)
            if percentile_02 <= current_price <= percentile_98:
                fig_hist.add_vline(x=current_price, line_dash="dash", line_color="red", 
                                  annotation_text="Prix actuel")
            
            if percentile_02 <= results['strike_price'] <= percentile_98:
                fig_hist.add_vline(x=results['strike_price'], line_dash="dash", line_color="green", 
                                  annotation_text="Prix de livraison")
            
            if percentile_02 <= percentile_95 <= percentile_98:
                fig_hist.add_vline(x=percentile_95, line_dash="dash", line_color="orange", 
                                  annotation_text="95ème centile")
            
            if percentile_02 <= percentile_99 <= percentile_98:
                fig_hist.add_vline(x=percentile_99, line_dash="dash", line_color="purple", 
                                  annotation_text="99ème centile")
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Statistiques détaillées de dispersion
            st.subheader("📊 Analyse de dispersion")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Statistiques descriptives :**")
                st.write(f"- **Prix minimum :** €{df_scenarios['future_price'].min():.2f}")
                st.write(f"- **Prix maximum :** €{df_scenarios['future_price'].max():.2f}")
                st.write(f"- **Médiane :** €{df_scenarios['future_price'].median():.2f}")
                st.write(f"- **Coefficient de variation :** {(df_scenarios['future_price'].std()/df_scenarios['future_price'].mean()*100):.1f}%")
                st.write(f"- **Plage affichée :** €{percentile_02:.2f} - €{percentile_98:.2f}")
            
            with col2:
                st.markdown("**Centiles :**")
                st.write(f"- **10ème centile :** €{df_scenarios['future_price'].quantile(0.10):.2f}")
                st.write(f"- **25ème centile :** €{df_scenarios['future_price'].quantile(0.25):.2f}")
                st.write(f"- **75ème centile :** €{df_scenarios['future_price'].quantile(0.75):.2f}")
                st.write(f"- **90ème centile :** €{df_scenarios['future_price'].quantile(0.90):.2f}")
            
            # Statistiques des scénarios
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Prix moyen futur",
                    f"€{df_scenarios['future_price'].mean():.2f}"
                )
            
            with col2:
                st.metric(
                    "Écart-type des prix",
                    f"€{df_scenarios['future_price'].std():.2f}"
                )
            
            with col3:
                st.metric(
                    "95ème centile",
                    f"€{percentile_95:.2f}"
                )
            
            with col4:
                st.metric(
                    "99ème centile",
                    f"€{percentile_99:.2f}"
                )
            
            # Graphique de l'évolution temporelle
            st.subheader("⏰ Évolution temporelle du prix")
            
            # Simulation de l'évolution du prix dans le temps
            time_steps = np.linspace(0, results['time_to_delivery'], 100)
            expected_prices = current_price * np.exp((risk_free_rate - 0.5 * volatility**2) * time_steps)
            
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=time_steps * 365,
                y=expected_prices,
                mode='lines',
                name='Prix attendu',
                line=dict(color='blue', width=2)
            ))
            
            # Bandes de confiance
            upper_bound = expected_prices * np.exp(1.96 * volatility * np.sqrt(time_steps))
            lower_bound = expected_prices * np.exp(-1.96 * volatility * np.sqrt(time_steps))
            
            fig_time.add_trace(go.Scatter(
                x=time_steps * 365,
                y=upper_bound,
                mode='lines',
                name='Bande supérieure (95%)',
                line=dict(color='lightblue', width=1, dash='dash')
            ))
            
            fig_time.add_trace(go.Scatter(
                x=time_steps * 365,
                y=lower_bound,
                mode='lines',
                name='Bande inférieure (95%)',
                line=dict(color='lightblue', width=1, dash='dash'),
                fill='tonexty'
            ))
            
            fig_time.add_hline(y=results['strike_price'], line_dash="dash", line_color="green",
                              annotation_text="Prix de livraison")
            
            fig_time.update_layout(
                title="Évolution du prix dans le temps",
                xaxis_title="Jours jusqu'à la livraison",
                yaxis_title="Prix (€)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_time, use_container_width=True)
        
        # Recommandations pour couverture d'exposition volume
        st.subheader("💡 Recommandations de couverture (Exposition volume)")
        
        # Sélection du type d'exposition volume
        volume_exposure = st.selectbox(
            "Type d'exposition volume",
            options=["Surconsommation client (fournisseur vend)", 
                    "Sous-consommation client (fournisseur achète)",
                    "Rachat de production (fournisseur achète)",
                    "Exposition mixte (tous cas possibles)"],
            index=3,
            help="Détermine l'exposition volume du fournisseur"
        )
        
        if volume_exposure == "Surconsommation client (fournisseur vend)":
            # Client surconsomme → fournisseur doit acheter plus d'énergie au marché
            st.warning(f"""
            **⚠️ Exposition haussière pour le fournisseur**
            
            **Situation :** Client surconsomme → Fournisseur doit acheter davantage d'énergie au marché 
            pour satisfaire le client à son prix contractuel
            
            **Risque :** Si le prix monte au-dessus du prix de hedging (€{results['strike_price']:.2f}), 
            le fournisseur doit acheter plus cher au marché pour honorer son contrat.
            
            **Recommandation :** Acheter des options call pour couvrir le risque de hausse des prix d'achat au marché.
            """)
        elif volume_exposure == "Sous-consommation client (fournisseur achète)":
            # Client sous-consomme → fournisseur doit revendre l'excédent au marché
            st.warning(f"""
            **⚠️ Exposition baissière pour le fournisseur**
            
            **Situation :** Client sous-consomme → Fournisseur doit revendre l'excédent d'énergie au marché
            
            **Risque :** Si le prix baisse en-dessous du prix de hedging (€{results['strike_price']:.2f}), 
            le fournisseur doit vendre moins cher au marché.
            
            **Recommandation :** Acheter des options put pour couvrir le risque de baisse des prix de vente au marché.
            """)
        elif volume_exposure == "Rachat de production (fournisseur achète)":
            # Rachat de production → fournisseur doit revendre l'excédent au marché
            st.warning(f"""
            **⚠️ Exposition baissière pour le fournisseur**
            
            **Situation :** Rachat de production → Fournisseur doit revendre l'excédent d'énergie au marché
            
            **Risque :** Si le prix baisse en-dessous du prix de hedging (€{results['strike_price']:.2f}), 
            le fournisseur doit vendre moins cher au marché.
            
            **Recommandation :** Acheter des options put pour couvrir le risque de baisse des prix de vente au marché.
            """)
        else:
            # Exposition mixte - le fournisseur ne sait pas à l'avance
            st.info(f"""
            **🔄 Exposition mixte - Couverture bilatérale recommandée**
            
            Le fournisseur ne sait pas à l'avance le sens de déviation du client.
            
            **Stratégie recommandée :**
            - **Options Call** : Protection contre hausse des prix (surconsommation)
            - **Options Put** : Protection contre baisse des prix (sous-consommation/rachat)
            
            **Prix de hedging :** €{results['strike_price']:.2f} (vs €{current_price:.2f} actuel)
            """)
        
        # Explication de l'exposition volume
        with st.expander("📚 Explication de l'exposition volume"):
            st.markdown("""
            ### 🔄 Exposition volume du fournisseur
            
            **Surconsommation client :**
            - Le client consomme plus que prévu
            - Le fournisseur **doit acheter davantage d'énergie au marché** pour satisfaire le client
            - **Exposition haussière** : Si prix monte → fournisseur doit acheter plus cher au marché
            
            **Sous-consommation client :**
            - Le client consomme moins que prévu
            - Le fournisseur **doit revendre l'excédent d'énergie au marché**
            - **Exposition baissière** : Si prix baisse → fournisseur doit vendre moins cher au marché
            
            **Rachat de production :**
            - Le client produit plus que prévu
            - Le fournisseur **doit revendre l'excédent d'énergie au marché**
            - **Exposition baissière** : Si prix baisse → fournisseur doit vendre moins cher au marché
            
            ### 🎯 Stratégies de couverture
            - **Options Call** : Protection contre hausse des prix (surconsommation)
            - **Options Put** : Protection contre baisse des prix (sous-consommation/rachat)
            """)
        
        # Paramètres utilisés
        with st.expander("📋 Paramètres utilisés"):
            st.write(f"""
            - **Prix actuel du sous-jacent :** €{current_price:.2f}
            - **Date de début :** {start_date.strftime('%d/%m/%Y')}
            - **Date de fin :** {end_date.strftime('%d/%m/%Y')}
            - **Volatilité annuelle :** {volatility*100:.1f}%
            - **Centile de couverture :** {coverage_percentile:.1f}%
            - **Taux d'intérêt sans risque :** {risk_free_rate*100:.1f}%
            - **Milieu de livraison :** {results['holding_period']*365:.0f} jours
            - **Temps jusqu'à fin :** {results['time_to_delivery']*365:.0f} jours
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Calculateur de couverture de prix basé sur le modèle Black & Scholes</p>
    <p>Développé pour l'analyse de risque et la gestion de portefeuille</p>
</div>
""", unsafe_allow_html=True) 