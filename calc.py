def calculate_implied_probability(odds):
    print("**********************"*20)
    lhs, rhs = odds
    print(lhs, rhs)
    print("**********************"*20)
    implied_prob_lhs = 1 / lhs
    implied_prob_rhs = 1 / rhs
    total_implied_prob = implied_prob_lhs + implied_prob_rhs

    return {
        'Odds 1': round(lhs, 2),
        'Odds 2': round(rhs, 2),
        'Implied Probability for Odds 1 (%)': round(implied_prob_lhs * 100, 2),
        'Implied Probability for Odds 2 (%)': round(implied_prob_rhs * 100, 2),
        'Total Implied Probability (%)': round(total_implied_prob * 100, 2),
        'Arbitrage Opportunity': total_implied_prob < 1
    }

def calculate_bet_amounts(total_stake, odds1, odds2):
    stake_lhs = (1 / odds1) / ((1 / odds1) + (1 / odds2)) * total_stake
    stake_rhs = (1 / odds2) / ((1 / odds1) + (1 / odds2)) * total_stake
    return round(stake_lhs, 2), round(stake_rhs, 2)

if __name__ == '__main__':
    print(calculate_implied_probability(odds=[1.80, 2.05]))
    pass
