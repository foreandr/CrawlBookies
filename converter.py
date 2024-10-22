import pybettor
from fractions import Fraction
import re
import math

def round_down_to_two_places(value):
    """
    Rounds down the value to two decimal places.
    """
    return math.floor(value * 100) / 100

def detect_odds_type(odds):
    """
    Detects the type of odds and returns the cleaned version of the odds.
    Returns ('us', cleaned_odds), ('frac', cleaned_odds), or ('dec', cleaned_odds).
    """
    # Convert odds to string and clean extra spaces
    odds = str(odds).strip()

    # Standardize minus signs and non-ASCII slashes
    odds = odds.replace("−", "-").replace("／", "/")

    # Remove any non-numeric, non-slash, non-minus/plus characters (e.g., $, %, etc.)
    cleaned_odds = re.sub(r'[^\d\.\-+/]', '', odds)  # Keeps numbers, dots, slashes, plus/minus

    # Check for American odds (starts with + or -)
    if cleaned_odds.startswith('+') or cleaned_odds.startswith('-'):
        return 'us', cleaned_odds  # Return format and cleaned odds

    # Check for fractional odds (contains a slash)
    elif '/' in cleaned_odds:
        cleaned_odds = cleaned_odds.replace(' ', '')  # Remove spaces around fractions
        return 'frac', cleaned_odds  # Return format and cleaned odds

    # Check for decimal odds (no slash, just a number)
    else:
        try:
            float(cleaned_odds)  # Convert to float to ensure it's valid decimal odds
            return 'dec', cleaned_odds  # Return format and cleaned odds
        except ValueError:
            raise ValueError(f"Unknown odds format: {odds}")

def fractional_to_decimal(odds):
    """
    Converts fractional odds (e.g., '3/2') to decimal odds.
    
    Args:
        odds (str): Fractional odds in string format (e.g., '3/2', '5/1')
    
    Returns:
        float: Decimal odds.
    """
    try:
        # Convert the fractional string to a Fraction object
        fraction = Fraction(odds)
        
        # Decimal odds = (numerator/denominator) + 1
        decimal_odds = float(fraction) + 1
        
        return round_down_to_two_places(decimal_odds)  # Round down to 2 decimal places
    except ValueError:
        raise ValueError(f"Invalid fractional odds format: {odds}")

def pybetter_decimal_conversion(raw_odds):
    """
    Converts odds to decimal format using pybettor for American odds
    and a custom function for fractional odds.
    """
    try:
        odds_type, odds = detect_odds_type(raw_odds)

        # If it's already decimal, just return it
        if odds_type == 'dec':
            return round_down_to_two_places(float(odds))
        
        # Use the custom fractional conversion if it's fractional odds
        if odds_type == 'frac':
            return fractional_to_decimal(odds)
        
        # Use pybettor for American odds
        result = pybettor.convert_odds(odds=float(odds), cat_in=odds_type, cat_out='dec')
        
        if isinstance(result, list):
            return round_down_to_two_places(result[0])
        
        return round_down_to_two_places(result)

    except Exception as e:
        # print(f"BET FAILED? [e:{e}] [odds:{odds}] ")
        raise ValueError("Unknown odds format")

def convert_to_decimal(odds):
    if odds.lower() == "even":
        odds = 1.0
    """
    Converts odds of any type to decimal format.
    """
    return pybetter_decimal_conversion(odds)

# Expanded test cases to capture every possible bet type
test_odds = [
    # American odds (positive and negative)
    "-2500",   # Large negative American odds
    "−1450",    # Positive American odds
    "+150",    # Positive American odds
    "-110",    # Standard negative American odds
    "+400",    # Positive American odds
    "-200",    # Moderate negative American odds
    "+250",    # Positive American odds
    
    # Fractional odds (simple and complex)
    "3/2",     # Standard fractional odds
    "5/1",     # Large fractional odds
    "1/1",     # Even fractional odds
    "2/5",     # Small fractional odds
    "7/4",     # Mid-range fractional odds
    "11/10",   # Fractional odds just above even
    "4/9",     # Complex fractional odds
    "8/15",    # Small fractional odds
    "5/2",     # Mid-range fractional odds
    "1/4",     # Small fractional odds
    "100/1",   # Large fractional odds
    "10/3",    # Complex fractional odds
    
    # Decimal odds (simple and edge cases)
    "1.75",    # Common decimal odds
    "2.5",     # Mid-range decimal odds
    "0.5",     # Unlikely edge case (should fail, invalid odds)
    "1.0",     # Break-even odds
    "3.0",     # Standard positive decimal odds
    "10.0",    # Larger decimal odds
    "100.0",   # Very large decimal odds
    "1000.0",  # Extremely large decimal odds
]

# Run tests
if __name__ == '__main__':
    for odds in test_odds:
        try:
            print(f"Original odds: {odds} => Decimal odds: {convert_to_decimal(odds)}")
        except ValueError as e:
            print(f"Error converting {odds}: {e}")
            break
