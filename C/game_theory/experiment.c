#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "experiment.h"

PayoffElement *buildPayoffElement(int player1Payoff,
                                  int player2Payoff)
{
    PayoffElement *const element = malloc(sizeof(PayoffElement));
    if (element == NULL)
    {
        printf("Failed to allocate space for the payoff element");
        exit(-1);
    }

    element->player1Payoff = player1Payoff;
    element->player2Payoff = player2Payoff;

    return element;
}

void printPayoffElement(const PayoffElement *const element)
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

bool payoff(int player1Action,                // Action of player 1
            int player2Action,                // Action of player 2
            const PayoffMatrix *const matrix, // Payoff matrix
            PayoffElement **result)           // Payoff result
{
    if ((player1Action == COOPERATE) && (player2Action == COOPERATE))
    {
        *result = matrix->cooperateCooperate;
        return true;
    }
    else if ((player1Action == COOPERATE) && (player2Action == DEFECT))
    {
        *result = matrix->cooperateDefect;
        return true;
    }
    else if ((player1Action == DEFECT) && (player2Action == COOPERATE))
    {
        *result = matrix->defectCooperate;
        return true;
    }
    else if ((player1Action == DEFECT) && (player2Action == DEFECT))
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

void freeStrategy(Strategy *const strategy)
{
    free(strategy);
}

void freeStrategies(Strategy **const strategies,
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

int alwaysDefectDecide(const int *const playerDecisions,
                       const int *const opponentDecisions,
                       int currentTurn)
{
    return DEFECT;
}

Strategy *newAlwaysDefectStrategy()
{
    Strategy *const strategy = malloc(sizeof(Strategy));
    strategy->name = "always-defect";
    strategy->decide = alwaysDefectDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy: Always cooperate
// -----------------------------------------------------------------------------

int alwaysCooperateDecide(const int *const playerDecisions,
                          const int *const opponentDecisions,
                          int currentTurn)
{
    return COOPERATE;
}

Strategy *newAlwaysCooperateStrategy()
{
    Strategy *const strategy = malloc(sizeof(Strategy));
    strategy->name = "always-cooperate";
    strategy->decide = alwaysCooperateDecide;
    return strategy;
}

// -----------------------------------------------------------------------------
// Strategy: Always defect if the opponent defects
// -----------------------------------------------------------------------------

int alwaysDefectIfOpponentDefectsDecide(const int *const playerDecisions,
                                        const int *const opponentDecisions,
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

int titForTatDecide(const int *const playerDecisions,
                    const int *const opponentDecisions,
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

bool anyDefections(const int *const decisions,
                   int maxIndex)
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

void freeGame(Game *const game)
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

bool updateGame(Game *const game,
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

bool scoreGame(const Game *const game,
               const PayoffMatrix *const payoffMatrix,
               int *const player1Score,
               int *const player2Score)
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

void printGame(const Game *const game)
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

bool executeGame(Game *const game,
                 const Strategy *const player1,
                 const Strategy *const player2)
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

bool gameEquals(const Game *const game,
                int expectedNumberOfRounds,
                int expectedNumberOfRoundsPlayed,
                const int *const expectedPlayer1Actions,
                const int *const expectedPlayer2Actions)
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

Tournament *newTournament(Strategy **const strategies,
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

void freeTournament(Tournament *const tournament)
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

void printTournament(const Tournament *const tournament)
{
    printf("Tournament:\n");
    printf("Number of games: %d\n", tournament->numberOfGames);

    for (int i = 0; i < tournament->numberOfGames; i++)
    {
        printf("Strategy %s vs %s\n", tournament->player1Strategies[i]->name,
               tournament->player2Strategies[i]->name);
    }
}

void executeTournament(Tournament *const tournament)
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

void freeTournamentScores(TournamentScores *const scores)
{
    free(scores->player1Scores);
    free(scores->player2Scores);
    free(scores);
}

TournamentScores *scoreTournament(const Tournament *const tournament,
                                  const PayoffMatrix *const payoffMatrix)
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

bool tournamentScoresEquals(const TournamentScores *const scores,
                            int numberOfGames,
                            const int *const expectedPlayer1Scores,
                            const int *const expectedPlayer2Scores)
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

bool updateStrategyScore(Strategy **const strategies,
                         int numberOfStrategies,
                         const Strategy *const playerStrategy,
                         int playerScore,
                         int *const scores)
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

int *strategyScores(Strategy **const strategies,
                    int numberOfStrategies,
                    const Tournament *const tournament,
                    const TournamentScores *const tournamentScores)
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

bool strategyScoresEqual(const int *const scores,
                         const int *const expectedScores,
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

void printStrategyScores(Strategy **const strategies,
                         int numberOfStrategies,
                         const int *const scores)
{
    printf("Score\tStrategy\n");
    for (int i = 0; i < numberOfStrategies; i++)
    {
        printf("%d\t%s\n", scores[i], strategies[i]->name);
    }
}