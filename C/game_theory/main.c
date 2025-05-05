#include <stdio.h>
#include <stdlib.h>
#include "experiment.h"

int main(void)
{
    printf("Game theory experiment\n");

    // Build an array holding two strategies
    Strategy *strategies[4];
    strategies[0] = newAlwaysDefectStrategy();
    strategies[1] = newAlwaysCooperateStrategy();
    strategies[2] = newTitForTatStrategy();
    strategies[3] = newAlwaysDefectIfOpponentDefectsStrategy();
    int numberOfStrategies = 4;

    // Build a payoff matrix
    PayoffMatrix *payoffMatrix = buildPayoffMatrix(3, 1, 0, 5);

    // Build a tournament with two strategies
    Tournament *tournament = newTournament(strategies, numberOfStrategies, 200);

    // Execute the tournament
    executeTournament(tournament);

    // Score the tournament where
    TournamentScores *scores = scoreTournament(tournament,
                                               payoffMatrix);

    // Calculate the scores for each of the two strategies
    int *overallScores = strategyScores(strategies,
                                        numberOfStrategies,
                                        tournament,
                                        scores);

    printStrategyScores(strategies,
                        numberOfStrategies,
                        overallScores);

    // Free the space allocated to the tournament and the strategies
    freeTournament(tournament);
    freePayoffMatrix(payoffMatrix);
    freeStrategies(strategies, numberOfStrategies);
    freeTournamentScores(scores);
    free(overallScores);

    return 0;
}