# Import your existing classes
from game_engine import GameEngine, Expectimax
import pydealer
def test_expectimax():
    # Initialize test environment
    expectimax = Expectimax()
    test_deck = pydealer.Deck(ranks=GameEngine.hle_ranks, suits=GameEngine.hle_suits)
    test_deck.shuffle()

    def run_single_test(hand, deck, description):
        print(f"\nTest Case: {description}")
        print(f"Hand: {hand}")
        print(f"Deck size: {deck.size}")

        expected_value, best_move = expectimax.expectimax(hand, deck)
        if best_move:
            chosen_card, chosen_move = best_move
            print(f"Expected Value: {expected_value:.2f}")
            print(f"Chosen Card: {chosen_card}")
            print(f"Recommended Move: {chosen_move}")
            print(f"Card Value: {expectimax.card_value(chosen_card)}")
        else:
            print("No move found!")
        return expected_value, best_move

    # Test Case 1: Extreme Values Test
    print("\n=== Testing Extreme Values ===")
    # Create a hand with Ace (1) and King (13)
    extreme_hand = pydealer.Stack()
    extreme_hand.add([
        pydealer.Card("Ace", "Spades"),    # Value 1
        pydealer.Card("King", "Hearts"),    # Value 13
        pydealer.Card("7", "Diamonds")      # Value 7
    ])
    ev1, move1 = run_single_test(extreme_hand, test_deck, "Extreme Values (Ace, King, 7)")

    # Test Case 2: Middle Values Test
    print("\n=== Testing Middle Values ===")
    middle_hand = pydealer.Stack()
    middle_hand.add([
        pydealer.Card("6", "Spades"),    # Value 6
        pydealer.Card("7", "Hearts"),    # Value 7
        pydealer.Card("8", "Diamonds")   # Value 8
    ])
    ev2, move2 = run_single_test(middle_hand, test_deck, "Middle Values (6, 7, 8)")

    # Test Case 3: Equal Values Test
    print("\n=== Testing Equal Values ===")
    equal_hand = pydealer.Stack()
    equal_hand.add([
        pydealer.Card("Queen", "Spades"),    # Value 12
        pydealer.Card("Queen", "Hearts"),    # Value 12
        pydealer.Card("Queen", "Diamonds")   # Value 12
    ])
    ev3, move3 = run_single_test(equal_hand, test_deck, "Equal Values (Queen, Queen, Queen)")

    # Validation checks
    print("\n=== Validation Results ===")

    # Check if extreme values produce higher expected values
    print("1. Extreme Values Check:", end=" ")
    if abs(ev1) > abs(ev2):
        print("✓ (Extreme values produce higher expected values)")
    else:
        print("✗ (Expected extreme values to produce higher expected values)")

    # Check if moves are valid
    def validate_move(move, description):
        print(f"2. {description}:", end=" ")
        if move and move[1] in ["Higher", "Lower", "Equal"]:
            print("✓ (Valid move suggested)")
            return True
        else:
            print("✗ (Invalid or no move suggested)")
            return False

    validate_move(move1, "Extreme Values Move")
    validate_move(move2, "Middle Values Move")
    validate_move(move3, "Equal Values Move")

    # Check if the algorithm suggests logical moves
    def check_move_logic(move, description):
        if not move:
            return

        card, guess = move
        card_value = expectimax.card_value(card)
        print(f"3. {description} Logic Check:", end=" ")

        if card_value <= 4 and guess == "Higher":
            print("✓ (Correctly suggests Higher for low values)")
        elif card_value >= 10 and guess == "Lower":
            print("✓ (Correctly suggests Lower for high values)")
        elif 5 <= card_value <= 9:
            print("✓ (Middle range value, any guess can be optimal)")
        else:
            print("✗ (Unexpected move suggestion)")

    check_move_logic(move1, "Extreme Values")
    check_move_logic(move2, "Middle Values")
    check_move_logic(move3, "Equal Values")

# Run the tests
if __name__ == "__main__":
    test_expectimax()