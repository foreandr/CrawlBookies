import difflib
import numpy as np
import hyperSel.log_utilities as log_utilities

def chunk_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def transpose_chunks(chunks):
    return list(map(list, zip(*chunks)))

def calculate_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio()

def are_similar(dict1, dict2, threshold=0.62): 
    #goodiesh threshold
    '''
    EG.
    [2024-09-25 10:36:22.009043][test][][]-Similarity between 'Indiana Pacers' and 'IND Pacers': 0.6666666666666666
    [2024-09-25 10:36:22.018992][test][][]-Similarity between 'Detroit Pistons' and 'DET Pistons': 0.6923076923076923
    '''
    
    # log_utilities.log_function(log_string="==="*100)

    # Compare outcome_1 from both dictionaries
    sim_outcome_1 = calculate_similarity(dict1['outcome_1'], dict2['outcome_1'])
    # log_utilities.log_function(log_string=f"Similarity between '{dict1['outcome_1']}' and '{dict2['outcome_1']}': {sim_outcome_1}")

    # Compare outcome_2 from both dictionaries
    sim_outcome_2 = calculate_similarity(dict1['outcome_2'], dict2['outcome_2'])
    # log_utilities.log_function(log_string=f"Similarity between '{dict1['outcome_2']}' and '{dict2['outcome_2']}': {sim_outcome_2}")
    
    # If both outcome_1 and outcome_2 similarity exceed the threshold, return True
    if sim_outcome_1 > threshold and sim_outcome_2 > threshold:
        #print(f"Both outcomes passed the threshold ({threshold}). They are similar.")
        return True
    else:
        #print(f"One or both outcomes did not pass the threshold ({threshold}). They are not similar.")
        return False

def group_similar_dicts(dicts, threshold=0.7):
    '''
    honestly, I feel this needs work, and I feel I am missing data but, i'm not sure how to fix it...
    '''
    groups = []
    used = [False] * len(dicts)
    
    for i in range(len(dicts)):
        if used[i]:
            continue

        group = [dicts[i]]
        used[i] = True
        
        for j in range(i + 1, len(dicts)):
            sim = are_similar(dicts[i], dicts[j], threshold)
            if not used[j] and sim:
                duplicate = False
                for existing in group:
                    # Check if the dictionary already exists based on relevant fields
                    if (existing['odds_1'] == dicts[j]['odds_1'] and 
                        existing['odds_2'] == dicts[j]['odds_2'] and
                        existing['outcome_1'] == dicts[j]['outcome_1'] and
                        existing['outcome_2'] == dicts[j]['outcome_2']):
                        duplicate = True
                        break
                
                if not duplicate:
                    group.append(dicts[j])
                    used[j] = True
        
        if len(group) > 1:
            groups.append(group)
    
    # Sorting groups by size in descending order
    groups = sorted(groups, key=len, reverse=True)
    return groups

def detect_and_split(text):
    if len(text) <= 21:
        return text
    # Initialize variables
    result = []
    truncate = False
    
    # Iterate over each character with its index
    for i, char in enumerate(text):
        if char.isupper():
            # Check if this capital letter is not at the start of the word
            if i > 0 and text[i - 1] != ' ':
                # Trigger truncation if condition is met
                truncate = True
        if truncate:
            break
        result.append(char)
    
    # Convert the result list back to a string and clean up spaces
    cleaned_text = ''.join(result).strip()
    
    return cleaned_text

def detect_anomalies(numbers, threshold_percentage):
    # Convert the list to a NumPy array for easier calculations
    data = np.array(numbers)
    
    # Calculate mean and standard deviation
    mean = np.mean(data)
    std_dev = np.std(data)
    
    # Calculate the threshold for detecting anomalies
    threshold = mean * (threshold_percentage / 100)
    
    # Calculate the acceptable range
    min_value = mean - threshold
    max_value = mean + threshold
    
    # Find anomalies (values that are further than 'threshold' away from the mean)
    anomalies = [num for num in numbers if num < min_value or num > max_value]
    
    return {
        'mean': mean,
        'std_dev': std_dev,
        'threshold': threshold,
        'min_value': min_value,
        'max_value': max_value,
        'anomalies': anomalies
    }

def detect_anomalies_mad(numbers, threshold_percentage):
    # Convert the list to a NumPy array for easier calculations
    data = np.array(numbers)
    
    # Calculate the median and MAD (Median Absolute Deviation)
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    
    # Calculate the threshold for detecting anomalies
    threshold = mad * (threshold_percentage / 100)
    
    # Calculate the acceptable range
    min_value = median - threshold
    max_value = median + threshold
    
    # Find anomalies (values that are further than 'threshold' away from the median)
    anomalies = [num for num in numbers if num < min_value or num > max_value]
    
    return {
        'median': median,
        'mad': mad,
        'threshold': threshold,
        'min_value': min_value,
        'max_value': max_value,
        'anomalies': anomalies
    }

def detect_anomalies_robust(numbers, threshold_percentage):
    # Convert the list to a NumPy array for easier calculations
    data = np.array(numbers)
    
    # Calculate the median
    median = np.median(data)
    
    # Calculate the threshold as a percentage of the median
    threshold = median * (threshold_percentage / 100)
    
    # Calculate the acceptable range
    min_value = median - threshold
    max_value = median + threshold
    
    # Find anomalies (values that are further than 'threshold' away from the median)
    anomalies = [num for num in numbers if num < min_value or num > max_value]
    
    return {
        'median': median,
        'threshold': threshold,
        'min_value': min_value,
        'max_value': max_value,
        'anomalies': anomalies
    }

def anomalies_test():
    bet_ratios = [
        1.9, 1.85, 1.92, 1.94, 1.97, 2.1, 6.0, 1.88, 1.93, 1.95, 
        2.2, 2.35, 1.87, 1.91, 3.5, 2.05, 1.99, 2.0, 2.15, 10.0
    ]
    threshold_percentage = 20

    result = detect_anomalies(bet_ratios, threshold_percentage)
    print(f"Mean: {result['mean']:.2f}")
    print(f"Standard Deviation: {result['std_dev']:.2f}")
    print(f"Anomaly Threshold: ±{result['threshold']:.2f}")
    print(f"Acceptable range: {result['min_value']:.2f} to {result['max_value']:.2f}")
    print(f"Anomalies: {result['anomalies']}")

    print("==="*20)
    result = detect_anomalies_mad(bet_ratios, threshold_percentage)
    print(f"Median: {result['median']:.2f}")
    print(f"MAD: {result['mad']:.2f}")
    print(f"Anomaly Threshold: ±{result['threshold']:.2f}")
    print(f"Acceptable range: {result['min_value']:.2f} to {result['max_value']:.2f}")
    print(f"Anomalies: {result['anomalies']}")

    print("==="*20)
    result = detect_anomalies_robust(bet_ratios, threshold_percentage)
    print(f"Median: {result['median']:.2f}")
    print(f"Anomaly Threshold: ±{result['threshold']:.2f}")
    print(f"Acceptable range: {result['min_value']:.2f} to {result['max_value']:.2f}")
    print(f"Anomalies: {result['anomalies']}")


if __name__ == '__main__':
    
    pass