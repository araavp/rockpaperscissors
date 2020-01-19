# Import
import random
import math

# Declare variables
fix_typo = [["r", "o", "c", "k"], ["p", "a", "p", "e", "r"], ["s", "c", "i", "s", "s", "o", "r", "s"]]
rock_typo = ["r", "o", "c", "k"]
paper_typo = ["p", "a", "p", "e", "r"]
scissors_typo = ["s", "c", "i", "s", "s", "o", "r", "s"]
letter_count = 0
user_choice = ""
user_intchoice = 0
all_userchoices = []
cpu_choice = ""
all_cpuchoices = []
user_gamedifficulty = ""
game_difficulty = 0
user_input = ""
cpu_input = 0
wins = 0
draws = 0
losses = 0
score = wins - losses
record = "(" + str(wins) + "-" + str(losses) + "-" + str(draws) + ")"
all_results = []  # 0 is user win, 1 is cpu win, 2 is draw
half_length = 0
last2 = '33'
RPS_count = {'000': 3, '001': 3, '002': 3, '010': 3, '011': 3, '012': 3, '020': 3, '021': 3, '022': 3, '100': 3,
             '101': 3, '102': 3, '110': 3, '111': 3, '112': 3, '120': 3, '121': 3, '122': 3, '200': 3, '201': 3,
             '202': 3, '210': 3, '211': 3, '212': 3, '220': 3, '221': 3, '222': 3}


# Choose user difficulty
def difficulty():
    global user_gamedifficulty, game_difficulty

    user_gamedifficulty = str(input("Choose a level of difficulty (easy or hard): "))
    user_gamedifficulty = user_gamedifficulty.lower()

    if "e" in user_gamedifficulty:
        game_difficulty = 1  # Easy
    elif "h" in user_gamedifficulty:
        game_difficulty = 2  # Hard
    else:
        print("Pick from only the options listed")
        difficulty()

    start_game()


# Starts game
def start_game():
    global user_choice, user_intchoice, letter_count, user_input, user_gamedifficulty, game_difficulty
    letter_count = 0

    user_input = str(input("Choose rock, paper, or scissors: "))
    user_input = user_input.lower()

    # Checks for typos
    for i in fix_typo:
        letter_count = 0
        user_choice = ""

        if letter_count < 4:
            letter_count = 0
            for j in i:
                if j in user_input:
                    letter_count += 1

        if letter_count > 3:
            if i == fix_typo[0]:
                user_choice = "Rock"
                user_intchoice = 1
                all_userchoices.insert(0, user_intchoice)
            if i == fix_typo[1]:
                user_choice = "Paper"
                user_intchoice = 2
                all_userchoices.insert(0, user_intchoice)
            if i == fix_typo[2]:
                user_choice = "Scissors"
                user_intchoice = 3
                all_userchoices.insert(0, user_intchoice)

            print("You chose:", user_choice)

        if user_choice != "":
            if game_difficulty == 1:
                cpu_random()
            if game_difficulty == 2:
                alg()

    # If input is unrecognizable
    if user_choice == "":
        print("Pick from only the options")
        start_game()


# Generates random computer choice
def cpu_random():
    global cpu_input

    cpu_input = random.randint(1, 3)
    compare()


# Compares user and computer choice
def compare():
    global wins, cpu_choice, draws, losses, cpu_input

    all_cpuchoices.insert(0, cpu_input)

    if cpu_input == 1:
        cpu_choice = "Rock"
    if cpu_input == 2:
        cpu_choice = "Paper"
    if cpu_input == 3:
        cpu_choice = "Scissors"

    print("The computer chose:", cpu_choice)
    print()

    if ((cpu_input == 1 and user_choice == "Paper") or (cpu_input == 2 and user_choice == "Scissors")
            or (cpu_input == 3 and user_choice == "Rock")):
        print("You won!")
        wins += 1
        all_results.insert(0, 0)
    if ((cpu_input == 1 and user_choice == "Scissors") or (cpu_input == 2 and user_choice == "Rock")
            or (cpu_input == 3 and user_choice == "Paper")):
        print("You lost!")
        losses += 1
        all_results.insert(0, 1)
    if cpu_choice == user_choice:
        print("It is a draw!")
        draws += 1
        all_results.insert(0, 2)

    restart()


# Finds patterns in user's choices
def alg():
    global cpu_input, wins, losses, draws, cpu_choice, half_length, last2, user_intchoice

    half_length = math.floor(len(all_userchoices) / 2)
    z = str(user_intchoice - 1)

    if last2[0] == '3':
        last2 = last2[1] + z
        cpu_random()
    else:
        r_count = RPS_count[last2 + '0']
        p_count = RPS_count[last2 + '1']
        s_count = RPS_count[last2 + '2']

        # Detects longest, most recent pattern
        for x in range(2, half_length):
            if all_userchoices[0:x] == all_userchoices[x:2*x]:
                if all_userchoices[x] == 1 or all_userchoices[x] == 2:
                    cpu_input = all_userchoices[x] + 1
                elif all_userchoices[x] == 3:
                    cpu_input = 1
                last2 = last2[1] + z
                compare()

        # Markov chain model
        tot_count = r_count + p_count + s_count

        q_dist = [r_count / tot_count, p_count / tot_count, 1 - (r_count / tot_count) - (p_count / tot_count)]
        result = [max(q_dist[2] - q_dist[1], 0), max(q_dist[0] - q_dist[2], 0), max(q_dist[1] - q_dist[0], 0)]
        resultnorm = math.sqrt(result[0] * result[0] + result[1] * result[1] + result[2] * result[2])
        result = [result[0] / resultnorm, result[1] / resultnorm, 1 - result[0] / resultnorm - result[1] / resultnorm]

        y = random.uniform(0, 1)

        if y <= result[0]:
            cpu_input = 1
        elif y <= result[0] + result[1]:
            cpu_input = 2
        else:
            cpu_input = 3

        RPS_count[last2 + z] += 1

    last2 = last2[1] + z

    compare()


# Starts new round, ends game, and check stats
def restart():
    global score
    global record

    score = wins - losses
    record = "(" + str(wins) + " - " + str(losses) + " - " + str(draws) + ")"

    print()
    play_again = input("Play again or check stats? (yes, no, check stats):")
    play_again = play_again.lower()

    # Starts new round
    if "y" in play_again:
        start_game()
        return None
    # Ends game
    if "n" in play_again:
        print()
        print("Your final score is:", score)
        print("Your final record is:", record)
    # Checks stats
    if 'st' in play_again:
        print()
        print("Total wins:", wins)
        print("Total losses:", losses)
        print("Total draws:", draws)
        print()
        print("Your score is:", score)
        print("Your record is:", record)
        restart()

    exit()


difficulty()
