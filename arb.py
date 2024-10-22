import calc

def single_group_find_best_arbitrage_opportunity(group):
    best_opportunity = None

    for j in group:
        odd_1 = j['odds_1']
        outcome_1 = j['outcome_1']
        site_1 = j['site']
        for i in group:
            if j == i:
                continue  # Skip comparing the same entry
            
            odds_2 = i['odds_2']
            site_2 = i['site']
            outcome_2 = i['outcome_2']
            
            if site_1 == site_2:
                continue

            prob = calc.calculate_implied_probability([odd_1, odds_2])
            
            if prob['Arbitrage Opportunity']:
                if best_opportunity is None or prob['Total Implied Probability (%)'] < best_opportunity['Total Implied Probability (%)']:
                    best_opportunity = {
                        'Outcome 1': outcome_1,
                        'Odds 1': round(odd_1, 2),
                        'Site 1': site_1,
                        'Outcome 2': outcome_2,
                        'Odds 2': round(odds_2, 2),
                        'Site 2': site_2,
                        'Total Implied Probability (%)': round(prob['Total Implied Probability (%)'], 2),
                        'Arbitrage Opportunity': prob['Arbitrage Opportunity']
                    }

    return best_opportunity

def get_lowest_implied_probability(groups):
    results = []
    for group in groups:
        try:
            result = single_group_find_best_arbitrage_opportunity(group)
            if result['Arbitrage Opportunity']:
                results.append(result)
                # print("group:", group)
        except:
            continue

    lowest_implied_prob = 100
    wanted_bet = None
    for i in results:
        implied_prob = i['Total Implied Probability (%)']
        if implied_prob < lowest_implied_prob:
            wanted_bet = i
            lowest_implied_prob = implied_prob

    return wanted_bet