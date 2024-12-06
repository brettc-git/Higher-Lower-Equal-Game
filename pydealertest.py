import pydealer

hl_ranks = {
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
    },
    "suits": ["Spades", "Hearts", "Clubs", "Diamonds"],
}


def highlow_value(card):
    return hl_ranks["values"][card.value]


def simple_prob(your_card, deck):

    l = []
    h = []
    eq = []

    for i in deck:
        # Cards lower than your current card
        if highlow_value(your_card) > highlow_value(i):
            l.append(i)
        # Cards higher than your current card
        elif highlow_value(your_card) < highlow_value(i):
            h.append(i)
        # Cards equal than your current card
        elif highlow_value(your_card) == highlow_value(i):
            eq.append(i)
        else:
            print("Exception occurred.")

    lower_prob = round(len(l) / deck.size, 4)
    higher_prob = round(len(h) / deck.size, 4)
    equal_prob = round(len(eq) / deck.size, 4)
    return [lower_prob, higher_prob, equal_prob]


sample_deck = pydealer.Deck()

print("Shuffling deck...")
sample_deck.shuffle()

# Both hands are visible to players
players_hand = sample_deck.deal(2)
cpu_hand = sample_deck.deal(2)

print("Player: ")
print(players_hand)

print("CPU: ")
print(cpu_hand)

stats1 = simple_prob(players_hand[0], sample_deck)

print("Test probability:\n")
print("Probability of a lower card for your first one: ", stats1[0])
print("Probability of a higher card for you first one: ", stats1[1])
print("Probability of an equal value card for your first one: ", stats1[2])

stats2 = simple_prob(players_hand[1], sample_deck)

print("Probability of a lower card for your second one: ", stats2[0])
print("Probability of a higher card for you second one: ", stats2[1])
print("Probability of an equal value card for your second one: ", stats2[2])
