#this app is written with vim
#please make sure to not touch the mouse!!

import random
import keyboard
import pynput
from pynput.keyboard import Key, Listener
import os
COLS = 20
ROWS = 20
TREES_NUM = 5
board = [[' ' for j in range(COLS)] for i in range(ROWS)]
pg = [1, 1]
inv = {new_list: [] for new_list in range(0)}
inv["wood"] = 5
inv["water"] = 10
wood = 0
seed = 0
trees = []
hoed_zones = []
tree = [u'\u2588', u'\u2551'] 
a = "ciao" 

def initialize_board(board):
    board[pg[1]][pg[0]] = u'\u2593' 
    for i in range(COLS):
        for j in range(ROWS):
            if i == 0:
                if j == 0:
                    board[i][j] = u'\u2554' 
                elif j == COLS-1:
                    board[i][j] = u'\u2557'
                else:
                    board[i][j] = u'\u2550'

            elif i < ROWS-1:
                if j == 0:
                    board[i][j] = u'\u2551'
                elif j == COLS-1:
                    board[i][j] = u'\u2551'

            elif i == ROWS-1:
                if j == 0:
                    board[i][j] = u'\u255a'
                elif j == COLS-1:
                    board[i][j] = u'\u255d'
                else:
                    board[i][j] = u'\u2550'
   
    for i in range(TREES_NUM):
        
        global a
        
        tree_xpos = random.randint(2, COLS-3)
        tree_ypos = random.randint(2, ROWS-3)
        
        ok = False
        ok_counter = 0

        loop_counter = 0

        if len(trees) >= 1:
            while(not ok):
                ok_counter = 0

                tree_ypos = random.randint(2, ROWS-3)
                tree_xpos = random.randint(2, COLS-3)
                for t in trees:
                    if abs(tree_xpos - t[0]) < 2 or abs(tree_ypos - t[1]) < 2:
                        tree_ypos = random.randint(2, ROWS-3)
                        tree_xpos = random.randint(2, COLS-3)
                        #print(str(tree_xpos) + " " + str(tree_ypos))
                        ok_counter += 1
                        a = "collisione"
                        break
                
                if ok_counter == 0:
                    ok = True
        
        trees.append([tree_xpos, tree_ypos])
        loop_counter += 1

def print_board():
    
    board = [[' ' for j in range(COLS)] for i in range(ROWS)]
    board[pg[1]][pg[0]] = u'\u2524' 
    
    for i in range(len(trees)):
        board[trees[i][1]][trees[i][0]] = tree[0]
        board[trees[i][1]-1][trees[i][0]] = tree[0]
        board[trees[i][1]][trees[i][0]-1] = tree[0]
        board[trees[i][1]][trees[i][0]+1] = tree[0]
        board[trees[i][1]+1][trees[i][0]] = tree[1]
    
    #hoed
    for h in hoed_zones:
        if h[2] == 0:
            board[h[1]][h[0]] = u'\u2591'
        if h[2] == 1:
            board[h[1]][h[0]] = u'\u2592'
        if h[2] == 2:
            board[h[1]][h[0]] = u'\u2593'

    for i in range(COLS):
        for j in range(ROWS):
            if i == 0:
                if j == 0:
                    board[i][j] = u'\u2554' 
                elif j == COLS-1:
                    board[i][j] = u'\u2557'
                else:
                    board[i][j] = u'\u2550'

            elif i < ROWS-1:
                if j == 0:
                    board[i][j] = u'\u2551'
                elif j == COLS-1:
                    board[i][j] = u'\u2551'

            elif i == ROWS-1:
                if j == 0:
                    board[i][j] = u'\u255a'
                elif j == COLS-1:
                    board[i][j] = u'\u255d'
                else:
                    board[i][j] = u'\u2550'

    for i in range(ROWS):
        for j in range(COLS):
            offset = (u'\u2550' if (i == 0 or i == ROWS-1) and j < COLS-1 else " ")
            
            #trees
            if board[i][j] == u'\u2588':
                offset = u'\u2588'
            if board[i][j] == u'\u2551' and (j != 0 and j != COLS-1):
                offset = u'\u2551'
            
            #pg
            if board[i][j] == u'\u2524':
                offset = u'\u251C'

            #hoe
            if board[i][j] == u'\u2591' or board[i][j] == u'\u2592' or board[i][j] == u'\u2593':
                offset = board[i][j]


            print(board[i][j] + offset, end ="")
            if j == COLS-1:
                print("\n", end="")
   
    tabulation_1 = "\t\t\t"
    tabulation_2 = "\t\t\t"

    hoeble = True
    waterable = False

    for t in trees:
        if abs(pg[0] - t[0]) <= 2 and abs(pg[1] - t[1]) <= 2:
            print("cut tree [C]", end = "")
            tabulation_1 = "\t\t"
            break

    for t in trees:
       if abs(pg[0] - t[0]) <= 2 and abs(pg[1] - t[1]) <= 2:
           hoeble = False
           break 

    for h in hoed_zones:
        if pg[0] == h[0] and pg[1] == h[1]:
            waterable = True
            break
    
    print(tabulation_1 + "INVENTORY:")
    if hoeble:
        print("hoe [H]", end = "")
        tabulation_2 =  "\t\t\t"
    index = 0
    for key, value in inv.items():
        if(index == 0):
            print (tabulation_2 + key + ": " + str(value))
        elif(waterable and index == 1):
            print("water [R]", end = "")
            print ("\t\t" + key + ": " + str(value))
        else:
            print ("\t\t\t" + key + ": " + str(value))
        index+=1
    
def add_to_inv(element, qty):
    global inv 
    if element not in inv.keys():
        inv[element] = qty
    else:
        inv[element] += qty

def remove_from_inv(element, qty):
    global inv
    inv[element] -= 1
    if inv[element] == 0:
        del inv[element]
        
def on_press(key):
    global keys, count, a, wood, seed, inv
    pre_ypos = pg[1]
    pre_xpos = pg[0]
    try:
        if key.char == 'w':
            if board[pg[1]-1][pg[0]] == ' ':
                pg[1] -= 1
        elif key.char == 's':
            if board[pg[1]+1][pg[0]] == ' ':
                pg[1] += 1
        elif key.char == 'a':
            if board[pg[1]][pg[0]-1] == ' ':
                pg[0] -= 1
        elif key.char == 'd':
            if board[pg[1]][pg[0]+1] == ' ':
                print(board[pg[1]][pg[0]+1])
                pg[0] += 1
        elif key.char == 'c':
            index = 0
            ok = False
            for t in trees:
                if abs(pg[0] - t[0]) <= 2 and abs(pg[1] - t[1]) <= 2:
                    ok = True
                    break
                index += 1

            if ok:
                trees.pop(index)
                add_to_inv("wood", 5)
                add_to_inv("seed", 1)
        
        elif key.char == 'h':
            seed_needed = 1
            if "seed" in inv.keys():
                if inv["seed"] - seed_needed >= 0:
                    hoed_zones.append([pg[0], pg[1], 0])
                    remove_from_inv("seed", 1)
        elif key.char == 'r':
            water_needed = 1
            if "water" in inv.keys():
                if inv["water"] - water_needed >= 0:
                    for h in hoed_zones:
                        if pg[0] == h[0] and pg[1] == h[1]:
                            if h[2] == 2:
                                trees.append([h[0], h[1]])
                            h[2] += 1
                            break
                    remove_from_inv("water", 1)

    except Exception as e: 
        print(e)
        #input("e mo?")

    os.system("cls")
    board[pre_ypos][pre_xpos] = ' '
    print_board()

def on_realease(key):
    if key == Key.esc:
        return False

def main():
    os.system("cls")
    initialize_board(board)
    print_board()

if __name__ == "__main__":
    main()
    with Listener (on_press=on_press, on_release=on_realease) as listener:
        listener.join()
