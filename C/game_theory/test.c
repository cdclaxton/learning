#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "experiment.h"

void testPayoffElement()
{
    PayoffElement *element = buildPayoffElement(2, 3);
    assert(element->player1Payoff == 2);
    assert(element->player2Payoff == 3);

    freePayoffElement(element);
}

void testPayoff()
{
    PayoffMatrix *matrix = buildPayoffMatrix(3, 1, 0, 5);
    PayoffElement *element = NULL;

    // Player 1 cooperates, player 2 cooperates
    assert(payoff(COOPERATE, COOPERATE, matrix, &element) == true);
    assert(element->player1Payoff == 3);
    assert(element->player2Payoff == 3);

    // Player 1 cooperates, player 2 defects
    assert(payoff(COOPERATE, DEFECT, matrix, &element) == true);
    assert(element->player1Payoff == 0);
    assert(element->player2Payoff == 5);

    // Player 1 defects, player 2 cooperates
    assert(payoff(DEFECT, COOPERATE, matrix, &element) == true);
    assert(element->player1Payoff == 5);
    assert(element->player2Payoff == 0);

    // Player 1 defects, player 2 defects
    assert(payoff(DEFECT, DEFECT, matrix, &element) == true);
    assert(element->player1Payoff == 1);
    assert(element->player2Payoff == 1);

    freePayoffMatrix(matrix);
}

void testAlwaysDefect()
{
    Strategy *alwaysDefect = newAlwaysDefectStrategy();
    assert(alwaysDefect->decide(NULL, NULL, 1) == DEFECT);

    free(alwaysDefect);
}

void testAlwaysCooperate()
{
    Strategy *alwaysCooperate = newAlwaysCooperateStrategy();
    assert(alwaysCooperate->decide(NULL, NULL, 1) == COOPERATE);

    freeStrategy(alwaysCooperate);
}

void testAnyDefections()
{
    int decisions[5] = {COOPERATE, COOPERATE, DEFECT, COOPERATE, DEFECT};
    assert(anyDefections(decisions, 0) == false);
    assert(anyDefections(decisions, 1) == false);
    assert(anyDefections(decisions, 2) == true);
    assert(anyDefections(decisions, 3) == true);
    assert(anyDefections(decisions, 4) == true);

    int decisions2[2] = {DEFECT, COOPERATE};
    assert(anyDefections(decisions2, 0) == true);
    assert(anyDefections(decisions2, 1) == true);
}

void testAlwaysDefectIfOpponentDefects()
{
    Strategy *strategy = newAlwaysDefectIfOpponentDefectsStrategy();

    int opponentDecisions[5] = {COOPERATE, COOPERATE, DEFECT, COOPERATE, DEFECT};
    assert(strategy->decide(NULL, opponentDecisions, 0) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 1) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 2) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 3) == DEFECT);
    assert(strategy->decide(NULL, opponentDecisions, 4) == DEFECT);

    freeStrategy(strategy);
}

void testTitForTat()
{
    Strategy *strategy = newTitForTatStrategy();

    int opponentDecisions[5] = {COOPERATE, COOPERATE, DEFECT, COOPERATE, DEFECT};
    assert(strategy->decide(NULL, opponentDecisions, 0) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 1) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 2) == COOPERATE);
    assert(strategy->decide(NULL, opponentDecisions, 3) == DEFECT);
    assert(strategy->decide(NULL, opponentDecisions, 4) == COOPERATE);

    freeStrategy(strategy);
}

void testIsActionValid()
{
    assert(isActionValid(COOPERATE) == true);
    assert(isActionValid(DEFECT) == true);
    assert(isActionValid(2) == false);
}

void testUpdateGame()
{
    // Make a game with 3 rounds
    Game *game = newGame(3);
    assert(game->numberOfRounds == 3);
    assert(game->numberOfRoundsPlayed == 0);

    // Update the game with valid actions
    assert(updateGame(game, COOPERATE, DEFECT) == true);
    assert(game->numberOfRoundsPlayed == 1);
    assert(game->player1Actions[0] == COOPERATE);
    assert(game->player2Actions[0] == DEFECT);

    // Try to update the game with an invalid action for player 1
    assert(updateGame(game, -1, DEFECT) == false);
    assert(game->numberOfRoundsPlayed == 1);

    // Try to update the game with an invalid action for player 2
    assert(updateGame(game, DEFECT, -1) == false);
    assert(game->numberOfRoundsPlayed == 1);

    // Update the game with a 2nd set of valid actions
    assert(updateGame(game, DEFECT, DEFECT) == true);
    assert(game->numberOfRoundsPlayed == 2);
    assert(game->player1Actions[0] == COOPERATE);
    assert(game->player2Actions[0] == DEFECT);
    assert(game->player1Actions[1] == DEFECT);
    assert(game->player2Actions[1] == DEFECT);

    // Update the game with a 3rd set of valid actions
    assert(updateGame(game, DEFECT, COOPERATE) == true);
    assert(game->numberOfRoundsPlayed == 3);
    assert(game->player1Actions[0] == COOPERATE);
    assert(game->player2Actions[0] == DEFECT);
    assert(game->player1Actions[1] == DEFECT);
    assert(game->player2Actions[1] == DEFECT);
    assert(game->player1Actions[2] == DEFECT);
    assert(game->player2Actions[2] == COOPERATE);

    // Try to update the game when all rounds are exhausted
    assert(updateGame(game, DEFECT, COOPERATE) == false);
    assert(game->numberOfRoundsPlayed == 3);

    freeGame(game);
}

void testScoreGame()
{
    // Build the payoff matrix
    PayoffMatrix *payoff = buildPayoffMatrix(3, 1, 0, 5);

    // Make a game with 3 rounds
    Game *game = newGame(3);

    // Player scores
    int player1Score;
    int player2Score;

    // The game will be played as follows:
    //
    // Player 1:  | COOPERATE | DEFECT | COOPERATE |
    // Player 2:  | DEFECT    | DEFECT | COOPERATE |
    //
    // Giving scores at each round of:
    //
    // Player 1:  | 0 | 1 | 3 |
    // Player 2:  | 5 | 1 | 3 |
    //
    // The cumulative scores are then:
    //
    // Player 1:  | 0 | 1 | 4 |
    // Player 2:  | 5 | 6 | 9 |

    // Update the game for the 1st round
    assert(updateGame(game, COOPERATE, DEFECT) == true);
    assert(game->numberOfRoundsPlayed == 1);

    // Calculate the scores after the 1st round
    assert(scoreGame(game, payoff, &player1Score, &player2Score) == true);
    assert(player1Score == 0);
    assert(player2Score == 5);

    // Update the game for the 2nd round
    assert(updateGame(game, DEFECT, DEFECT) == true);
    assert(game->numberOfRoundsPlayed == 2);

    // Calculate the scores after the 2nd round
    assert(scoreGame(game, payoff, &player1Score, &player2Score) == true);
    assert(player1Score == 1);
    assert(player2Score == 6);

    // Update the game for the 3rd round
    assert(updateGame(game, COOPERATE, COOPERATE) == true);
    assert(game->numberOfRoundsPlayed == 3);

    // Calculate the scores after the 3rd round
    assert(scoreGame(game, payoff, &player1Score, &player2Score) == true);
    assert(player1Score == 4);
    assert(player2Score == 9);

    freeGame(game);
    freePayoffMatrix(payoff);
}

void testExecuteGame()
{
    Strategy *strategy1 = newAlwaysCooperateStrategy();
    Strategy *strategy2 = newAlwaysDefectStrategy();

    // Execute the game
    Game *game = newGame(3);
    assert(executeGame(game, strategy1, strategy2) == true);

    // Check the game
    int expectedPlayer1Actions[3] = {COOPERATE, COOPERATE, COOPERATE};
    int expectedPlayer2Actions[3] = {DEFECT, DEFECT, DEFECT};
    assert(gameEquals(game, 3, 3, expectedPlayer1Actions, expectedPlayer2Actions) == true);

    // Free allocated memory
    freeStrategy(strategy1);
    freeStrategy(strategy2);
    freeGame(game);
}

void testTournamentOneStrategy()
{
    // Build an array holding a single strategy
    Strategy *strategies[1];
    strategies[0] = newAlwaysDefectStrategy();

    // Build a tournament with a single strategy
    Tournament *tournament = newTournament(strategies, 1, 3);

    assert(tournament->numberOfGames == 1);

    assert(tournament->player1Strategies[0] == strategies[0]);
    assert(strcmp(tournament->player1Strategies[0]->name, "always-defect") == 0);

    assert(tournament->player2Strategies[0] == strategies[0]);
    assert(strcmp(tournament->player2Strategies[0]->name, "always-defect") == 0);

    // Free the space allocated to the tournament
    freeTournament(tournament);
    freeStrategies(strategies, 1);
}

void testTournamentTwoStrategies()
{
    // Build an array holding two strategies
    Strategy *strategies[2];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();

    // Build a tournament with two strategies
    Tournament *tournament = newTournament(strategies, 2, 3);

    assert(tournament->numberOfGames == 4);

    // Game 1: Both always defect
    assert(tournament->player1Strategies[0] == strategies[0]);
    assert(strcmp(tournament->player1Strategies[0]->name, "always-defect") == 0);
    assert(tournament->player2Strategies[0] == strategies[0]);
    assert(strcmp(tournament->player2Strategies[0]->name, "always-defect") == 0);

    // Game 2: Always defect vs. always cooperate
    assert(tournament->player1Strategies[1] == strategies[0]);
    assert(strcmp(tournament->player1Strategies[1]->name, "always-defect") == 0);
    assert(tournament->player2Strategies[1] == strategies[1]);
    assert(strcmp(tournament->player2Strategies[1]->name, "always-cooperate") == 0);

    // Game 3: Always cooperate vs. always defect
    assert(tournament->player1Strategies[2] == strategies[1]);
    assert(strcmp(tournament->player1Strategies[2]->name, "always-cooperate") == 0);
    assert(tournament->player2Strategies[2] == strategies[0]);
    assert(strcmp(tournament->player2Strategies[2]->name, "always-defect") == 0);

    // Game 4: Both always cooperate
    assert(tournament->player1Strategies[3] == strategies[1]);
    assert(strcmp(tournament->player1Strategies[3]->name, "always-cooperate") == 0);
    assert(tournament->player2Strategies[3] == strategies[1]);
    assert(strcmp(tournament->player2Strategies[3]->name, "always-cooperate") == 0);

    // Free the space allocated to the tournament and the strategies
    freeTournament(tournament);
    freeStrategies(strategies, 2);
}

void testExecuteTournament()
{
    // Build an array holding two strategies
    Strategy *strategies[2];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();

    // Build a tournament with two strategies
    Tournament *tournament = newTournament(strategies, 2, 3);

    // Execute the tournament
    executeTournament(tournament);

    // Check the number of games
    assert(tournament->numberOfGames == 4);

    // Check the 1st game (defect vs defect)
    int game1ExpectedPlayer1Actions[3] = {DEFECT, DEFECT, DEFECT};
    int game1ExpectedPlayer2Actions[3] = {DEFECT, DEFECT, DEFECT};
    assert(gameEquals(tournament->games[0], 3, 3,
                      game1ExpectedPlayer1Actions,
                      game1ExpectedPlayer2Actions) == true);

    // Check the 2nd game (defect vs cooperate)
    int game2ExpectedPlayer1Actions[3] = {DEFECT, DEFECT, DEFECT};
    int game2ExpectedPlayer2Actions[3] = {COOPERATE, COOPERATE, COOPERATE};
    assert(gameEquals(tournament->games[1], 3, 3,
                      game2ExpectedPlayer1Actions,
                      game2ExpectedPlayer2Actions) == true);

    // Check the 3rd game (cooperate vs defect)
    int game3ExpectedPlayer1Actions[3] = {COOPERATE, COOPERATE, COOPERATE};
    int game3ExpectedPlayer2Actions[3] = {DEFECT, DEFECT, DEFECT};
    assert(gameEquals(tournament->games[2], 3, 3,
                      game3ExpectedPlayer1Actions,
                      game3ExpectedPlayer2Actions) == true);

    // Check the 4th game (cooperate vs cooperate)
    int game4ExpectedPlayer1Actions[3] = {COOPERATE, COOPERATE, COOPERATE};
    int game4ExpectedPlayer2Actions[3] = {COOPERATE, COOPERATE, COOPERATE};
    assert(gameEquals(tournament->games[3], 3, 3,
                      game4ExpectedPlayer1Actions,
                      game4ExpectedPlayer2Actions) == true);

    // Free the space allocated to the tournament and the strategies
    freeTournament(tournament);
    freeStrategies(strategies, 2);
}

void testNewTournamentScores()
{
    TournamentScores *scores1 = newTournamentScores(0);
    assert(scores1 == NULL);

    TournamentScores *scores2 = newTournamentScores(1);
    assert(scores2->numberOfGames == 1);
    freeTournamentScores(scores2);
}

void testScoreTournament()
{
    // Build an array holding two strategies
    Strategy *strategies[2];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();

    // Build a payoff matrix
    PayoffMatrix *payoffMatrix = buildPayoffMatrix(3, 1, 0, 5);

    // Build a tournament with two strategies
    Tournament *tournament = newTournament(strategies, 2, 3);

    // Execute the tournament
    executeTournament(tournament);

    // Score the tournament
    TournamentScores *scores = scoreTournament(tournament,
                                               payoffMatrix);

    // Check the scores are as expected for the three rounds per game
    //
    // Game 1: always defect vs always defect
    //   Player 1:  | DEFECT (1) | DEFECT (1) | DEFECT (1) | => total=3
    //   Player 2:  | DEFECT (1) | DEFECT (1) | DEFECT (1) | => total=3
    //
    // Game 2: always defect vs always cooperate
    //   Player 1:  | DEFECT (5)    | DEFECT (5)    | DEFECT (5)    | => total=15
    //   Player 2:  | COOPERATE (0) | COOPERATE (0) | COOPERATE (0) | => total=0
    //
    // Game 3: always cooperate vs. always defect
    //   Player 1:  | COOPERATE (0) | COOPERATE (0) | COOPERATE (0) | => total=0
    //   Player 2:  | DEFECT (5)    | DEFECT (5)    | DEFECT (5)    | => total=15
    //
    // Game 4: always cooperate vs. always cooperate
    //   Player 1:  | COOPERATE (3) | COOPERATE (3) | COOPERATE (3) | => total=9
    //   Player 2:  | COOPERATE (3) | COOPERATE (3) | COOPERATE (3) | => total=9

    int expectedPlayer1Scores[4] = {3, 15, 0, 9};
    int expectedPlayer2Scores[4] = {3, 0, 15, 9};

    assert(tournamentScoresEquals(scores,
                                  4,
                                  expectedPlayer1Scores,
                                  expectedPlayer2Scores) == true);

    // Free the space allocated to the tournament and the strategies
    freeTournament(tournament);
    freePayoffMatrix(payoffMatrix);
    freeStrategies(strategies, 2);
    freeTournamentScores(scores);
}

void testUpdateStrategyScore()
{
    // Build an array holding two strategies
    Strategy *strategies[2];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();

    int scores[2] = {10, 20};

    assert(updateStrategyScore(strategies, 2, strategies[0], 5, scores) == true);
    assert(scores[0] == 15);
    assert(scores[1] == 20);

    assert(updateStrategyScore(strategies, 2, strategies[1], 10, scores) == true);
    assert(scores[0] == 15);
    assert(scores[1] == 30);

    freeStrategies(strategies, 2);
}

void testStrategyScores()
{
    // Build an array holding two strategies
    Strategy *strategies[2];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();

    // Build a payoff matrix
    PayoffMatrix *payoffMatrix = buildPayoffMatrix(3, 1, 0, 5);

    // Build a tournament with two strategies
    Tournament *tournament = newTournament(strategies, 2, 3);

    // Execute the tournament
    executeTournament(tournament);

    // Score the tournament where
    // D = always defect strategy
    // C = always cooperate strategy
    //                   D-D  D-C  C-D  C-C
    // Player 1 scores: {3,   15,    0,  9}
    // Player 2 scores: {3,    0,   15,  9}
    TournamentScores *scores = scoreTournament(tournament,
                                               payoffMatrix);

    // Calculate the scores for each of the two strategies
    int *overallScores = strategyScores(strategies, 2, tournament, scores);

    // Check the strategy scores
    // D = 3 + 3 + 15 + 15 = 36
    // C = 9 + 9 = 18
    int expectedScores[2] = {36, 18};
    assert(strategyScoresEqual(overallScores, expectedScores, 2));

    // Free the space allocated to the tournament and the strategies
    freeTournament(tournament);
    freePayoffMatrix(payoffMatrix);
    freeStrategies(strategies, 2);
    freeTournamentScores(scores);
    free(overallScores);
}

// Run all of the tests
int main(void)
{
    printf("Running tests\n");

    // Payoff
    testPayoffElement();
    testPayoff();

    // Strategy utility functions
    testAnyDefections();

    // Strategies
    testAlwaysDefect();
    testAlwaysCooperate();
    testAlwaysDefectIfOpponentDefects();
    testTitForTat();

    // Game
    testIsActionValid();
    testUpdateGame();
    testScoreGame();
    testExecuteGame();

    // Tournament
    testTournamentOneStrategy();
    testTournamentTwoStrategies();
    testExecuteTournament();

    // Tournament scores
    testNewTournamentScores();
    testScoreTournament();

    // Strategy scores
    testUpdateStrategyScore();
    testStrategyScores();

    printf("All tests pass\n");
}