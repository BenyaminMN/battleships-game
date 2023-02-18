import random


ROWS = 5
COLUMNS = 5
SEA = " "
SUBSEAINE = "S"  # Occupies one cell
DESTROYER = "D"  # Occupies two cells
VERTICAL_DESTROYER = "A"  # Occupies two cells
FAILED_SHOT = "-"
SUCCESSFUL_SHOT = "*"
INITIAL_SHOTS = 10
QUANTITY_STARTING_SHIPS = 8
PLAYER_1 = "P1"
PLAYER_2 = "P2"


def get_initial_array():
    array = []
    for y in range(ROWS):
        # We add an array to the array, which would basically be a row
        array.append([])
        for x in range(COLUMNS):
            # And then we add a cell to that row. By default it has "SEA"
            array[y].append(SEA)
    return array


def increase_letter(letter):
    return chr(ord(letter)+1)


def print_horizontal_separator():
    # Print a line depending on the COLUMNS
    for _ in range(COLUMNS+1):
        print("+---", end="")
    print("+")


def print_row_of_numbers():
    print("|   ", end="")
    for x in range(COLUMNS):
        print(f"| {x+1} ", end="")
    print("|")


# Indicates if a coordinate in the array is empty
def its_sea(x, y, array):
    return array[y][x] == SEA


def coordinate_in_range(x, y):
    return x >= 0 and x <= COLUMNS-1 and y >= 0 and y <= ROWS-1


def place_and_print_ships(array, quantity_ships, player):
    # We divide and round down to an integer 
    # (since we cannot place a non-integer part of a ship)
    one_cell_ships = quantity_ships//2
    two_cell_vertical_ships = quantity_ships//4
    two_cell_horizontal_ships = quantity_ships//4
    if player == PLAYER_1:
        print("Printing ships of player 1 ")
    else:
        print("Printing ships of player 2 ")
    print(f"Ships of one cell: {one_cell_ships}\nVertical ships of two cells: {two_cell_vertical_ships}\nHorizontal ships of two cells: {two_cell_horizontal_ships}\nTotal: {one_cell_ships+two_cell_vertical_ships+two_cell_horizontal_ships}")
    # First we place the ones with two cells so that they fit well
    array = place_two_cell_horizontal_ships(
        two_cell_horizontal_ships, DESTROYER, array)
    array = place_two_cell_vertical_ships(
        two_cell_vertical_ships, VERTICAL_DESTROYER, array)
    array = place_one_cell_ships(one_cell_ships, SUBSEAINE, array)
    return array


def get_x_random():
    return random.randint(0, COLUMNS-1)


def get_y_random():
    return random.randint(0, ROWS-1)


def place_one_cell_ships(quantity, type_ships, array):
    located_ships = 0
    while True:
        x = get_x_random()
        y = get_y_random()
        if its_sea(x, y, array):
            array[y][x] = type_ships
            located_ships += 1
        if located_ships >= quantity:
            break
    return array


def place_two_cell_horizontal_ships(quantity, type_ships, array):
    located_ships = 0
    while True:
        x = get_x_random()
        y = get_y_random()
        x2 = x+1
        if coordinate_in_range(x, y) and coordinate_in_range(x2, y) and its_sea(x, y, array) and its_sea(x2, y, array):
            array[y][x] = type_ships
            array[y][x2] = type_ships
            located_ships += 1
        if located_ships >= quantity:
            break
    return array


def place_two_cell_vertical_ships(quantity, type_ships, array):
    located_ships = 0
    while True:
        x = get_x_random()
        y = get_y_random()
        y2 = y+1
        if coordinate_in_range(x, y) and coordinate_in_range(x, y2) and its_sea(x, y, array) and its_sea(x, y2, array):
            array[y][x] = type_ships
            array[y2][x] = type_ships
            located_ships += 1
        if located_ships >= quantity:
            break
    return array


def print_shots_left(remaining_shots, player):
    print(f"Remaining shots of {player}: {remaining_shots}")


def print_array(array, should_show_ships, player):
    print(f"This is the sea of player {player}: ")
    letter = "A"
    for y in range(ROWS):
        print_horizontal_separator()
        print(f"| {letter} ", end="")
        for x in range(COLUMNS):
            cell = array[y][x]
            real_value = cell
            if not should_show_ships and real_value != SEA and real_value != FAILED_SHOT and real_value != SUCCESSFUL_SHOT:
                real_value = " "
            print(f"| {real_value} ", end="")
        letter = increase_letter(letter)
        print("|",)  # Line break
    print_horizontal_separator()
    print_row_of_numbers()
    print_horizontal_separator()


def request_coordinates(player):
    print(f"Requesting shot coordinates to the player {player}")
    # Infinite loop. It breaks when you enter a correct row
    y = None
    x = None
    while True:
        letter_row = input(
            "Enter the row letter as it appears on the board: ")
        # We need a letter of 1 character. 
        # If it is not 1 character we use continue to repeat this cycle
        if len(letter_row) != 1:
            print("You must enter only one letter")
            continue
        # Convert letter to an index to access array
        y = ord(letter_row) - 65
        # Check if it is valid. In case it is, we break the cycle
        if coordinate_in_range(0, y):
            break
        else:
            print("Invalid row")
    # We do the same but for the column
    while True:
        try:
            x = int(input("Enter the column number: "))
            if coordinate_in_range(x-1, 0):
                x = x-1  # We want the index, so we always subtract a 1
                break
            else:
                print("Invalid column")
        except:
            print("Please enter a valid number")

    return x, y


def shoot(x, y, array) -> bool:
    if its_sea(x, y, array):
        array[y][x] = FAILED_SHOT
        return False
    # If already fired before, it still counts as a miss.
    elif array[y][x] == FAILED_SHOT or array[y][x] == SUCCESSFUL_SHOT:
        return False
    else:
        array[y][x] = SUCCESSFUL_SHOT
        return True


def opponent_of_player(player):
    if player == PLAYER_1:
        return PLAYER_2
    else:
        return PLAYER_1


def all_sunk_ships(array):
    for y in range(ROWS):
        for x in range(COLUMNS):
            cell = array[y][x]
            # If it is not sea or a shot, 
            # it means there's still a ship out there
            if cell != SEA and cell != SUCCESSFUL_SHOT and cell != FAILED_SHOT:
                return False
    # We just looped through the entire array and didn't return to the previous line. So all the ships have been sunk
    return True


def show_win(player):
    print(f"End of the game\nPlayer {player} is the winner")


def show_loose(player):
    print(
        f"End of the game\nPlayer {player} looses. Your shots have run out")


def print_ships_with_arrays(array_p1, array_p2):
    print("Showing location of the ships of both players:")
    print_array(array_p1, True, PLAYER_1)
    print_array(array_p2, True, PLAYER_2)


def play():
    remaining_shots_p1 = INITIAL_SHOTS
    remaining_shots_p2 = INITIAL_SHOTS
    quantity_ships = 5
    array_p1, array_p2 = get_initial_array(), get_initial_array()
    array_p1 = place_and_print_ships(
        array_p1, quantity_ships, PLAYER_1)
    array_p2 = place_and_print_ships(
        array_p2, quantity_ships, PLAYER_2)
    current_turn = PLAYER_1
    print("===============")
    while True:
        print(f"Turn of {current_turn}")
        remaining_shots = remaining_shots_p2
        if current_turn == PLAYER_1:
            remaining_shots = remaining_shots_p1
        print_shots_left(remaining_shots, current_turn)
        opponent_array = array_p1
        if current_turn == PLAYER_1:
            opponent_array = array_p2
        print_array(opponent_array, False,
                    opponent_of_player(current_turn))
        x, y = request_coordinates(current_turn)
        correct = shoot(x, y, opponent_array)
        if current_turn == PLAYER_1:
            remaining_shots_p1 -= 1
        else:
            remaining_shots_p2 -= 1

        print_array(opponent_array, False,
                    opponent_of_player(current_turn))
        if correct:
            print("Correct shot")
            if all_sunk_ships(opponent_array):
                show_win(current_turn)
                print_ships_with_arrays(array_p1, array_p2)
                break
        else:
            print("Missed shot")
            if remaining_shots-1 <= 0:
                show_loose(current_turn)
                print_ships_with_arrays(array_p1, array_p2)
                break
            current_turn = opponent_of_player(current_turn)


def about_us():
    print("Programmed by Benyamin Montoro")


def show_menu():
    choice = ""
    while choice != "3":
        menu = """
1. Play
2. About Us
3. Exit
Choose: """
        choice = input(menu)
        if choice == "1":
            play()
        elif choice == "2":
            about_us()


show_menu()