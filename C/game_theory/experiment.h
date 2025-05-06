#include <stdbool.h>

// Constants related to player actions
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
void printPayoffElement(const PayoffElement *const element);

typedef struct
{
    PayoffElement *cooperateCooperate; // Payoff if both players cooperate
    PayoffElement *cooperateDefect;    // Payoff if player 1 cooperates and player 2 defects
    PayoffElement *defectCooperate;    // Payoff if player 1 defects and player 2 cooperates
    PayoffElement *defectDefect;       // Payoff if both players defect
} PayoffMatrix;

PayoffMatrix *buildPayoffMatrix(int bothPlayersCooperate, // Payoff for each player when they both cooperate
                                int bothPlayersDefect,    // Payoff for each player when they both defect
                                int cooperateDefect,      // Payoff for the cooperating player when the other defects
                                int defectCooperate);     // Payoff for the defecting player when the other cooperates

// Free the payoff matrix (and its elements)
void freePayoffMatrix(PayoffMatrix *matrix);

bool payoff(int player1Action,                // Action of player 1
            int player2Action,                // Action of player 2
            const PayoffMatrix *const matrix, // Payoff matrix
            PayoffElement **const result);    // Payoff result

// -----------------------------------------------------------------------------
// Strategy
// -----------------------------------------------------------------------------

typedef struct
{
    // Name of the strategy
    char *name;

    // Decision function that takes an array of the player's decisions, their
    // opponent's decisions and the current turn index
    int (*decide)(const int *const playerDecisions,
                  const int *const opponentDecisions,
                  int currentTurn);
} Strategy;

// Free the memory allocated for the strategy
void freeStrategy(Strategy *const strategy);

// Free the memory allocated to an array of strategies
void freeStrategies(Strategy **const strategies,
                    int numberOfStrategies);

// -----------------------------------------------------------------------------
// Strategies
// -----------------------------------------------------------------------------

int alwaysDefectDecide(const int *const playerDecisions,
                       const int *const opponentDecisions,
                       int currentTurn);
Strategy *newAlwaysDefectStrategy();

int alwaysCooperateDecide(const int *const playerDecisions,
                          const int *const opponentDecisions,
                          int currentTurn);
Strategy *newAlwaysCooperateStrategy();

int alwaysDefectIfOpponentDefectsDecide(const int *const playerDecisions,
                                        const int *const opponentDecisions,
                                        int currentTurn);
Strategy *newAlwaysDefectIfOpponentDefectsStrategy();

int titForTatDecide(const int *const playerDecisions,
                    const int *const opponentDecisions,
                    int currentTurn);
Strategy *newTitForTatStrategy();

// -----------------------------------------------------------------------------
// Strategy utility functions
// -----------------------------------------------------------------------------

// Are there any defections in the range [0, maxIndex]?
bool anyDefections(const int *const decisions,
                   int maxIndex);

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
void freeGame(Game *const game);

// Is the action valid?
bool isActionValid(int action);

// Update the actions of the players in a game
bool updateGame(Game *const game,
                int player1Action,
                int player2Action);

// Calculate the scores for the two players
bool scoreGame(const Game *const game,
               const PayoffMatrix *const payoffMatrix,
               int *const player1Score,
               int *const player2Score);

// Print the game to stdout (for debugging)
void printGame(const Game *const game);

// Execute the game
bool executeGame(Game *const game,
                 const Strategy *const player1,
                 const Strategy *const player2);

// Does the game have the expected values?
bool gameEquals(const Game *const game,
                int expectedNumberOfRounds,
                int expectedNumberOfRoundsPlayed,
                const int *const expectedPlayer1Actions,
                const int *const expectedPlayer2Actions);

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
Tournament *newTournament(Strategy **const strategies,
                          int numberOfStrategies,
                          int numberOfRoundsPerGame);

// Free the space allocated to a tournament
void freeTournament(Tournament *const tournament);

// Print the tournament to stdout (for debugging purposes)
void printTournament(const Tournament *const tournament);

// Execute the tournament
void executeTournament(Tournament *const tournament);

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
void freeTournamentScores(TournamentScores *const scores);

// Calculate the scores for the tournament
TournamentScores *scoreTournament(const Tournament *const tournament,
                                  const PayoffMatrix *const payoffMatrix);

// Are the tournament scores equal to those expected?
bool tournamentScoresEquals(const TournamentScores *const scores,
                            int numberOfGames,
                            const int *const expectedPlayer1Scores,
                            const int *const expectedPlayer2Scores);

// Update the overall strategy scores
bool updateStrategyScore(Strategy **const strategies,
                         int numberOfStrategies,
                         const Strategy *const playerStrategy,
                         int playerScore,
                         int *const scores);

// Calculate the score for each strategy
int *strategyScores(Strategy **const strategies,
                    int numberOfStrategies,
                    const Tournament *const tournament,
                    const TournamentScores *const tournamentScores);

// Are the strategy scores equal to their expected scores?
bool strategyScoresEqual(const int *const scores,
                         const int *const expectedScores,
                         int numberOfScores);

// Print the strategy scores to stdout
void printStrategyScores(Strategy **const strategies,
                         int numberOfStrategies,
                         const int *const scores);