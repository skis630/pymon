from backend import utils
from backend import db

def createGame(name, creator):
    sequence = utils.generateSequence()
    db.newGame(name, creator, sequence)

def createPlayer(name, avatar):
    db.newPlayer(name, avatar)

def gameExists(game_id):
    return db.getGame(game_id)

def listGames():
    return db.getAllGames()

def deleteGame(game_id):
    db.deleteGamePlayers(game_id)
    db.deleteGame(game_id)

def joinGame(game_id, player_id):
    currentGame = db.getGame(game_id)
    players = db.getGamePlayers(game_id)
    if players and len(players) == 4:
        print("change status")       
        db.updateGameStatus(game_id, "full")
    if currentGame['status'] == "open":
        return db.joinGame(game_id, player_id)
    return False

def getTopplayers():
    return db.getTopScores()

def generateGameStatus(game_id, player_id):
    currentPlayer = {"name":player_id}
    currentGame = db.getGame(game_id)
    currentGame["sequence"] = currentGame["sequence"].split(",")
    gamePlayers = db.getGamePlayers(game_id)
    gamePlayersV2 = db.getGamePlayersV2(game_id)
    # num_of_players = len(gamePlayers)
    # if num_of_players > 1:
    #     gamePlayersIds = tuple([player["player"] for player in gamePlayers])
    #     print(gamePlayersIds)
    #     gameAvatars = db.getGameAvatars(gamePlayersIds)
    #     for i in range(num_of_players):
    #         gamePlayers[i]["avatar"] = gameAvatars[i]["avatar"]

    # elif num_of_players == 1:
    #     gamePlayersIds = gamePlayers[0]["player"]
    #     gameAvatars = db.getFirstAvatar(gamePlayersIds)
    #     gamePlayers[0]["avatar"] = gameAvatars["avatar"]
   
    currentPlayer["status"] = "viewer"
    for p in gamePlayersV2:
        if p["player"] == player_id:
            currentPlayer["status"] = p["status"]
            break
    return {"game":currentGame,"players":gamePlayersV2, "user":currentPlayer}

def playTurn(game_id, player_id, color):
    currentGame = db.getGame(game_id)
    if currentGame:
        correct = checkTurn(currentGame, color)
        if correct:
            newStep = currentGame["step"] + 1
            if newStep == utils.GAME_LENGTH:
                win(game_id, newStep)
            else:
                correctTurn(game_id, player_id, newStep)
        else:
            wrongTurn(game_id, player_id)
        return True
    return False

def checkTurn(game, color):
    sequence = game["sequence"].split(",")
    step = game["step"]
    return color == sequence[step]



def markPlayerReady(game_id, player_id):
    currentGame = db.getGame(game_id)
    if currentGame:
        db.updatePlayerStatus(game_id, player_id, "ready")
        gamePlayers = db.getGamePlayers(game_id)
        readyPlayers = db.getReadyPlayers(game_id)
        if gamePlayers == readyPlayers:
            db.updateGameStatus(game_id, "on")
            db.setFirstTurn(game_id)
        return True
    return False

def correctTurn(game_id, player_id, newStep):
    db.updateGameStep(game_id, newStep)
    db.updatePlayerStatus(game_id, player_id, "ready")
    nextPlayer = db.getNextPlayer(game_id, player_id)
    return db.updatePlayerStatus(game_id, nextPlayer, "turn")

def wrongTurn(game_id, player_id):
    db.updatePlayerStatus(game_id, player_id, "failed")
    nextPlayer = db.getNextPlayer(game_id, player_id)
    if not nextPlayer:
        return db.updateGameStatus(game_id, "failed")
    return db.updatePlayerStatus(game_id, nextPlayer, "turn")

def win(game_id, newStep):
    db.updateGameStatusAndStep(game_id, "won", newStep)
    return db.updateWonPlayers(game_id)