import random
from collections import defaultdict

DEF_DIFFIC = 10
MAX_TRIALS = 20
MAX_VALUE = 99
MIN_VALUE = 1
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
NOT_POSSIBLE = "No FoCdle found of that difficulty"
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"
GRE_YEL = ['green', 'yellow']
GCOUNT_MAX = 10
ALL_CHOICES_SET = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+',
                   '-', '=', '*', '%'}
ALL_CHOICES = '0123456789-+*%'
DEF_S = '-'
DEF_I = 0
DEF_LIST = []
BLANK = ' '


##############################################################################################
def create_secret(difficulty=DEF_DIFFIC):
    '''
    Use a random number function to create a FoCdle instance of length
    `difficulty`. The generated equation will be built around three values
    each from 1 to 99, two operators, and an equality.
        Parameter:
            difficulty (int or str): a digit
        Returns:
            'secret' (3 values, 2 operators, 1 equality, and 1 result) if the
             number of trials is within MAX_TRIALS
            "No FoCdle found of that difficulty", otherwise
    '''
    # ensure 'difficulty' is an integer
    if not isinstance(difficulty, int):
        return "INVALID DIFFICULTY"

    # specify the range of min_value, max_value based on 'difficulty'
    if difficulty <= 8:
        min_value, max_value = MIN_VALUE, 9
    elif difficulty >= 14:
        min_value, max_value = 10, MAX_VALUE
    else:
        min_value, max_value = MIN_VALUE, MAX_VALUE

    # generate random 'secret' within the number of MAX_TRIALS
    trial_count = 0
    while trial_count <= MAX_TRIALS:
        num1, num2, num3 = random.sample(range(min_value, max_value), k=3)
        operator1, operator2 = random.choices(OPERATORS, k=2)
        incomplete_secret = str(num1) + operator1 + str(num2) + \
                            operator2 + str(num3)

        # call check_secret() to check the validity of incomplete_secret
        valid = check_secret(incomplete_secret, difficulty)
        if valid:
            return valid
        trial_count += 1

    # return NOT_POSSIBLE if the number of trials exceed MAX_TRIALS
    return NOT_POSSIBLE


def check_secret(incomplete_secret, difficulty=DEF_DIFFIC):
    '''
    Takes incomplete_secret (string) and difficulty (int) and validates if the
    result of the string is greater than 0 and the final string
    (complete_secret) has the same length as difficulty.
        Returns:
            False if the string is not valid.
            Otherwise, complete_secret (3 values, 2 operators, 1 equality,
            and 1 result).
    '''
    result = eval(incomplete_secret)
    complete_secret = incomplete_secret + EQUALITY + str(result)

    # check if result is greater than 0 and length of complete_secret is equal
    # to difficulty
    return complete_secret if len(complete_secret) == difficulty and \
                              result > 0 else False

##############################################################################################
def set_colors(secret, guess):
    '''
    Compares the latest `guess` equation against the unknown `secret` one.
    Returns a list of three-item tuples, one tuple for each character position
    in the two equations:
        -- a position number within the `guess`, counting from zero;
        -- the character at that position of `guess`;
        -- one of "green", "yellow", or "grey", to indicate the status of
           the `guess` at that position, relative to `secret`.
    The return list is sorted by position.
    '''
    # stores tuples of position, character, colour
    all_info = []

    # find characters of guess that are in correct positions as in secret
    for index, char in enumerate(guess):
        if char == secret[index]:
            all_info.append((index, char, GREEN))
            secret, guess = change_string(secret, guess, index, index)

    # find characters of guess that exist in secret but in wrong positions
    for index, char in enumerate(guess):
        if char != secret[index] and char != ' ' and char in secret:
            all_info.append((index, char, YELLO))
            secret, guess = change_string(secret, guess, secret.index(char),
                                          index)
    # find characters of guess that does not exist in secret
    all_info += [(index, char, GREYY) for index, char in enumerate(guess)
                 if char != ' ']

    return sorted(all_info)


def change_string(secret=DEF_S, guess=DEF_S, index1=DEF_I, index2=DEF_I):
    '''
    Takes 2 different strings and their corresponding indexes. Returns two new
    strings that have their characters replaced by ' ' at those indexes.
    '''
    new_secret = secret[:index1] + ' ' + secret[index1 + 1:]
    new_guess = guess[:index2] + ' ' + guess[index2 + 1:]

    return new_secret, new_guess


##############################################################################################
def passes_restrictions(guess, all_info):
    '''
    Tests a `guess` equation against `all_info`, a list of known restrictions,
    one entry in that list from each previous call to set_colors(). Returns
    True if that `guess` complies with the collective evidence imposed by
    `all_info`; returns False if any violation is detected. Does not check the
    mathematical accuracy of the proposed candidate equation.
    '''
    pass_restriction = True

    # return True is all_info is empty
    if not all_info:
        return pass_restriction

    # add info (index and/or char) to a corresponding list/set based on colours
    green_list, yellow_list, grey_list = [], [], []
    yellow_char_set, grey_char_set = set(), set()
    for info in all_info:
        for index, char, colour in info:
            if colour == GREEN:
                green_list.append((index, char))
            elif colour == YELLO:
                yellow_list.append((index, char))
                yellow_char_set.add(char)
            elif colour == GREYY:
                grey_list.append((index, char))
                grey_char_set.add(char)

    # index all characters in guess
    new_info = [(index, char) for index, char in enumerate(guess)]

    # check if previous greens are, yellows are not, greys are not in new guess
    if not check_inclusion(green_list, new_info) \
            or not check_exclusion(yellow_list, new_info) \
            or not check_exclusion(grey_list, new_info):
        return not pass_restriction

    # check if number of any character in guess is lesser than its combined
    # total in green and yellow lists
    for char in guess:
        for info in all_info:
            char_count = len([char for index, character, colour in info if
                              colour in GRE_YEL and char == character])
            if guess.count(char) < char_count:
                return not pass_restriction

    # check if grey characters are still in new guess by comparing its total
    # count in guess to its combined total in both green and yellow lists
    for char in guess:
        if char in grey_char_set:
            greatest_char_count = 0
            for info in all_info:
                # find total count of grey character in green and yellow lists
                char_count = len([char for index, character, colour in info if
                                  colour in GRE_YEL and char == character])
                # find the max total count among entries
                if char_count > greatest_char_count:
                    greatest_char_count = char_count
            if guess.count(char) > greatest_char_count:
                return not pass_restriction

    # check if number of characters in guess that are not grey is greater than
    # its combined total in green and yellow lists, plus grey tag count
    for char in guess:
        if char not in grey_char_set:
            for info in all_info:
                char_count = len([char for index, character, colour in info if
                                  colour in GRE_YEL and char == character]) + \
                             sum(map(lambda x: x[2] == GREYY, info))
                if guess.count(char) > char_count:
                    return not pass_restriction

    return pass_restriction


def check_inclusion(colour_list, new_info):
    '''
    Takes colour_list and new_info lists, then determines if all items in
    colour_list are still in new_info list. Returns True if they are, otherwise
    False.
    '''
    valid = True
    for colour_info in colour_list:
        if colour_info not in new_info:
            return not valid
    return valid


def check_exclusion(colour_list, new_info):
    '''
    Takes colour_list and new_info lists, then determines if all items in
    colour_list are still in new_info list. Returns False if they are,
    otherwise True.
    '''
    valid = True
    for colour_info in colour_list:
        if colour_info in new_info:
            return not valid
    return valid


##############################################################################################
def create_guess(all_info, difficulty=DEF_DIFFIC):
    '''
    Takes information built up from past guesses that is stored in `all_info`,
    and uses it as guidance to generate a new guess of length `difficulty`.
    '''
    # calling for general_guess() function to generate a random string
    if not all_info:
        return general_guess(difficulty)

    # guess_string_list stores potential values for the final guess
    guess_string_list = [BLANK] * difficulty

    # store all previous yellow characters and their old positions
    yellow_char_dict = defaultdict(set)
    # store all grey characters (and their indexes) in set (and list)
    grey_char, grey_char_set = [], set()
    # repeated_char_dict and repeated_char_set store valid repeated values
    repeated_char_dict, repeated_char_set = defaultdict(int), set()

    # find info based on their colours and store them in corresponding list/set
    for entry in all_info:
        for index, char, colour in entry:
            if colour == GREEN:
                guess_string_list[index] = char
                repeated_char_dict[char] += 1
            elif colour == YELLO:
                yellow_char_dict[char].add(index)
                repeated_char_dict[char] += 1
            elif colour == GREYY:
                grey_char.append((char, index))
                grey_char_set.add(char)
        # find repeated but valid values
        for char in repeated_char_dict:
            if repeated_char_dict[char] > 1:
                repeated_char_set.add(char)
        repeated_char_dict.clear()
        # find all indexes of characters that exist in both yellow and grey lists
    for char, index in grey_char:
        if char in yellow_char_dict:
            yellow_char_dict[char].add(index)

    # assign valid yellow characters to guess_string_list
    for char in random.sample(list(yellow_char_dict), k=len(yellow_char_dict)):
        if char not in guess_string_list or char not in grey_char_set:
            for i in range(len(guess_string_list)):
                if guess_string_list[i] == BLANK and i not \
                        in yellow_char_dict[char]:
                    guess_string_list[i] = char
                    break

    # eliminate grey characters from ALL_CHOICES_SET
    value_choice = ALL_CHOICES_SET - grey_char_set
    # fill the remaining BLANK in guess_string_list with value_choice
    if not value_choice or BLANK not in guess_string_list:
        pass
    else:
        guess_string_list = fill_guess_list(value_choice, guess_string_list)
        # further fill the remaining BLANK with values from repeated_char_list
    if not repeated_char_set or BLANK not in guess_string_list:
        pass
    else:
        guess_string_list = fill_guess_list(repeated_char_set,
                                            guess_string_list)
    return ''.join(guess_string_list)


def fill_guess_list(values_set, guess_string_list):
    '''
    Takes values_set that stores valid values and
    guess_string_list that stores potential values to create the final guess.
    Replaces empty ' ' in guess_string_list with valid values from values_set.
    Return a new guess_string_list.
    '''
    for i in range(len(guess_string_list)):
        if guess_string_list[i] == BLANK:
            guess_string_list[i] = random.choice(''.join(values_set))
    return guess_string_list


def general_guess(difficulty):
    secret_string = get_string(difficulty)
    while eval(secret_string) <= 0 or len(secret_string) + \
            len(str(eval(secret_string))) + 1 != difficulty:
        secret_string = get_string(difficulty)
    else:
        return secret_string + EQUALITY + str(eval(secret_string))


def get_string(difficulty):
    '''
    When called, it will generate a random string that contains num1 +
    operator1 + num2 + operator2 + num3. The operator(s) could be +, -, %, *.
    The numbers are between 1 and 99. Then, it will return that random string.
    '''
    if difficulty in (7, 8):
        min_value, max_value = 1, 9
    elif 12 <= difficulty <= 15:
        min_value, max_value = 10, MAX_VALUE
    else:
        min_value, max_value = 1, MAX_VALUE

    num1, num2, num3 = random.sample(range(min_value, max_value), k=3)
    operator1, operator2 = random.choices(OPERATORS, k=2)

    return str(num1) + operator1 + str(num2) + operator2 + str(num3)

##############################################################################################
def all_green(info):
    return all(color == GREEN for _, _, color in info)

def solve_FoCdle(secret):
    '''
    For a given `secret` equation, play out a game of FoCdle, returning a tuple
    of the number of guesses required to find the secret, and the secret itself.
    Note that we aren't allowed to look at the value of `secret` directly -- it
    is only taken as a parameter for the sake of `set_colors()`, and to infer
    the respective difficulty. Most importantly, `create_guess()` cannot see it!
    '''
    difficulty = len(secret)

    # each element of 'all_info' will be a list of tuples returned by
    # 'set_colors', the function you wrote in task 2
    all_info = []
    nguesses = 0

    while True:
        gcount = 0

        # iterate a controlled number of times to try and find a guess that
        # complies with the information that has been built up
        while True:
            new_guess = create_guess(all_info, difficulty)
            if passes_restrictions(new_guess, all_info):
                break
            gcount += 1
            if gcount > GCOUNT_MAX:
                break

        # apply that latest guess
        new_info = set_colors(secret, new_guess)
        nguesses += 1
        if all_green(new_info):
            return (nguesses, new_guess)
        else:
            # didn't hit the solution, but get additional
            # information to use when generating next candidate
            all_info.append(new_info)

# finally we're ready to play a game of FoCdle...
nguesses, final_guess = solve_FoCdle(create_secret(difficulty=DEF_DIFFIC))

# and print out the results
print(f"Solved the FoCdle after {nguesses} guesses: '{final_guess}'")
