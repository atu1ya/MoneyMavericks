# Container data with correct multipliers
containers = {
    10: {'multiplier': 10, 'inhabitants': 1},
    80: {'multiplier': 80, 'inhabitants': 6},
    37: {'multiplier': 37, 'inhabitants': 3},
    17: {'multiplier': 17, 'inhabitants': 1},
    31: {'multiplier': 31, 'inhabitants': 2},
    50: {'multiplier': 50, 'inhabitants': 4},
    90: {'multiplier': 90, 'inhabitants': 10},
    20: {'multiplier': 20, 'inhabitants': 2},
    73: {'multiplier': 73, 'inhabitants': 4},
    89: {'multiplier': 89, 'inhabitants': 8}
}

BASE_AMOUNT = 10000
SECOND_CONTAINER_FEE = 50000

# Calculate all options (single containers and combinations)
all_options = []

# Process single containers
print("CALCULATING SINGLE CONTAINER OPTIONS...")
for container_id, data in containers.items():
    # Calculate values
    total_value = data['multiplier'] * BASE_AMOUNT
    personal_share = total_value / data['inhabitants']
    
    # Save option data
    option = {
        'type': 'single',
        'description': f"Container {container_id} only",
        'ids': (container_id,),
        'values': (total_value,),
        'total_value': total_value,
        'fee': 0,
        'net_value': total_value,
        'inhabitants': data['inhabitants'],
        'personal_share': personal_share
    }
    all_options.append(option)

# Process two-container combinations
print("CALCULATING TWO-CONTAINER COMBINATIONS...")
container_ids = list(containers.keys())
for i in range(len(container_ids)):
    for j in range(i+1, len(container_ids)):
        id1 = container_ids[i]
        id2 = container_ids[j]
        
        # Calculate values
        value1 = containers[id1]['multiplier'] * BASE_AMOUNT
        value2 = containers[id2]['multiplier'] * BASE_AMOUNT
        total_value = value1 + value2
        net_value = total_value - SECOND_CONTAINER_FEE
        total_inhabitants = containers[id1]['inhabitants'] + containers[id2]['inhabitants']
        personal_share = net_value / total_inhabitants
        
        # Save option data
        option = {
            'type': 'combination',
            'description': f"Containers {id1} + {id2}",
            'ids': (id1, id2),
            'values': (value1, value2),
            'total_value': total_value,
            'fee': SECOND_CONTAINER_FEE,
            'net_value': net_value,
            'inhabitants': total_inhabitants,
            'personal_share': personal_share
        }
        all_options.append(option)

# Sort all options by personal share (best to worst)
all_options_sorted = sorted(all_options, key=lambda x: x['personal_share'], reverse=True)

# Print results in order from best to worst
print("\nALL OPTIONS RANKED FROM BEST TO WORST:")
print("=" * 120)
print(f"{'Rank':<6} {'Option':<20} {'Total Value':<15} {'Fee':<10} {'Net Value':<15} {'Inhabitants':<15} {'Personal Share':<15}")
print("-" * 120)

for i, option in enumerate(all_options_sorted):
    print(f"{i+1:<6} {option['description']:<20} {option['total_value']:,d} SeaShells{' ':<3} {option['fee']:,d} SeaShells{' ':<2} {option['net_value']:,d} SeaShells{' ':<3} {option['inhabitants']}{' ':<13} {option['personal_share']:,.0f} SeaShells")

# Print top recommendation
best_option = all_options_sorted[0]
print("\n" + "=" * 80)
print("TOP RECOMMENDATION:")
print(f"{best_option['description']}")
print(f"Expected personal gain: {best_option['personal_share']:,.0f} SeaShells")
print("=" * 80)

# Additional detailed analysis of best option
print("\nDETAILS OF TOP RECOMMENDATION:")
if best_option['type'] == 'single':
    container_id = best_option['ids'][0]
    multiplier = containers[container_id]['multiplier']
    print(f"Container {container_id}: {multiplier}× multiplier")
    print(f"Base value: {BASE_AMOUNT:,d} SeaShells")
    print(f"Total value: {multiplier} × {BASE_AMOUNT:,d} = {best_option['total_value']:,d} SeaShells")
    print(f"Number of inhabitants: {best_option['inhabitants']}")
    print(f"Personal share: {best_option['total_value']:,d} ÷ {best_option['inhabitants']} = {best_option['personal_share']:,.0f} SeaShells")
else:
    id1, id2 = best_option['ids']
    value1, value2 = best_option['values']
    mult1 = containers[id1]['multiplier']
    mult2 = containers[id2]['multiplier']
    inhab1 = containers[id1]['inhabitants']
    inhab2 = containers[id2]['inhabitants']
    print(f"Container {id1}: {mult1}× multiplier, {value1:,d} SeaShells, {inhab1} inhabitants")
    print(f"Container {id2}: {mult2}× multiplier, {value2:,d} SeaShells, {inhab2} inhabitants")
    print(f"Combined value before fee: {value1:,d} + {value2:,d} = {best_option['total_value']:,d} SeaShells")
    print(f"Fee for second container: {SECOND_CONTAINER_FEE:,d} SeaShells")
    print(f"Net value after fee: {best_option['total_value']:,d} - {SECOND_CONTAINER_FEE:,d} = {best_option['net_value']:,d} SeaShells")
    print(f"Total inhabitants: {inhab1} + {inhab2} = {best_option['inhabitants']}")
    print(f"Personal share: {best_option['net_value']:,d} ÷ {best_option['inhabitants']} = {best_option['personal_share']:,.0f} SeaShells")