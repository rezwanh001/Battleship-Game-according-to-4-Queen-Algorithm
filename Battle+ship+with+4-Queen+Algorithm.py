
# coding: utf-8

# # AI GAME (Battle-ship with 4-Queen Algorithm)

# In[5]:


import copy, random
import sys
import itertools

computer_score = 0
user_score = 0
player = 0

case1,case2 = [], []
cnt1 = 0
cnt2 = 1
finalCase = []
visited = [[True]*4]*4

def print_board(s,board):

    #find out if you are printing the computer or user board
    player = "Computer"
    if s == "u":
        player = "User"

    print ("The " + player + "'s board look like this: \n")

    #print the horizontal numbers
    print (" ",end="")
    for i in range(4):
        print ("  " + str(i+1) + "  ",end="")
    print ("\n")

    for i in range(4):
        print (str(i+1) + " ",end="")

        for j in range(4):
            if board[i][j] == -1:
                print (' ',end="")
            elif s == "u":
                print (board[i][j],end="")
            elif s == "c":
                if board[i][j] == "*" or board[i][j] == "$":
                    print (board[i][j],end="")
                else:
                    print (" ",end="")


            print (" | ",end=" ")
        print()
        
        print (" --------------------")

            
def user_place_ships(board,ships):

    for ship in ships.keys():

        #get coordinates from user and vlidate the postion
        valid = False
        while(not valid):

            print_board("u",board)
            print ("Placing  " + ship)
            x,y = get_coor()
            ori = v_or_h()
            valid = validate(board,ships[ship],x,y,ori)
            if not valid:
                print ("Cannot place a ship there.\nPlease take a look at the board and try again.")
                input("Hit ENTER to continue")

        #place the ship
        board = place_ship(board,ships[ship],ship[0],ori,x,y)
        print_board("u",board)

    input("Done placing user ships. Hit ENTER to continue")
    return board


# Apply N-Quueen for placing ships into the grid
def queens ():
    for p in itertools.permutations (range (4) ):
        yield [x for x in enumerate (p) ]
        
        
def computer_place_ships(board,ships):
    o = random.randint(0,1)
    x, y = 0, 0
    positions = []
    pos = []
    for q in queens ():
        err = False
        for a, b in ( (a, b) for a in q for b in q if a [0] < b [0] ):
            if abs (a [0] - b [0] ) == abs (a [1] - b [1] ):
                err = True
                break
        if not err:
            positions.append(q)


    for i in positions[o]:
        k = ','.join(str(e) for e in i)

        a, b = k.split(",")
        pos.append(int(a))
        pos.append(int(b))
    
    k = 0
    m = 1
    
    for ship in ships.keys():
        valid = False
        while(not valid):
                
            x = pos[k] 
            y = pos[m] 
            k += 2
            m += 2

            ori = "v"
            valid = validate(board,ships[ship],x,y,ori)

        #place the ship
        print ("Computer placing  " + ship)
        board = place_ship(board,ships[ship],ship[0],ori,x,y)

    return board

#place ship based on orientation
def place_ship(board,ship,s,ori,x,y):

    if ori == "v":
        for i in range(ship):
            board[x+i][y] = s
    elif ori == "h":
        for i in range(ship):
            board[x][y+i] = s

    return board


#validate the ship can be placed at given coordinates
def validate(board,ship,x,y,ori):

    if ori == "v" and x+ship > 4:
        return False
    elif ori == "h" and y+ship > 4:
        return False
    else:
        if ori == "v":
            for i in range(ship):
                if board[x+i][y] != -1:
                    return False
        elif ori == "h":
            for i in range(ship):
                if board[x][y+i] != -1:
                    return False

    return True

#get ship orientation from user
def v_or_h():

    while(True):
        user_input = "v" #input("vertical or horizontal (v,h) ? ")
        if user_input == "v" or user_input == "h":
            return user_input
        else:
            print ("Invalid input. Please only enter v or h")
            


            

def get_coor():

    while (True):
        user_input = input("Please User enter coordinates (row,col) ? ")
        try:
            #see that user entered 2 values seprated by comma
            coor = user_input.split(",")
            if len(coor) != 2:
                raise Exception("Invalid entry, too few/many coordinates.")

            #check that 2 values are integers
            coor[0] = int(coor[0])-1
            coor[1] = int(coor[1])-1

            #check that values of integers are between 1 and 5 for both coordinates
            if coor[0] > 3 or coor[0] < 0 or coor[1] > 3 or coor[1] < 0:
                raise Exception("Invalid entry. Please use values between 1 to 4 only.")

            #if everything is ok, return coordinates
            return coor

        except ValueError:
            print ("Invalid entry. Please enter only numeric values for coordinates")
        except Exception as e:
            print (e)
            
#make a move on the board and return the result, hit, miss or try again for repeat hit           
def make_move(board,x,y):
    if board[x][y] == -1:
        return "miss"
    elif board[x][y] == '*' or board[x][y] == '$':
        return "try again"
    else:
        return "hit"
    
# User try with co-ordinate    
def user_move(board):
    global user_score;
    #get coordinates from the user and try to make move
    #if move is a hit, check ship sunk and win condition
    while(True):
        x,y = get_coor()
        res = make_move(board,x,y)
        if res == "hit":
            print ("Hit at " + str(x+1) + "," + str(y+1)); user_score += 1;
            check_sink(board,x,y)
            board[x][y] = '$'
            if check_win(board):
                return "WIN"
        elif res == "miss":
            print ("Sorry USER, " + str(x+1) + "," + str(y+1) + " is a miss.")
            board[x][y] = "*"
        elif res == "try again":
            print ("Sorry, that coordinate was already hit. Please try again")	

        if res != "try again":
            return board
        

## Store co-ordinate value using N-Queens
def store_value():
    ### Appply N-Queen###
    o = random.randint(0,1)
    positions = []
    
    global finalCase
    global visited
    
    for q in queens ():
        err = False
        for a, b in ( (a, b) for a in q for b in q if a [0] < b [0] ):
            if abs (a [0] - b [0] ) == abs (a [1] - b [1] ):
                err = True
                break
        if not err:
            positions.append(q)

    for i in positions[o]:
        k = ','.join(str(e) for e in i)

        a, b = k.split(",")
        case1.append(int(a))
        case1.append(int(b))
#         visited[int(a)][int(b)] = 
    #     print(a,b)

    val = 1 - o
    for i in positions[val]:
        k = ','.join(str(e) for e in i)
        a, b = k.split(",")
        case2.append(int(a))
        case2.append(int(b))
    #     print(a,b)
    
    finalCase = case1 + case2
    a = 0
    b = 1
    for i in range(len(finalCase)//2):
        x = finalCase[a]
        y = finalCase[b]
        a += 2
        b += 2
        visited[x][y] = False
#         print(x, y)
        
     
    #print(visited)
    
    for i in range(4):
        for j in range(4):
            if visited[i][j] == False:
                finalCase.append(i)
                finalCase.append(j)
#                 print(finalCase)
#                 visited[i][j] = True
#     print(visited)
#     print(finalCase)   

def computer_move(board):
    global computer_score;
    #generate user coordinates from the user and try to make move
    #if move is a hit, check ship sunk and win condition
    
    global cnt1
    global cnt2
    
    k = 0
#     print(finalCase)
    
    while(True):
        x = finalCase[cnt1] 
        y = finalCase[cnt2] 
        cnt1 += 2
        cnt2 += 2
#         print("X, Y: " + str(x) + " , " +str(y))
        res = make_move(board,x,y)
        if res == "hit":
            print ("Hit at " + str(x+1) + "," + str(y+1)); computer_score += 1;
            check_sink(board,x,y)
            board[x][y] = '$'
            if check_win(board):
                return "WIN"
        elif res == "miss":
            print ("Sorry COMPUTER, " + str(x+1) + "," + str(y+1) + " is a miss.")
            board[x][y] = "*"

        if res != "try again":

            return board
        
#figure out what ship was hit
def check_sink(board,x,y):
    if board[x][y] == "B":
        ship = "Battleship"
    elif board[x][y] == "S":
        ship = "Submarine" 
    elif board[x][y] == "D":
        ship = "Destroyer"
    elif board[x][y] == "P": 
        ship = "Patrol Boat"

    #mark cell as hit and check if sunk
    board[-1][ship] -= 1
    if board[-1][ship] == 0:
        print (ship + " Sunk")
        

def check_win(board):
    #simple for loop to check all cells in 2d board
    #if any cell contains a char that is not a hit or a miss return false
    for i in range(4):
        for j in range(4):
            if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
                return False
    return True



def main():
    #types of ships
    ships = {"Battleship":1,
             "Submarine":1,
             "Destroyer":1,
             "Patrol Boat":1}

    #setup blank 4x4 board
    board = []
    for i in range(4):
        board_row = []
        for j in range(4):
            board_row.append(-1)
        board.append(board_row)

    #setup user and computer boards
    user_board = copy.deepcopy(board)
    comp_board = copy.deepcopy(board)

    #add ships as last element in the array
    user_board.append(copy.deepcopy(ships))
    comp_board.append(copy.deepcopy(ships))

    #ship placement
    user_board = user_place_ships(user_board,ships)
    comp_board = computer_place_ships(comp_board,ships)
    
    #Store co-ordinate for computer 
    store_value() 
    
    #game main loop
    while(1):
        
#         if player == 1:
        #user move
        print_board("c",comp_board)
        comp_board = user_move(comp_board)

        #check if user won
        if comp_board == "WIN":
            print("User Score : " + str(user_score) + "\n" + "Computer Score : " + str(computer_score))
            if user_score == computer_score:
                print("Play DRAW!!")
                return 0
            else:
                print ("User WON! :)")
                return 0

        #display current computer board
        print_board("c",comp_board)
        input("To end USER turn hit ENTER")
        
        #computer move
        user_board = computer_move(user_board)

        #check if computer move
        if user_board == "WIN":
            print("Computer Score: " + str(computer_score) + "\n" + "User Score : " + str(user_score))
            if user_score == computer_score:
                print("Play DRAW!!")
                return 0
            else:
                print ("Computer WON! :("); 
                return 0

        #display user board
        print_board("u",user_board)
#         input("To end COMPUTER turn hit ENTER")
        
# Main function       
if __name__=="__main__":
    main()


# In[ ]:





# In[ ]:




