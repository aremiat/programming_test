import pandas as pd
import numpy as np 
import yfinance as yf

import matplotlib.pyplot as plt


# Logic

prices = pd.read_csv("https://raw.githubusercontent.com/aeqcap/programming_test/main/data/data.csv")
prices.rename(columns={'MSDEWIN Index': 'Close'}, inplace=True)

def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    seen = set() # crée un set vide pour stocker les items vus
    for item in lst: # itére dans la liste
        if item in seen: # si deja dans set alors false
            return False
        seen.add(item) # Sinon on ajoute a set 
    return True # si pas de doublon return true 
    
pass

test_list = [3, 1, 4, 3, 5, 6]
test_list = [3, 1, 4, 2, 5, 6]
result = check_uniqueness(test_list)
result

def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    if len(array) < 2: # check de la validité de array
        return 0
    
    array.sort() # tri
    
    min_diff = float('inf') # initialisation de notre variable
    
    for i in range(len(array) - 1): #logique : on itere dans array
        diff = abs(array[i] - array[i + 1]) # diff entre les nombres de array
        if diff < min_diff: # si la diff est plus petite que la premiere difference alors on enregistre cetet valeur en tant que plus petite
            min_diff = diff
    
    return min_diff
    
pass

test_array = [3, 10, 20, 30, 40, 50, 1]
result = smallest_difference(test_array)
result

# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file
    """
    sma_short = prices['Close'].rolling(window=window_short, min_periods=1).mean() # sma de 12j avec moyenne glissante(rolling window)
    sma_long = prices['Close'].rolling(window=window_long, min_periods=1).mean()# sma de 26 jours 
    
    # Calcul du MACD
    macd_values = sma_short - sma_long # diff des deux sma
    
    # Créer un DataFrame pour stocker les résultats
    macd_df = pd.DataFrame(macd_values)
    
    return macd_df
    
    
pass

# Verif

macd_result = macd(prices)
macd_result['date'] = prices['date']
merged_df = pd.merge(prices, macd_result, on='date')
merged_df.rename(columns={'Close_x': 'MSDEWIN Index', 'Close_y' : 'macd_12_26'}, inplace=True)
print(merged_df)


def sortino_ratio(prices): # sortino = (rendement moyen - Rf)/downside vol, ici r = 0 donc sortino = rendement moyen / downside vol
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
    # check le format des Close de prices 
    prices['Close'] = pd.to_numeric(prices['Close'], errors='coerce')

    # Calcul des rendements quotidiens pour la colonne 'Close'
    returns = prices['Close'].pct_change()
    # returns = np.log(prices['Close']).diff().dropna()

    # Calcul de la rentabilité moyenne des rendements positifs
    # mean_positive_returns = returns[returns > 0].mean()
    mean_positive_returns = returns.mean()
    
    
    # Calcul de la volatilité à la baisse (déviation standard des rendements négatifs)
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std(ddof=1)  # ddof=1 pour utiliser l'estimateur non biaisé
    
    # Calcul du ratio de Sortino: rentabilité moyenne divisée par la volatilité à la baisse
    sortino_ratio = mean_positive_returns / downside_std
    
    return sortino_ratio
    
    
pass

# Je retrouve pas 0.05457 mais 0.033656, erreur dans ma façon de calculer le sortino
sortino_results = sortino_ratio(prices)


def expected_shortfall(prices, level=0.95): # CVAR
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """
    # Calcul des rendements quotidiens
    # returns = prices['Close'].pct_change().dropna() ce que j'avais fait au début je trouve -0.03468
    returns = np.log(prices['Close']).diff().dropna() # en calculant avec np.log je me rappoche -0.025217 
    
    # Calcul de la Value at Risk (VaR) à 5%
    var_level = np.percentile(returns, (1 - level) * 100)
    
    # Calcul de l'Expected Shortfall (ES)
    es = returns[returns < var_level].mean()
    
    return es

pass

es_result = expected_shortfall(prices)
print(es_result)
# -0.02484449312964705 et je trouve -0.0252176


# Plot


def visualize(prices, path):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    
    """
    # format datetime
    prices['date'] = pd.to_datetime(prices['date'])

    # Tracer les prix de clôture

    plt.figure(figsize=(14, 7))

    plt.plot(prices['date'], prices['Close'], label='Close Price')

    plt.title('Price Chart') # titre

    plt.xlabel('Date') # légende axe x

    plt.ylabel('Price') # légende axe y

    plt.legend()

    plt.grid(True)


    # Sauvegarder la figure

    plt.savefig(path)

    plt.close() 
    
    pass

visualize(prices, r'C:\Users\admin\Desktop\Kanopy\graphique.png')