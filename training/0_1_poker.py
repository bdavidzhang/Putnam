import random

def get_user_strategy_params():
    """Helper to get strategy thresholds from user for simulation."""
    print("\n--- Define Your Strategy ---")
    print("Standard Strategy: Bet if x > Value_Threshold.")
    print("Bluffing Strategy: Also Bet if x < Bluff_Threshold.")
    
    while True:
        try:
            v_input = input("Enter Value Threshold (0.0 - 1.0) [e.g., 0.55]: ")
            val_thresh = float(v_input)
            if 0 <= val_thresh <= 1:
                break
            print("Please enter a number between 0 and 1.")
        except ValueError:
            print("Invalid input.")

    while True:
        try:
            b_input = input("Enter Bluff Threshold (0.0 - 1.0) [Enter 0 for none, e.g., 0.11]: ")
            bluff_thresh = float(b_input)
            if 0 <= bluff_thresh <= 1:
                break
            print("Please enter a number between 0 and 1.")
        except ValueError:
            print("Invalid input.")
            
    return val_thresh, bluff_thresh

def simulate_game(rounds=1000):
    """Simulates the game for N rounds based on user thresholds."""
    val_thresh, bluff_thresh = get_user_strategy_params()
    
    # House GTO Call Threshold (Fixed)
    HOUSE_CALL_THRESHOLD = 4/9  # approx 0.444
    
    initial_bankroll = 0
    bankroll = initial_bankroll
    
    wins = 0
    losses = 0
    folds = 0
    
    print(f"\nSimulating {rounds} rounds...")
    print(f"Strategy: Bet if x < {bluff_thresh:.2f} OR x > {val_thresh:.2f}")
    print(f"House Strategy: Call if y > {HOUSE_CALL_THRESHOLD:.2f}")
    print("-" * 40)

    for i in range(rounds):
        # 1. Ante
        bankroll -= 1
        pot = 2
        
        # 2. Deal
        x = random.random() # Player
        y = random.random() # House
        
        # 3. Player Decision (Based on simulation thresholds)
        # Bet if x is very low (bluff) or very high (value)
        if x < bluff_thresh or x > val_thresh:
            action = 'bet'
        else:
            action = 'fold'
            
        # 4. Resolve
        if action == 'fold':
            # House wins pot (Bankroll -1 is final for this round)
            folds += 1
        else:
            # Player Bets
            bankroll -= 1 # Cost of bet
            pot += 2      # Pot grows to $4 (assuming house matches for calculation)
            
            # House Decision
            if y > HOUSE_CALL_THRESHOLD:
                # House Calls
                if x > y:
                    bankroll += 4 # Player wins pot
                    wins += 1
                else:
                    # Player loses (Bankroll -2 is final)
                    losses += 1
            else:
                # House Folds
                bankroll += 3 # Player wins pot ($2) + their bet back ($1)
                wins += 1

    # Statistics
    print(f"--- Simulation Results ({rounds} Rounds) ---")
    print(f"Net Profit/Loss: ${bankroll}")
    print(f"EV per Hand: ${bankroll / rounds:.4f}")
    print(f"Win Rate (incl. opponent folds): {wins/rounds * 100:.1f}%")
    print(f"Total Folds by You: {folds}")
    
    # Theoretical Check
    # If using GTO (Val=0.555, Bluff=0.111), EV should be approx -0.05 to 0 (depending on who has the edge, actually game value is -1/9 for P1 in this variant)
    print("-" * 40)
    input("Press Enter to return to menu...")

def play_interactive():
    """The original interactive mode."""
    bankroll = 100
    round_num = 1
    
    ALICE_BLUFF_LIMIT = 1/9
    ALICE_VALUE_LIMIT = 5/9
    BOB_CALL_THRESHOLD = 4/9

    while True:
        print(f"\n--- Round {round_num} | Bankroll: ${bankroll} ---")
        bankroll -= 1
        pot = 2
        x = random.random()
        y = random.random()
        
        print(f"Your Hand (x): {x:.3f}")
        
        optimal_move = "CHECK (FOLD)"
        if x < ALICE_BLUFF_LIMIT:
            optimal_move = "BET (BLUFF)"
        elif x > ALICE_VALUE_LIMIT:
            optimal_move = "BET (VALUE)"
        
        # Uncomment below to see GTO hints
        # print(f"  [Hint: GTO suggests {optimal_move}]")

        while True:
            action = input("Action? (f)old or (b)et: ").lower().strip()
            if action in ['f', 'fold', 'b', 'bet']:
                break
        
        if action in ['f', 'fold']:
            print(f"You folded. House wins pot. House had (y): {y:.3f}")
        else:
            print(f"You bet $1. Pot is now ${pot + 1}...")
            bankroll -= 1
            pot += 2
            
            if y > BOB_CALL_THRESHOLD:
                print(f"House CALLS with {y:.3f}.")
                if x > y:
                    print(f"You Win! ({x:.3f} > {y:.3f})")
                    bankroll += 4
                else:
                    print(f"House Wins. ({y:.3f} > {x:.3f})")
            else:
                print(f"House FOLDS (had {y:.3f}). You win.")
                bankroll += 3

        if bankroll <= 0:
            print("You have gone bust!")
            break
            
        if input("Play again? (y/n): ").lower() != 'y':
            break
        round_num += 1

def main():
    print("=================================================")
    print("      THE [0,1] POKER GAME (You vs. House)")
    print("=================================================")
    while True:
        print("\nMain Menu:")
        print("1. Play Interactive Mode")
        print("2. Run Simulation (1000 rounds)")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            play_interactive()
        elif choice == '2':
            try:
                rounds = int(input("How many rounds? [Default 1000]: ") or 1000)
                simulate_game(rounds)
            except ValueError:
                print("Invalid number.")
        elif choice == '3':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()