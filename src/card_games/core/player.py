class Player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = hand if hand is not None else []

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None

    def show_hand(self):
        return self.hand

    def __str__(self):
        return f"Player({self.name}, Hand: {self.hand})"