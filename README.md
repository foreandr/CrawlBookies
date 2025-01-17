
# Bookie Arbitrage Betting Crawler

This script crawls bookie sites to gather, clean, and analyze bets for arbitrage opportunities. By comparing betting odds across platforms, it identifies bets where you can lock in a profit by placing opposing bets at different bookmakers.

---

## Features

- **Bet Collection**: Gathers raw betting data across specified sports using the `crawlers.get_all_bets_raw` function.
- **Data Cleaning**: Processes and cleans the collected data for consistency.
- **Grouping**: Groups similar bets for easier comparison with a configurable threshold.
- **Arbitrage Calculation**: Identifies arbitrage bets by sorting based on implied probability.
- **Results Export**: Outputs final data to a dictionary for easy access.

---

## Installation

Ensure required dependencies are installed:
```bash
pip install -r req.txt
```

## Usage

To run the crawler:
```bash
python main.py
```

The results, including grouped bets, cleaned bets, and arbitrage opportunities, will be displayed.
