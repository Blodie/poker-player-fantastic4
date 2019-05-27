class Player:
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    VERSION = "Fantastic4"

    def betRequest(self, game_state):
        if self.call(game_state) < 100:
            return self.raise_minimum_amount(game_state)
        else:
            return 0

    def showdown(self, game_state):
        pass

    def call(self, game_state):
        return game_state['current_buy_in'] - game_state['players'][game_state['in_action']]['bet']

    def raise_minimum_amount(self, game_state):
        return self.call(game_state) + game_state['minimum_raise']

    def get_cards_sorted(self, game_state):
        cards = game_state['players'][game_state['in_action']]['hole_cards'] + game_state['community_cards']
        cards = sorted(cards, key=lambda x: self.ranks[x['rank']])
        return cards

    def check_straight(self, game_state):
        cards = self.get_cards_sorted(game_state)
        if len(cards) > 4:
            current_ranks = map(lambda x: self.ranks[x['rank']], cards)
            for i in range(len(current_ranks) - 4):
                checking_interval = current_ranks[0 + i: 6 + i]
                reduce1 = reduce((lambda x, y: y if (x - y + 1 == 0) else -1000), checking_interval)
                if reduce1 == checking_interval[-1]:
                    return True
        return False


if __name__ == '__main__':
    game_state = {
        "tournament_id": "550d1d68cd7bd10003000003",

        "game_id": "550da1cb2d909006e90004b1",

        "round": 0,
        "bet_index": 0,
        "small_blind": 10,
        "current_buy_in": 320,
        "pot": 400,
        "minimum_raise": 240,
        "dealer": 1,
        "orbits": 7,
        "in_action": 1,
        "players": [
            {
                "id": 0,  # Id of the player (same as the index)

                "name": "Albert",  # Name specified in the tournament config

                "status": "active",  # Status of the player:
                #   - active: the player can make bets, and win the current pot
                #   - folded: the player folded, and gave up interest in
                #       the current pot. They can return in the next round.
                #   - out: the player lost all chips, and is out of this sit'n'go

                "version": "Default random player",  # Version identifier returned by the player

                "stack": 1010,  # Amount of chips still available for the player. (Not including
                #     the chips the player bet in this round.)

                "bet": 320  # The amount of chips the player put into the pot
            },
            {
                "id": 1,  # Your own player looks similar, with one extension.
                "name": "Bob",
                "status": "active",
                "version": "Default random player",
                "stack": 1590,
                "bet": 80,
                "hole_cards": [  # The cards of the player. This is only visible for your own player
                    #     except after showdown, when cards revealed are also included.
                    {
                        "rank": "6",  # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                        "suit": "hearts"  # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                    },
                    {
                        "rank": "7",
                        "suit": "spades"
                    }
                ]
            },
            {
                "id": 2,
                "name": "Chuck",
                "status": "out",
                "version": "Default random player",
                "stack": 0,
                "bet": 0
            }
        ],
        "community_cards": [  # Finally the array of community cards.
            {
                "rank": "8",
                "suit": "spades"
            },
            {
                "rank": "9",
                "suit": "hearts"
            },
            {
                "rank": "10",
                "suit": "clubs"
            }
        ]
    }

    p = Player()
    print(p.check_straight(game_state))
