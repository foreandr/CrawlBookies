import crawlers
import util
import report
import hyperSel.log_utilities as log_utilities
def main():

    # GET BETS
    all_bets_raw, bet_functions, bet_counts = crawlers.get_all_bets_raw(
        test=False, 
        sports=["basketball"]
    )

    print("bet_counts:", bet_counts)

    # CLEAN BETS
    cleaned_bets = crawlers.clean_all_bets(all_bets_raw)
    print("cleaned_bets:", len(cleaned_bets))

    # GROUP BETS
    grouped_bets = util.group_similar_dicts(cleaned_bets, threshold=0.7)
    print("\nCHECKPOINT [3]")
    #print("grouped_bets:")
        
    # ARB BETS
    arbs = sorted(crawlers.grouped_bets_cleaner(grouped_bets), key=lambda x: x['implied_probability'])
    #for arb in arbs:
    #    print(arb)
    #    print("--")

    #print("\narbs:", arbs)
    print("CHECKPOINT [4]")

    # RETURN RESULTS
    final_data_dict = {
        "arbs": arbs,
        "grouped_bets": grouped_bets,
        "cleaned_bets": cleaned_bets,
        "all_bets_raw":all_bets_raw,
        "bet_functions": len(bet_functions),
        "bet_counts": bet_counts  # Add the dictionary to the final data
    }
    # report.write_betting_data_to_csv(data_list=all_bets_raw)

    return final_data_dict

if __name__ == '__main__':
    res = main()
    print("\n\n\n", "="*25, "RESULTS","="*25)
    arbs = res['arbs']
    for i in arbs:
        print(i)
        print("--")