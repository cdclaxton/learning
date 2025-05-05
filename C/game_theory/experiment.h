#include <stdbool.h>

// Constants related to player decisions
#define COOPERATE 0
#define DEFECT 1

typedef struct
{
    int player1Payoff; // Payoff for player 1
    int player2Payoff; // Payoff for player 2
} PayoffElement;

PayoffElement *buildPayoffElement(int player1Payoff,  // Payoff for player 1
                                  int player2Payoff); // Payoff for player 2

// Free the memory allocated for the payoff element
void freePayoffElement(PayoffElement *element);

// Print the payoff element to stdout
void printPayoffElement(PayoffElement *element);

typedef struct
{
    PayoffElement *cooperateCooperate;
    PayoffElement *cooperateDefect;
    PayoffElement *defectCooperate;
    PayoffElement *defectDefect;
} PayoffMatrix;

PayoffMatrix *buildPayoffMatrix(int bothPlayersCooperate, // Payoff for each player when they both cooperate
                                int bothPlayersDefect,    // Payoff for each player when they both defect
                                int cooperateDefect,      // Payoff for the cooperating player when the other defects
                                int defectCooperate);     // Payoff for the defecting player when the other cooperates

// Free the payoff matrix (and its elements)
void freePayoffMatrix(PayoffMatrix *matrix);

bool payoff(int player1Decision,     // Decision of player 1
            int player2Decision,     // Decision of player 2
            PayoffMatrix *matrix,    // Payoff matrix
            PayoffElement **result); // Payoff result

// -----------------------------------------------------------------------------
// Strategy
// -----------------------------------------------------------------------------

typedef struct
{
    // Name of the strategy
    char *name;

    // Decision function that takes an array of the player's decisions, their
    // opponent's decisions and the current turn index
    int (*decide)(int *playerDecisions, int *opponentDecisions, int currentTurn);
} Strategy;

// Free the memory allocated for the strategy
void freeStrategy(Strategy *strategy);

// Free the memory allocated to an array of strategies
void freeStrategies(Strategy **strategies,
                    int numberOfStrategies);

// -----------------------------------------------------------------------------
// Strategies
// -----------------------------------------------------------------------------

int alwaysDefectDecide(int *, int *, int);
Strategy *newAlwaysDefectStrategy();

int alwaysCooperateDecide(int *, int *, int);
Strategy *newAlwaysCooperateStrategy();

int alwaysDefectIfOpponentDefectsDecide(int *, int *, int);
Strategy *newAlwaysDefectIfOpponentDefectsStrategy();

int titForTatDecide(int *, int *, int);
Strategy *newTitForTatStrategy();

// -----------------------------------------------------------------------------
// Strategy utility functions
// -----------------------------------------------------------------------------

// Are there any defections in the range [0, maxIndex]?
bool anyDefections(int *decisions, int maxIndex);

// -----------------------------------------------------------------------------
// Game
// -----------------------------------------------------------------------------

typedef struct
{
    // Number of rounds
    int numberOfRounds;

    // Number of rounds played
    int numberOfRoundsPlayed;

    // Actions made by player 1
    int *player1Actions;

    // Actions made by player 2
    int *player2Actions;
} Game;

// Create a new game with the given number of rounds
Game *newGame(int numberOfRounds);

// Free the memory allocated for the game
void freeGame(Game *game);

// Is the action valid?
bool isActionValid(int action);

// Update the actions of the players in a game
bool updateGame(Game *game,
                int player1Action,
                int player2Action);

// Calculate the scores for the two players
bool scoreGame(Game *game,
               PayoffMatrix *payoffMatrix,
               int *player1Score,
               int *player2Score);

// Print the game to stdout (for debugging)
void printGame(Game *game);

// Execute the game
bool executeGame(Game *game,
                 Strategy *player1,
                 Strategy *player2);

// Does the game have the expected values?
bool gameEquals(Game *game,
                int expectedNumberOfRounds,
                int expectedNumberOfRoundsPlayed,
                int *expectedPlayer1Actions,
                int *expectedPlayer2Actions);

// -----------------------------------------------------------------------------
// Tournament
// -----------------------------------------------------------------------------

// A tournament consists of one or more games
typedef struct
{
    // Number of games
    int numberOfGames;

    // Strategies for player 1 and player 2 (array of pointers to the strategies)
    Strategy **player1Strategies;
    Strategy **player2Strategies;

    // Array of games
    Game **games;

} Tournament;

// Build a new tournament where every strategy plays against every other
// strategy and itself
Tournament *newTournament(Strategy **strategies,
                          int numberOfStrategies,
                          int numberOfRoundsPerGame);

// Free the space allocated to a tournament
void freeTournament(Tournament *tournament);

// Print the tournament to stdout (for debugging purposes)
void printTournament(Tournament *tournament);

// Execute the tournament
void executeTournament(Tournament *tournament);

typedef struct
{
    // Number of games
    int numberOfGames;

    // Array of scores for players 1 and 2
    int *player1Scores;
    int *player2Scores;

} TournamentScores;

// Instantiate a new TournamentScores struct
TournamentScores *newTournamentScores(int numberOfGames);

// Free the memory allocated for the tournament scores struct
void freeTournamentScores(TournamentScores *scores);

// Calculate the scores for the tournament
TournamentScores *scoreTournament(Tournament *tournament,
                                  PayoffMatrix *payoff);

// Are the tournament scores equal to those expected?
bool tournamentScoresEquals(TournamentScores *scores,
                            int numberOfGames,
                            int *expectedPlayer1Scores,
                            int *expectedPlayer2Scores);

// Update the overall strategy scores
bool updateStrategyScore(Strategy **strategies,
                         int numberOfStrategies,
                         Strategy *playerStrategy,
                         int playerScore,
                         int *scores);

// Calculate the score for each strategy
int *strategyScores(Strategy **strategies,
                    int numberOfStrategies,
                    Tournament *tournament,
                    TournamentScores *tournamentScores);

// Are the strategy scores equal to their expected scores?
bool strategyScoresEqual(int *scores,
                         int *expectedScores,
                         int numberOfScores);

// Print the strategy scores to stdout
void printStrategyScores(Strategy **strategies,
                         int numberOfStrategies,
                         int *scores);