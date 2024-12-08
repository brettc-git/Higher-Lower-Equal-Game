# Higher-Lower-Equal Game

Group Members
- Brett Chiu
- Florentino Becerra
- Jesus Lozano-Vega
  
## Assets Used
- Pydealer library
- Pygame
- https://totalnonsense.com/download/vector-play-card-download/ TotalNonsense's SVG cards


## Rules of the Game
- Two players (the player and a CPU) are dealt there cards each and there is a deck of cards that both of them draw from. All six cards from both players are face-up while the deck remains face-down.
- Each player takes consecutive turns deciding which card will be chosen to compare with the one at the top of the deck. For example, if the player has cards with rank A, 7, and J, and they decide to choose the card with rank 7, they can choose if the card will be higher than, lower than, or equal to the card in the deck.
- Depending on whether the guess is correct or incorrect, points will be added/deducted from the player or CPU depending on their choice. For example, if a player decides to choose the card with 7 and guesses lower with the card revealed to be 2, they will earn the difference between the two cards (7-2=5).
- The first player that wins 50 points in total wins the game.
- In the event that a player guesses that the next card is equal to their card correctly, this will result in 20 points being added, inversely 20 points will be lost if the cards are not equal.
- In the event that a player guesses that the next card is higher or lower, but the card turns out to be equal, 5 points will be deducted.
- If the deck is emptied before a victory, then it is shuffled. 

Additionally:
- Ace (A) = 1
- Jack (J) = 11
- Queen (Q) = 12
- King (K) = 13

