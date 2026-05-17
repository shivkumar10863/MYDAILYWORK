import math
import streamlit as st
# Create board by list and list have empty space
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
board = st.session_state.board
si=sig=None
player_moved=False
# This method is for check who is the winner
def check_winner(player):
    flag=False
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diagonals
    ]

    for condi in win_conditions:
        for i in condi:
            if board[i] == player:
                flag=True
            else:                
                flag=False
                break
        if flag:
            return True
    return False

# this method for check the draw
def is_draw():
    return " " not in board

# We get all available moves in a list
def available_moves():
    return [i for i, spot in enumerate(board) if spot == " "]

# this method for check the Minimax algorithm
def minimax(is_maximizing):
    if check_winner(si):  # Check AI is winner
        return 1
    if check_winner(sig):  # Check Human is winner
        return -1
    if is_draw(): # Check the match is draw
        return 0
    if is_maximizing:
        best_score=-math.inf
        for move in available_moves():
            board[move]=si
            score=minimax(False)
            board[move]=" "
            best_score=max(score,best_score)
        return best_score
    else:
        best_score=math.inf
        for move in available_moves():
            board[move]=sig
            score=minimax(True)
            board[move]=" "
            best_score=min(score,best_score)
        return best_score
# This method is for AI move
def ai_move():
    best_score = -math.inf
    best_move = None
    for move in available_moves():
        board[move] = si
        score = minimax(False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    if best_move is not None:
        board[best_move]=si
# Main game loop starts here
st.title("Tic Tac Toe Game")
if "sig" not in st.session_state:
    st.session_state.sig="X"
sig=st.selectbox(
    "Select your sign",
    ["X","O"],
    index=["X","O"].index(st.session_state.sig)
)
st.session_state.sig=sig
if sig=="X":
    si="O"
else:
    si="X"
# This method is for Human move
col1,col2,col3 = st.columns(3)
with col1:
    if st.button(board[0],key=0):
        if board[0]==" ":
            board[0]=sig
            player_moved=True
    if st.button(board[3],key=3):
        if board[3]==" ":
            board[3]=sig
            player_moved=True
    if st.button(board[6],key=6):
        if board[6]==" ":
            board[6]=sig
            player_moved=True
with col2:
    if st.button(board[1],key=1):
        if board[1]==" ":
            board[1]=sig
            player_moved=True
    if st.button(board[4],key=4):
        if board[4]==" ":
            board[4]=sig
            player_moved=True
    if st.button(board[7],key=7):
        if board[7]==" ":
            board[7]=sig
            player_moved=True
with col3:
    if st.button(board[2],key=2):
        if board[2]==" ":
            board[2]=sig
            player_moved=True
    if st.button(board[5],key=5):
        if board[5]==" ":
            board[5]=sig
            player_moved=True
    if st.button(board[8],key=8):
        if board[8]==" ":
            board[8]=sig
            player_moved=True
if check_winner(sig):
    st.success("You win!")
elif check_winner(si):
    st.success("AI win!")
elif is_draw():
    st.info("It's a draw!")
elif player_moved:
    ai_move()
    st.rerun()