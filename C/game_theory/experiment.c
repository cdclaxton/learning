#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "experiment.h"

PayoffElement *buildPayoffElement(int player1Payoff, int player2Payoff)
{
    PayoffElement *element = malloc(sizeof(PayoffElement));
    if (element == NULL)
    {
        printf("Failed to allocate space for the payoff element");
        exit(-1);
    }

    element->player1Payoff = player1Payoff;
    element->player2Payoff = player2Payoff;

    return element;
}

void printPayoffElement(PayoffElement *element)
{
    printf("Payoff: Player 1=%d, Player 2=%d", element->player1Payoff, element->player2Payoff);
}

void freePayoffElement(PayoffElement *element)
{
    free(element);
}

PayoffMatrix *buildPayoffMatrix(int bothPlayersCooperate,
                                int bothPlayersDefect,
                                int cooperateDefect,
                                int defectCooperate)
{
    PayoffMatrix *matrix = malloc(sizeof(PayoffMatrix));
    matrix->cooperateCooperate = buildPayoffElement(bothPlayersCooperate, bothPlayersCooperate);
    matrix->cooperateDefect = buildPayoffElement(cooperateDefect, defectCooperate);
    matrix->defectCooperate = buildPayoffElement(defectCooperate, cooperateDefect);
    matrix->defectDefect = buildPayoffElement(bothPlayersDefect, bothPlayersDefect);
    return matrix;
}

void freePayoffMatrix(PayoffMatrix *matrix)
{
    freePayoffElement(matrix->cooperateCooperate);
    freePayoffElement(matrix->cooperateDefect);
    freePayoffElement(matrix->defectCooperate);
    freePayoffElement(matrix->defectDefect);
    free(matrix);
}

bool payoff(int player1Decision,
            int player2Decision,
            PayoffMatrix *matrix,
            PayoffElement **result)
{
    if ((player1Decision == COOPERATE) && (player2Decision == COOPERATE))
    {
        *result = matrix->cooperateCooperate;
        return true;
    }
    else if ((player1Decision == COOPERATE) && (player2Decision == DEFECT))
    {
        *result = matrix->cooperateDefect;
        return true;
    }
    else if ((player1Decision == DEFECT) && (player2Decision == COOPERATE))
    {
        *result = matrix->defectCooperate;
        return true;
    }
    else if ((player1Decision == DEFECT) && (player2Decision == DEFECT))
    {
        *result = matrix->defectDefect;
        return true;
    }

    // One or both of the player decisions was invalid
    return false;
}

// -----------------------------------------------------------------------------
// Strategy
// -----------------------------------------------------------------------------

void freeStrategy(Strategy *strategy)
{
    free(strategy);
}

void freeStrategies(Strategy **strategies,
                    int numberOfStrategies)
{
    for (int i = 0; i < numberOfStrategies; i++)
    {
        freeStrategy(strategies[i]);
    }
}

// -----------------------------------------------------------------------------
// Strategy: Always defect
// -----------------------------------------------------------------------------

int alwaysDefectDecide(int *playerDecisions,
                       int *opponentDecisions,
                       int currentTurn)
{
    return DEFECT;
}

Strategy *newAlwaysDefectStrategy()
{
    Strategy *strategy = malloc(sizeof(Strategy));
    strategy->name = "always-defect";
    strategy->decide = alwaysDefectDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy: Always cooperate
// -----------------------------------------------------------------------------

int alwaysCooperateDecide(int *playerDecisions,
                          int *opponentDecisions,
                          int currentTurn)
{
    return COOPERATE;
}

Strategy *newAlwaysCooperateStrategy()
{
    Strategy *strategy = malloc(sizeof(Strategy));
    strategy->name = "always-cooperate";
    strategy->decide = alwaysCooperateDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy: Always defect if the opponent defects
// -----------------------------------------------------------------------------

int alwaysDefectIfOpponentDefectsDecide(int *playerDecisions,
                                        int *opponentDecisions,
                                        int currentTurn)
{
    // Cooperate on the first turn
    if (currentTurn == 0)
    {
        return COOPERATE;
    }

    // If the opponent has ever defected, then defect
    if (anyDefections(opponentDecisions, currentTurn - 1) == true)
    {
        return DEFECT;
    }

    return COOPERATE;
}

Strategy *newAlwaysDefectIfOpponentDefectsStrategy()
{
    Strategy *strategy = malloc(sizeof(Strategy));
    strategy->name = "always-defect-if-opponent-defects";
    strategy->decide = alwaysDefectIfOpponentDefectsDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy: Tit-for-tat
// -----------------------------------------------------------------------------

int titForTatDecide(int *playerDecisions,
                    int *opponentDecisions,
                    int currentTurn)
{
    // Cooperate on the first turn
    if (currentTurn == 0)
    {
        return COOPERATE;
    }

    return opponentDecisions[currentTurn - 1];
}

Strategy *newTitForTatStrategy()
{
    Strategy *strategy = malloc(sizeof(Strategy));
    strategy->name = "tit-for-tat";
    strategy->decide = titForTatDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy utility functions
// -----------------------------------------------------------------------------

bool anyDefections(int *decisions, int maxIndex)
{
    for (int i = 0; i <= maxIndex; i++)
    {
        if (decisions[i] == DEFECT)
        {
            return true;
        }
        else if (decisions[i] != COOPERATE)
        {
            printf("Invalid state encountered");
            exit(-1);
        }
    }

    return false;
}

// -----------------------------------------------------------------------------
// Game
// -----------------------------------------------------------------------------

Game *newGame(int numberOfRounds)
{
    // Check that the number of rounds is valid
    if (numberOfRounds <= 0)
    {
        printf("Invalid number of rounds: %d\n", numberOfRounds);
        exit(-1);
    }

    Game *game = malloc(sizeof(Game));
    game->numberOfRounds = numberOfRounds;
    game->numberOfRoundsPlayed = 0;
    game->player1Actions = malloc(sizeof(int) * numberOfRounds);
    game->player2Actions = malloc(sizeof(int) * numberOfRounds);

    return game;
}

void freeGame(Game *game)
{
    free(game->player1Actions);
    free(game->player2Actions);
    free(game);
}

bool isActionValid(int action)
{
    if ((action == COOPERATE) || (action == DEFECT))
    {
        return true;
    }

    return false;
}

bool updateGame(Game *game,
                int player1Action,
                int player2Action)
{
    if (game == NULL)
    {
        printf("Game is NULL\n");
        exit(-1);
    }

    if ((isActionValid(player1Action) == false) ||
        (isActionValid(player2Action) == false))
    {
        return false;
    }

    if (game->numberOfRoundsPlayed >= game->numberOfRounds)
    {
        return false;
    }

    game->player1Actions[game->numberOfRoundsPlayed] = player1Action;
    game->player2Actions[game->numberOfRoundsPlayed] = player2Action;

    game->numberOfRoundsPlayed += 1;
    return true;
}

bool scoreGame(Game *game,
               PayoffMatrix *payoffMatrix,
               int *player1Score,
               int *player2Score)
{
    if ((game == NULL) || (payoffMatrix == NULL))
    {
        return false;
    }

    // Check that the number of rounds is valid
    if (game->numberOfRoundsPlayed <= 0)
    {
        false;
    }

    // Initialise the player scores
    *player1Score = 0;
    *player2Score = 0;

    bool isValid = false;
    PayoffElement *result = NULL;

    for (int i = 0; i < game->numberOfRoundsPlayed; i++)
    {
        isValid = payoff(game->player1Actions[i],
                         game->player2Actions[i],
                         payoffMatrix,
                         &result);

        if (isValid == false)
        {
            return false;
        }

        *player1Score += result->player1Payoff;
        *player2Score += result->player2Payoff;
    }

    return true;
}

void printGame(Game *game)
{
    printf("Game:\n");
    printf("  Number of rounds: %d\n", game->numberOfRounds);
    printf("  Number of rounds played: %d\n", game->numberOfRoundsPlayed);

    printf("  Actions:\n");
    for (int i = 0; i < (game->numberOfRoundsPlayed); i++)
    {
        printf("    Player 1: %d, Player 2: %d\n",
               game->player1Actions[i],
               game->player2Actions[i]);
    }
}

bool executeGame(Game *game,
                 Strategy *player1,
                 Strategy *player2)
{
    int action1;
    int action2;
    bool result;

    for (int i = 0; i < game->numberOfRounds; i++)
    {
        // Player 1 plays first
        action1 = player1->decide(game->player1Actions,
                                  game->player2Actions,
                                  game->numberOfRoundsPlayed);

        // Player 2 plays second
        action2 = player2->decide(game->player2Actions,
                                  game->player1Actions,
                                  game->numberOfRoundsPlayed);

        // Update the game
        result = updateGame(game, action1, action2);
        if (result == false)
        {
            return false;
        }
    }
}

bool gameEquals(Game *game,
                int expectedNumberOfRounds,
                int expectedNumberOfRoundsPlayed,
                int *expectedPlayer1Actions,
                int *expectedPlayer2Actions)
{
    if (game == NULL)
    {
        return false;
    }

    if ((game->numberOfRounds != expectedNumberOfRounds) ||
        (game->numberOfRoundsPlayed != expectedNumberOfRoundsPlayed))
    {
        return false;
    }

    for (int i = 0; i < game->numberOfRoundsPlayed; i++)
    {
        if ((game->player1Actions[i] != expectedPlayer1Actions[i]) ||
            (game->player2Actions[i] != expectedPlayer2Actions[i]))
        {
            return false;
        }
    }

    return true;
}

// -----------------------------------------------------------------------------
// Tournament
// -----------------------------------------------------------------------------

Tournament *newTournament(Strategy **strategies,
                          int numberOfStrategies,
                          int numberOfRoundsPerGame)
{
    Tournament *tournament = malloc(sizeof(Tournament));
    if (tournament == NULL)
    {
        printf("Failed to allocate space for the tournament\n");
        exit(-1);
    }

    // Each strategy plays every other strategy and itself
    tournament->numberOfGames = numberOfStrategies * numberOfStrategies;

    // Allocate memory for each of the games
    tournament->games = malloc(tournament->numberOfGames * sizeof(Game *));

    // Allocate memory for each of the strategies
    tournament->player1Strategies = malloc(tournament->numberOfGames * sizeof(Strategy *));
    if (tournament->player1Strategies == NULL)
    {
        printf("Failed to allocate space for player 1 strategies\n");
        exit(-1);
    }

    tournament->player2Strategies = malloc(tournament->numberOfGames * sizeof(Strategy *));
    if (tournament->player2Strategies == NULL)
    {
        printf("Failed to allocate space for player 2 strategies\n");
        exit(-1);
    }

    // Walk through each of the games
    int gameIndex = 0;
    for (int i = 0; i < numberOfStrategies; i++)
    {
        for (int j = 0; j < numberOfStrategies; j++)
        {
            tournament->player1Strategies[gameIndex] = strategies[i];
            tournament->player2Strategies[gameIndex] = strategies[j];

            tournament->games[gameIndex] = newGame(numberOfRoundsPerGame);

            gameIndex++;
        }
    }

    return tournament;
}

void freeTournament(Tournament *tournament)
{
    free(tournament->player1Strategies);
    free(tournament->player2Strategies);

    // Free each of the games
    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        freeGame(tournament->games[i]);
    }

    // Free the array of games
    free(tournament->games);

    free(tournament);
}

void printTournament(Tournament *tournament)
{
    printf("Tournament:\n");
    printf("Number of games: %d\n", tournament->numberOfGames);

    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        printf("Strategy %s vs %s\n", tournament->player1Strategies[i]->name,
               tournament->player2Strategies[i]->name);
    }
}

void executeTournament(Tournament *tournament)
{
    if (tournament == NULL)
    {
        printf("Tournament is null");
        exit(-1);
    }

    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        executeGame(tournament->games[i],
                    tournament->player1Strategies[i],
                    tournament->player2Strategies[i]);
    }
}

TournamentScores *newTournamentScores(int numberOfGames)
{
    if (numberOfGames <= 0)
    {
        return NULL;
    }

    TournamentScores *scores = malloc(sizeof(TournamentScores));
    scores->numberOfGames = numberOfGames;
    scores->player1Scores = malloc(sizeof(int) * numberOfGames);
    scores->player2Scores = malloc(sizeof(int) * numberOfGames);

    return scores;
}

void freeTournamentScores(TournamentScores *scores)
{
    free(scores->player1Scores);
    free(scores->player2Scores);
    free(scores);
}

TournamentScores *scoreTournament(Tournament *tournament,
                                  PayoffMatrix *payoffMatrix)
{
    // Check that the tournament and payoff matrix are not NULL
    if ((tournament == NULL) || (payoffMatrix == NULL))
    {
        return NULL;
    }

    // Initialise a struct to hold the tournament scores
    TournamentScores *scores = newTournamentScores(tournament->numberOfGames);
    if (scores == NULL)
    {
        return NULL;
    }

    // Walk through each game in the tournament
    bool result;
    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        result = scoreGame(tournament->games[i],
                           payoffMatrix,
                           &(scores->player1Scores[i]),
                           &(scores->player2Scores[i]));

        if (result == false)
        {
            return NULL;
        }
    }

    return scores;
}

bool tournamentScoresEquals(TournamentScores *scores,
                            int numberOfGames,
                            int *expectedPlayer1Scores,
                            int *expectedPlayer2Scores)
{
    if (scores == NULL)
    {
        return false;
    }

    if (scores->numberOfGames != numberOfGames)
    {
        return false;
    }

    for (int i = 0; i < numberOfGames; i++)
    {
        if ((scores->player1Scores[i] != expectedPlayer1Scores[i]) ||
            (scores->player2Scores[i] != expectedPlayer2Scores[i]))
        {
            return false;
        }
    }

    return true;
}

bool updateStrategyScore(Strategy **strategies,
                         int numberOfStrategies,
                         Strategy *playerStrategy,
                         int playerScore,
                         int *scores)
{
    int strategyIndex = -1;

    for (int i = 0; i < numberOfStrategies; i++)
    {
        if (strcmp(strategies[i]->name, playerStrategy->name) == 0)
        {
            strategyIndex = i;
            break;
        }
    }

    if (strategyIndex == -1)
    {
        return false;
    }

    scores[strategyIndex] += playerScore;

    return true;
}

int *strategyScores(Strategy **strategies,
                    int numberOfStrategies,
                    Tournament *tournament,
                    TournamentScores *tournamentScores)
{
    if (tournament->numberOfGames != tournamentScores->numberOfGames)
    {
        return NULL;
    }

    // Allocate memory for one overall score per strategy
    int *scores = malloc(sizeof(int) * numberOfStrategies);
    if (scores == NULL)
    {
        return NULL;
    }

    // Initialise the scores
    for (int i = 0; i < numberOfStrategies; i++)
    {
        scores[i] = 0;
    }

    // Walk through each game in the tournament
    bool result;
    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        result = updateStrategyScore(strategies,
                                     numberOfStrategies,
                                     tournament->player1Strategies[i],
                                     tournamentScores->player1Scores[i],
                                     scores);
        if (result == false)
        {
            printf("Failed to update strategy scores");
            exit(-1);
        }

        result = updateStrategyScore(strategies,
                                     numberOfStrategies,
                                     tournament->player2Strategies[i],
                                     tournamentScores->player2Scores[i],
                                     scores);
        if (result == false)
        {
            printf("Failed to update strategy scores");
            exit(-1);
        }
    }

    return scores;
}

bool strategyScoresEqual(int *scores,
                         int *expectedScores,
                         int numberOfScores)
{
    for (int i = 0; i < numberOfScores; i++)
    {
        if (scores[i] != expectedScores[i])
        {
            return false;
        }
    }

    return true;
}

void printStrategyScores(Strategy **strategies,
                         int numberOfStrategies,
                         int *scores)
{
    for (int i = 0; i < numberOfStrategies; i++)
    {
        printf("Strategy: %s \tscore: %d\n", strategies[i]->name, scores[i]);
    }
}