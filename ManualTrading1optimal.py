import numpy as np
from itertools import product

def find_optimal_trade_path(exchange_rates, start_currency, max_trades, initial_amount):
    """
    Find the optimal trading path to maximize the final amount of the starting currency.
    
    Parameters:
    - exchange_rates: Dictionary mapping (from_currency, to_currency) to the exchange rate
    - start_currency: The currency to start and end with
    - max_trades: Maximum number of trades allowed
    - initial_amount: Initial amount of the starting currency
    
    Returns:
    - best_path: List of currencies in the optimal path
    - best_value: Final amount of the starting currency
    """
    # Define all available currencies in the trading system
    currencies = ['SeaShells', 'Snowballs', 'Pizzas', 'SiliconNuggets']
    
    # Create adjacency matrix for exchange rates - this is a 4x4 matrix where
    # each cell [i,j] represents the exchange rate from currency i to currency j
    n = len(currencies)
    rate_matrix = np.zeros((n, n))
    
    # Populate the rate matrix with exchange rates from the provided dictionary
    # This makes lookups faster during the recursive search
    for i, from_curr in enumerate(currencies):
        for j, to_curr in enumerate(currencies):
            if from_curr == to_curr:
                # Set self-exchange rate to 1.0 (no change when converting to same currency)
                rate_matrix[i, j] = 1.0
            else:
                key = (from_curr, to_curr)
                if key in exchange_rates:
                    # Store the exchange rate from the provided rates dictionary
                    rate_matrix[i, j] = exchange_rates[key]
    
    # Initialize variables to track the best trading path found so far
    # Start with just the initial currency and the initial amount
    best_path = [start_currency]
    best_value = initial_amount
    start_idx = currencies.index(start_currency)
    
    def dfs(current_idx, current_value, trades_left, path_so_far):
        """
        Recursive depth-first search to explore all possible trading paths
        
        Parameters:
        - current_idx: Index of current currency
        - current_value: Current amount after converting through the path
        - trades_left: Number of trades remaining
        - path_so_far: List of currency indices visited so far
        
        Returns:
        - best_value, best_path for this sub-problem
        """
        nonlocal best_value, best_path
        
        # If we've completed a path that ends at the start currency with better value, update best
        if trades_left == 0:
            if current_idx == start_idx and current_value > best_value:
                # Convert indices to currency names
                curr_path = []
                for idx in path_so_far:
                    curr_path.append(currencies[idx])
                best_path = curr_path
                best_value = current_value
            return
        
        # Try all possible next currencies (exhaustive search)
        for next_idx in range(n):
            # Skip self-trades (generally not profitable)
            if next_idx == current_idx:
                continue
                
            # Calculate value after this trade
            rate = rate_matrix[current_idx, next_idx]
            
            # Only explore this path if rate is positive
            if rate > 0:
                next_value = current_value * rate
                # Continue exploring this path
                dfs(next_idx, next_value, trades_left - 1, path_so_far + [next_idx])
    
    # Try all possible trade counts from 1 to max_trades
    for trade_count in range(1, max_trades + 1):
        # Start with initial currency index
        dfs(start_idx, initial_amount, trade_count, [start_idx])
    
    return best_path, best_value

# Define the exchange rates from the table
exchange_rates = {
    ('Snowballs', 'Snowballs'): 1.0,
    ('Snowballs', 'Pizzas'): 1.45,
    ('Snowballs', 'SiliconNuggets'): 0.52,
    ('Snowballs', 'SeaShells'): 0.72,
    
    ('Pizzas', 'Snowballs'): 0.7,
    ('Pizzas', 'Pizzas'): 1.0,
    ('Pizzas', 'SiliconNuggets'): 0.31,
    ('Pizzas', 'SeaShells'): 0.48,
    
    ('SiliconNuggets', 'Snowballs'): 1.95,
    ('SiliconNuggets', 'Pizzas'): 3.1,
    ('SiliconNuggets', 'SiliconNuggets'): 1.0,
    ('SiliconNuggets', 'SeaShells'): 1.49,
    
    ('SeaShells', 'Snowballs'): 1.34,
    ('SeaShells', 'Pizzas'): 1.98,
    ('SeaShells', 'SiliconNuggets'): 0.64,
    ('SeaShells', 'SeaShells'): 1.0,
}

# Find the optimal trading path
initial_amount = 500000
start_currency = 'SeaShells'
max_trades = 5

def optimize_with_iterative_deepening(exchange_rates, start_currency, max_trades, initial_amount):
    """
    Find optimal path using exhaustive search to find the absolute best trades.
    """
    best_overall_path = [start_currency]
    best_overall_value = initial_amount
    
    # Define all currencies in the system
    currencies = ['SeaShells', 'Snowballs', 'Pizzas', 'SiliconNuggets']
    start_idx = currencies.index(start_currency)
    
    # Try paths with different numbers of trades from 1 to max_trades
    for num_trades in range(1, max_trades + 1):
        # For each possible path length, we'll use BFS to find the best path
        paths = [[start_currency]]
        values = [initial_amount]
        
        for t in range(num_trades):
            # At each trade step, we'll generate new possible paths
            new_paths = []
            new_values = []
            
            # BFS: Breadth-First Search - explores all possible next trades at current depth before going deeper
            for path, value in zip(paths, values):
                current_curr = path[-1]
                
                # If this is the final trade, we must return to starting currency
                if t == num_trades - 1:
                    next_curr = start_currency
                    next_value = value * exchange_rates.get((current_curr, next_curr), 0)
                    if next_value > 0:
                        new_path = path + [next_curr]
                        new_paths.append(new_path)
                        new_values.append(next_value)
                else:
                    # For intermediate trades, consider all possible next currencies
                    for next_curr in currencies:
                        # Skip self-trades (redundant trades)
                        if next_curr == current_curr:
                            continue
                        
                        # Calculate the new value after this potential trade
                        next_value = value * exchange_rates.get((current_curr, next_curr), 0)
                        if next_value > 0:
                            new_path = path + [next_curr]
                            new_paths.append(new_path)
                            new_values.append(next_value)
            
            # Update our collection of paths to consider in the next iteration
            paths = new_paths
            values = new_values
            
            # No pruning since performance is not an issue
        
        # After exploring all paths with current trade count, find the best one
        # We only care about paths that end in our starting currency
        end_paths = []
        end_values = []
        for i, path in enumerate(paths):
            if path[-1] == start_currency:
                end_paths.append(path)
                end_values.append(values[i])
        
        if end_paths:
            best_idx = end_values.index(max(end_values))
            if end_values[best_idx] > best_overall_value:
                best_overall_path = end_paths[best_idx]
                best_overall_value = end_values[best_idx]
    
    return best_overall_path, best_overall_value

best_path, best_value = optimize_with_iterative_deepening(exchange_rates, start_currency, max_trades, initial_amount)

# Print the results
print(f"Initial amount: {initial_amount} {start_currency}")
print(f"Optimal trading path: {' -> '.join(best_path)}")
print(f"Final amount: {best_value:.2f} {start_currency}")
print(f"Profit: {best_value - initial_amount:.2f} {start_currency} ({(best_value/initial_amount - 1)*100:.2f}%)")

# Calculate the step-by-step results
print("\nStep-by-step trades:")
current_amount = initial_amount
current_currency = start_currency

for i in range(1, len(best_path)):
    from_curr = best_path[i-1]
    to_curr = best_path[i]
    rate = exchange_rates[(from_curr, to_curr)]
    next_amount = current_amount * rate
    
    print(f"Trade {i}: {current_amount:.2f} {from_curr} -> {next_amount:.2f} {to_curr} (rate: {rate})")
    
    current_amount = next_amount
    current_currency = to_curr
