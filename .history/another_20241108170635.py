import pydealer

deck = pydealer.Deck()

card_x = deck.deal()
card_y = deck.deal()

result = card_x == card_y
result = card_x != card_y
result = card_x > card_y
result = card_x >= card_y
result = card_x < card_y
result = card_x <= card_y
