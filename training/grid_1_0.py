import itertools

def solve_optimized(n):
    # Step 1: Pre-calculate all possible single rows that sum to an odd number
    valid_rows = []
    for row in itertools.product([0, 1], repeat=n):
        if sum(row) % 2 != 0:
            valid_rows.append(row)
    
    count = 0
    
    # Step 2: Iterate through combinations of these VALID rows only
    # We are picking 'n' rows from our valid_rows list
    for grid in itertools.product(valid_rows, repeat=n):
        
        # Rows are already guaranteed odd by Step 1.
        # We only need to check columns.
        cols_valid = True
        for c in range(n):
            col_sum = sum(grid[r][c] for r in range(n))
            if col_sum % 2 == 0:
                cols_valid = False
                break
        
        if cols_valid:
            count += 1
            
    return count

# --- Run the Code ---
n_input = 1
print(f"Calculating for n={n_input} using optimized approach...")
result = solve_optimized(n_input)
print(f"Total valid grids for n={n_input}: {result}")