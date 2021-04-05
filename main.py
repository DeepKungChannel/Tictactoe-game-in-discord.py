import random
import discord
from discord.ext import commands,tasks

PREFIX = "<"#Change your prefix here
TOKEN = "---Your bot token---"#Paste your token here

client = commands.Bot(command_prefix=PREFIX)


board = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

gameOver = True
player1 = ''
player2 = ''
turn = ''
numturn = 0

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def tictactoe(ctx,p1:discord.Member,p2:discord.Member):
    global gameOver
    global turn
    global numturn
    global player1
    global player2
    player1 = p1
    player2 = p2
    if gameOver:
        global board
        await ctx.send(render(board))
        num = random.randint(1,2)
        if num == 1:
            turn = player1
            numturn = 1
        elif num == 2:
            turn = player2
            numturn = 2
        await ctx.send("{} Turn!".format(turn.name))
        gameOver = False
    else:
        await ctx.send("Please try again later, system is error.")

@client.command(aliases=['p'])
async def place(ctx,num:int):
    global gameOver
    global turn
    global numturn
    global player1
    global player2
    if not gameOver:
        global board
        if turn == ctx.author:
            if num >= 1 and num <= 3:
                if board[0][num-1] != 0:
                    await ctx.send("Can't place.")
                    return
                else:
                    board[0][num-1] = numturn
            if num >= 4 and num <= 6:
                if board[1][num-4] != 0:
                    await ctx.send("Can't place.")
                    return
                else:
                    board[1][num-4] = numturn
            if num >= 7 and num <= 9:
                if board[2][num-7] != 0:
                    await ctx.send("Can't place.")
                    return
                else:
                    board[2][num-7] = numturn
            win,winpeople = windetect(board)
            tie = tiedetect(board)
            if tie:
                await ctx.send(render(board))
                await ctx.send("Game Over!")
                await ctx.send("Tie!")
                return True
            if win:
                await ctx.send(render(board))
                await ctx.send("Game Over!")
                await ctx.send("{} Win!".format(winpeople.name))
                gameOver = True
                return True
            await ctx.send(render(board))
            if turn == player1:
                turn = player2
                numturn = 2
            elif turn == player2:
                turn = player1
                numturn = 1
            await ctx.send("{} Turn!".format(turn.name))
            return False
        else:
            await ctx.send("It's not your turn!")
    else:
        await ctx.send("Please start the game.")

def tiedetect(board):
    tie = []
    if board != [[0,0,0],[0,0,0],[0,0,0]]:
        for x in board:
            for y in x:
                if y == 0:
                    return False
    return True

def windetect(board):
    j = 0
    global numturn
    global turn
    #check |
    for i in range(3):
        if board[i][j] == numturn and board[i][j+1] == numturn and board[i][j+2] == numturn:
            return True,turn
    
    #check -
    for i in range(3):
        if board[j][i] == numturn and board[j+1][i] == numturn and board[j+2][i] == numturn:
            return True,turn

    #check /
    if board[0][2] == numturn and board[1][1] == numturn and board[2][0] == numturn:
        return True,turn
    
    #check \
    if board[0][0] == numturn and board[1][1] == numturn and board[2][2] == numturn:
        return True,turn
    
    return False,''

def render(board):
    line = ''
    for i in board:
        for y in i:
            if y == 0:
                line += ('#' + ' ')
            elif y == 1:
                line += ('O'+' ')
            elif y == 2:
                line += ("X"+ ' ')
        line += '\n'
    return line


@client.command()
async def stop(ctx):
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send('Game is stop.')
    else:
        await ctx.send("Game has stopped.")

client.run(TOKEN)