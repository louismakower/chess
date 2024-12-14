from game import Game

def get_game_setup_params():
    valid_human = False
    while not valid_human:
        human_colour = input("Enter the colour you want to play as (either b or w): ")
        if human_colour in {'w', 'b'}:
            valid_human = True
        else:
            print("Not valid; please enter either 'w' or 'b'.")

    cutoffs = {'easy': 2, 'medium': 3, 'hard': 4}
    valid_difficulty = False
    while not valid_difficulty:
        difficulty = input("Enter the difficulty you want the computer to play at (either easy, medium, or hard): ")
        if difficulty in {'easy', 'medium', 'hard'}:
            cutoff = cutoffs[difficulty]
            valid_difficulty = True
        else:
            print("Not valid; please enter 'easy', 'medium', or 'hard'.")

    return human_colour, cutoff

if __name__ == "__main__":
    human_colour, cutoff = get_game_setup_params()
    game = Game(human_colour, cutoff)
    game.play()