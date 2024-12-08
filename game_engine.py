import pydealer
import pandas as pd
import numpy as np
import random # for CPU to make random guesses in the game

# Something other than higher, lower or equal exception
class InvalidClassError(Exception):
    pass

# For guesses of card values
class OutOfRangeError(Exception):
    pass

class Player:
    def __init__(self):
        # Each player will have a score and a hand of cards that are dealt in the main loop
        self.score = 0
        self.hand = pydealer.Stack()

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

        self.player = Player()
        self.cpu = Player()
        self.sample_deck = pydealer.Deck(ranks=self.hle_ranks, suits=self.hle_suits)
        self.discard_stack = pydealer.Stack()  # The stack of cards that will be accumulating cards if the game goes past using the 46 cards.

    # Returns the value of the card
    def card_value(self, card):
        return self.hle_ranks["values"][card.value]

    # Refills the stack in case deck runs out of the 46 cards
    def refill_stack(self):
        self.sample_deck.add(self.discard_stack)
        self.sample_deck.shuffle()
        self.discard_stack.clear()

    # Checks if the game should end
    def terminate_game(self):
        # If player score == 50 or cpu score == 50 end the game
        return self.player.score >= 50 or self.cpu.score >= 50

    # Deals card to player/cpu and updates score based on guess, returns how many points were won/lost
    def score_system(self, card_dealt, next_card, guess, player_type="player"):

        # Our result will be the absolute difference between the two cards; which will be added or deducted from the player's score
        result = abs(self.card_value(next_card) - self.card_value(card_dealt))
        flag = True # Default True if the player guesses correctly, False otherwise

        # Check current player
        if player_type == "player":
            player = self.player
        elif player_type == "cpu":
            player = self.cpu
        else:
            raise ValueError("Invalid player type.")

        match guess:
            case "Higher":
                if self.card_value(next_card) > self.card_value(card_dealt):
                    player.score += result
                    flag = True
                elif self.card_value(next_card) == self.card_value(card_dealt):
                    player.score -= 5
                    if player.score - 5 < 0:
                        player.score = 0
                    flag = False # If the cards are actually equal, the player loses 5 points
                    return (flag, 5)
                else:
                    player.score -= result
                    if player.score - result < 0:
                        player.score = 0
                    flag = False
            case "Lower":
                if self.card_value(next_card) < self.card_value(card_dealt):
                    player.score += result
                    flag = True
                elif self.card_value(next_card) == self.card_value(card_dealt):
                    player.score -= 5
                    flag = False
                    return (flag, 5)
                else:
                    player.score -= result
                    if player.score - result < 0:
                        player.score = 0
                    flag = False
            case "Equal":
                if self.card_value(next_card) == self.card_value(card_dealt):
                    player.score += 20
                    flag = True
                else:
                    player.score -= 20
                    if player.score - 20 < 0:
                        player.score = 0
                    flag = False
                    return (flag, 20)
            case _:
                print("Exception occurred.")
                raise InvalidClassError("Invalid class provided.")

        # Tuple has two values: flag (True/False) and result (points won/lost)
        return (flag, result)


# Class designed specifically for the CPU to make guesses in the game
class CPU(GameEngine):

    # Our CPU will not be given expectimax or naive bayes capabilities, it will be making random guesses in the game based on separate logic
    def __init__(self):
        super().__init__()

    # Used to make a guess based on cards in CPU's hand using a different strategy
    def make_guess(self, hand, deck):

        best_card = None
        max_score = -np.inf

        # Get the biggest potential score out of the three cards in the hand
        for card in hand:
            score = self.card_potential(self.card_value(card), deck.size)
            if score > max_score:
                max_score = score
                best_card = card

        # Make guesses based on the cards

        if self.card_value(best_card) <= 4:
            return (best_card, "Higher")
        elif self.card_value(best_card) >= 10:
            return (best_card, "Lower")
        elif 5 <= self.card_value(best_card) <= 9:
            return (best_card, random.choice(["Higher", "Lower", "Equal"]))  # Random guess for middle values
        else:
            if not (1 <= self.card_value(best_card) <= 13):
                raise OutOfRangeError("Card value out of range.")

    # Calculate how good a card is for the given game state
    def card_potential(self, card_value, deck_size):
        # Total number of possible card values (13 in a standard deck)
        vals = len(self.hle_ranks["values"]) # Gets all values of cards possible
        vals = len(self.hle_ranks["values"]) # Gets all values of cards possible

        # Get how many cards could be lower or higher than the curent card
        higher_than = vals - card_value #e.g. 13 - card value 10 = 3 cards higher than 10
        lower_than = card_value - 1 #e.g. 4 - 1 = 3 cards lower than 4

        score = 0

        # Extreme values that can factor into whether the CPU guesses higher or lower
        if card_value in [1,13]:
            score += 7
        elif card_value in [2,12]:
            score += 5
        elif card_value in [6,7,8]:
            score += 3
        else: # For the rest of the values
            score += 1

        score += max(higher_than, lower_than) # Add the maximum of the two values to the score
        if deck_size > 0:
            score *= (deck_size/52) # Multiply the score by the fraction of the deck left
        else: # If the deck is empty, the score will be 0
            score = 0
        score *= (deck_size/52) # Multiply the score by the fraction of the deck left

        return score



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
        probability = 1.0 / deck.size if deck.size > 0 else 0 # Probability of each card in the deck if non-empty

        # Expectimax calculated through going down the tree of all possible moves

            # Check if new expected value is better than the current best expected value
        for card in hand:
            for guess in ["Higher", "Lower", "Equal"]:
                current_EV = 0

                for next_card in deck:
                    # Get the utility for each card which represents a terminal node
                    utility = self.utility_calculation(card, next_card, guess)
                    current_EV += probability * utility

                if current_EV > maxEV:
                    maxEV = current_EV
                    best_move = (card, guess)

            if self.expected_value > maxEV:
                maxEV = self.expected_value
                best_move = (card, guess)

        return maxEV, best_move

    def utility_calculation(self, card, next_card, guess):
        diff = abs(self.card_value(next_card) - self.card_value(card))

        if guess == "Higher":
            return diff if self.card_value(next_card) > self.card_value(card) else -diff
        elif guess == "Lower":
            return diff if self.card_value(next_card) < self.card_value(card) else -diff
        else:  # guess == "Equal"
            return 20 if self.card_value(next_card) == self.card_value(card) else -20


class NaiveBayes(GameEngine):
    def __init__(self):
        super().__init__()  # Go back to later
        # Our table will use pandas and build upon the data from the choices that were made by the player
        self.training_data = pd.DataFrame(columns=["Card1", "Card2", "Card3", "Class"])
        # All initially equal probabilities of each class
        self.class_probs = {
            "Higher": 1/3,
            "Lower": 1/3,
            "Equal": 1/3,
        }  # Probabilities of each class given data of successful guesses

    def update_class_probs(self):
        if len(self.training_data) >= 1:
            total = len(self.training_data)
            self.class_probs = {
                "Higher": (self.training_data["Class"].value_counts().get("Higher", 0) + 1) / (total+3),
                "Lower": (self.training_data["Class"].value_counts().get("Lower", 0) + 1) / (total+3),
                "Equal": (self.training_data["Class"].value_counts().get("Equal", 0) + 1) / (total+3),
            }

    # To calculate conditional probability, we must consider P(Class|Card1, Card2, Card3) = P(Class) * P(Card1|Class) * P(Card2|Class) * P(Card3|Class)
    # Given a current hand, we will calculate the probability of each class and return an list of each probability, and the highest probability in a tuple
    def conditional_prob(self, current_hand):

        classes = list(self.class_probs.keys())  # "higher", "Lower", "Equal" as a list ["Higher", "Lower", "Equal"]

        # Get count of each class in the Classes column of the training data i.e. 9, 5, 6 in a set of 20
        class_counts = { c: len(self.training_data[self.training_data["Class"] == c]) for c in classes }

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
                matching_rows = len(self.training_data[(self.training_data["Card" + str(i+1)] == card_value) & (self.training_data["Class"] == class_type)])

                # Since we have probabilities that will equate to zero, we need to handle this with Laplace smoothing where alpha = 1. This is to avoid zero probabilities.

            # alpha = 1, number of unique card values = 13 is added to the denominator
                temp_prob *= (matching_rows + 1) / (class_counts[class_type] + 13)

            # Append conditional probability of each class to the probabilities list
            probabilities.append(temp_prob)


        max_class = classes[probabilities.index(max(probabilities))]  # Get the class with the highest probability
        # Return all the probabilities and the class with the highest probability and its probability in a tuple
        return (probabilities, (max(probabilities), max_class))

    # Update training data with the three cards from player and class of outcome
    def update_data(self, current_hand, outcome):
        new_row = []

        if outcome not in ["Higher", "Lower", "Equal"]:
            raise InvalidClassError("Invalid class provided.")

        new_row = [self.card_value(card) for card in current_hand]
        new_row.append(outcome)

        self.training_data.loc[len(self.training_data)] = new_row

        self.update_class_probs()

    # convenience function to predict the best guess
    def prediction(self, current_hand):
        probabilities, (max_prob, best_class) = self.conditional_prob(current_hand)
        classes = ["Higher", "Lower", "Equal"]
        probability_breakdown = dict(zip(classes, probabilities))

        return { "Class Probabilities": probability_breakdown, "Best Probability": max_prob, "Best Class": best_class }

