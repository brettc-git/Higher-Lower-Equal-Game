import pydealer
import pandas as pd
import numpy as np


class InvalidClassError(Exception):
    pass


# TO-DO: Implement the system for how the comparisons will be made
class GameEngine:

    hle_ranks = {
        "values": {
            "Ace": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "Jack": 11,
            "Queen": 12,
            "King": 13,
        }
    }

    hle_suits = {
        "suits": ["Spades", "Hearts", "Clubs", "Diamonds"],
    }

    def __init__(self):
        self.player_score = 0
        self.cpu_score = 0
        self.sample_deck = pydealer.Deck(ranks=self.hle_ranks, suits=self.hle_suits)
        self.stack = 0  # The stack of cards that will be accumulating cards if the game goes past using the 46 cards.
        self.isPlayer = (
            True  # True if it is the player's turn, False if it is the CPU's turn
        )

    # Returns the value of the card
    def card_value(self, card):
        return self.hle_ranks["values"][card.value]

    # Refills the stack in case deck runs out of the 46 cards
    def refill_stack(self):
        self.stack.shuffle()

    def terminate_game(self):
        # If player_score == 50 or cpu_score == 50 end the game
        if self.player_score == 50 or self.cpu_score == 50:
            return True

    # Update the score of player or CPU, card dealt and next card of game passed to this function
    def update_score(self, card_dealt, next_card, guess):
        # Compute the result of the guess, will be added or deducted
        result = abs(self.card_value(next_card) - self.card_value(card_dealt))

        match guess:
            case "Higher":
                if self.card_value(next_card) > self.card_value(card_dealt):
                    if self.isPlayer:
                        self.player_score += result
                    else:
                        self.cpu_score += result
                else:
                    if self.isPlayer:
                        self.player_score -= result
                    else:
                        self.cpu_score -= result
            case "Lower":
                if self.card_value(next_card) < self.card_value(card_dealt):
                    if self.isPlayer:
                        self.player_score += result
                    else:
                        self.cpu_score += result
                else:
                    if self.isPlayer:
                        self.player_score -= result
                    else:
                        self.cpu_score -= result
            case "Equal":
                if self.card_value(next_card) == self.card_value(card_dealt):
                    if self.isPlayer:
                        self.player_score += 20
                    else:
                        self.cpu_score += 20
                else:
                    if self.isPlayer:
                        self.player_score -= 20
                    else:
                        self.cpu_score -= 20
            case _:
                print("Exception occurred.")
                raise InvalidClassError("Invalid class provided.")


class Expectimax(GameEngine):
    """Used for doing expectimax calculations for the game (Player's assistance only)"""

    def __init__(self):
        super().__init__()
        self.expected_value = 0

    # Looks at the utility of every card left in the stack and offers which of player's card to choose AND what choice they should make.
    def expectimax(self, hand, deck):

        # Our expected value and predicted move will be at worst case scenario first.
        # This is our initial expected value while we look for better expected values in the loops below
        maxEV = -np.inf
        best_move = None

        # The fraction to compute each expected value
        probability = 1 / deck.size

        # Expectimax calculated through going down the tree of all possible moves
        for card in hand:  # First level, go through each card in the hand
            for guess in [
                "Higher",
                "Lower",
                "Equal",
            ]:  # Go through each option the player has
                for (
                    current_card
                ) in (
                    deck
                ):  # Go through every card in the deck and find the maximum expected value
                    if (
                        guess == "Higher"
                    ):  # Circumstance for every outcome, right or wrong guesses
                        utility = (
                            abs(self.card_value(current_card) - self.card_value(card))
                            if self.card_value(current_card) > self.card_value(card)
                            else -abs(
                                self.card_value(current_card) - self.card_value(card)
                            )
                        )
                        # The utility is the absolute difference between the two cards if the current card is higher than the card in hand, otherwise it is the negative of the absolute difference
                    elif guess == "Lower":
                        utility = (
                            abs(self.card_value(current_card) - self.card_value(card))
                            if self.card_value(current_card) < self.card_value(card)
                            else -abs(
                                self.card_value(current_card) - self.card_value(card)
                            )
                        )
                        # Utility is same as above, but in the case that the current card is lower than the card in hand
                    else:  # guess == "Equal"
                        utility = (
                            20
                            if self.card_value(current_card) == self.card_value(card)
                            else -20
                        )  # 20 total points will be added if the card is equal to current card in hand, the same amount is deducted otherwise

                    self.expected_value = probability * utility  # Expected value will

            # Check if new expected value is better than the current best expected value
            if self.expected_value > maxEV:
                maxEV = self.expected_value
                best_move = (card, guess)

        return maxEV, best_move


class NaiveBayes(GameEngine):
    def __init__(self):
        super().__init__()  # Go back to later
        self.training_data = pd.DataFrame(columns=["Card1", "Card2", "Card3", "Class"])
        self.class_probs = {
            "Higher": self.training_data["Class"].value_counts()["Higher"]
            / len(self.training_data),
            "Lower": self.training_data["Class"].value_counts()["Lower"]
            / len(self.training_data),
            "Equal": self.training_data["Class"].value_counts()["Equal"]
            / len(self.training_data),
        }  # Probabilities of each class given data of successful guesses

    def update_class_probs(self):
        if len(self.training_data) >= 1:
            self.class_probs = {
                "Higher": self.training_data["Class"].value_counts().get("Higher", 0)
                / len(self.training_data),
                "Lower": self.training_data["Class"].value_counts().get("Lower", 0)
                / len(self.training_data),
                "Equal": self.training_data["Class"].value_counts().get("Equal", 0)
                / len(self.training_data),
            }

    # To calculate conditional probability, we must consider P(Class|Card1, Card2, Card3) = P(Class) * P(Card1|Class) * P(Card2|Class) * P(Card3|Class)
    # Given a current hand, we will calculate the probability of each class and return an list of each probability, and the highest probability in a tuple
    def conditional_prob(self, current_hand):

        classes = list(
            self.class_probs.keys()
        )  # "higher", "Lower", "Equal" as a lis ["Higher", "Lower", "Equal"]

        # Get count of each class in the Classes column of the training data i.e. 9, 5, 6 in a set of 20
        class_counts = [
            self.training_data["Class"].value_counts()[class_type]
            for class_type in classes
        ]

        # In the order: higher, lower, equal
        probabilities = []

        # Probability can be calculated as:
        # P(Class|Card1, Card2, Card3) = P(Class) * P(Card1|Class) * P(Card2|Class) * P(Card3|Class)

        for class_type in classes:
            temp_prob = self.class_probs[class_type]  # P(Current Class)

            for i, card in enumerate(current_hand):
                # temp_prob *= P(Cardx|Class) for each class
                card_value = self.card_value(card)  # Gets card values from current_hand

                # Conditional probability of each card and each class in the loop
                matching_rows = len(
                    self.training_data[
                        (self.training_data.iloc[:, i] == card_value)
                        & self.training_data["Class"]
                        == class_type
                    ]
                )
                temp_prob *= matching_rows / class_counts[classes.index(class_type)]

            # Append conditional probability of each class to the probabilities list
            probabilities.append(temp_prob)

        max_class = classes[
            probabilities.index(max(probabilities))
        ]  # Get the class with the highest probability
        # Return all the probabilities and the class with the highest probability and its probability in a tuple
        return (probabilities, (max(probabilities), max_class))

    # Update training data with the three cards from player and class of outcome
    def update_data(self, current_hand, outcome):
        new_row = []

        for i in current_hand:
            new_row.append(self.card_value(i))

        match outcome:
            case "Higher":
                new_row.append("Higher")
                # attach class higher to training data column 4
            case "Lower":
                new_row.append("Lower")
                # attach class lower to training data column 4
            case "Equal":
                new_row.append("Equal")
                # attach class equal to training data column 4
            case _:
                print("Exception occurred.")
                raise InvalidClassError("Invalid class provided.")

        self.training_data.loc[len(self.training_data)] = new_row
        self.update_class_probs()


newGame = GameEngine()
newGame.sample_deck.shuffle()
players_hand = newGame.sample_deck.deal(3)
cpu_hand = newGame.sample_deck.deal(3)
remaining_cards = newGame.sample_deck.size


print("Player: ")
print(players_hand)

print("CPU: ")
print(cpu_hand)

print("Remaining cards:", remaining_cards)
