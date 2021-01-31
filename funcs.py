import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from math import sqrt
from scipy.stats import norm

def simulation(avg_return=0.05, std=0.15, start_amount=10000, monthly_invest=1000, n_years=15, n_simulations=1000):

    invested_vals, portfolio_vals = [], []

    avg_monthly_return = avg_return / 12
    monthly_std = std / sqrt(12)

    transact_costs = 0

    for i in range(0, n_simulations):
        investments_mom = np.repeat(monthly_invest, n_years*12-1)
        investments_mom = np.insert(investments_mom, 0, start_amount, axis=0)

        final_amount_invested = (investments_mom - transact_costs).cumsum()[-1]

        returns_mom = np.random.normal(avg_monthly_return, monthly_std, n_years*12)

        total_return_factor = (1+returns_mom).cumprod()[-1]

        final_portfolio_value = final_amount_invested * total_return_factor

        invested_vals.append(final_amount_invested)
        portfolio_vals.append(final_portfolio_value)

    avg_portfolio_val = np.array(portfolio_vals).mean()
    std_portfolio_val = np.array(portfolio_vals).std()

    profits = np.array(portfolio_vals) - np.array(invested_vals)
    avg_profit = profits.mean()
    std_profit = profits.std()

    n_pos_simulations = (np.array(profits) >= 0).sum()
    pos_proba = n_pos_simulations / n_simulations

    return dict(
        final_amount_invested=final_amount_invested,
        profits=profits, 
        avg_profit=avg_profit, 
        std_profit=std_profit, 
        avg_portfolio_val=avg_portfolio_val,
        std_portfolio_val=std_portfolio_val,
        pos_proba=pos_proba
        )

