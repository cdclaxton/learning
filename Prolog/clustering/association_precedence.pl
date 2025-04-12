/* Association precedence */

/* Lookup from an association type to a precedence value 
   precedenceLookup(AssociaionType, Precedence).
*/
precedenceLookup(assocType1, 2.0).
precedenceLookup(assocType2, 3.0).

/* Associations between two persons
   association(Person1, Person2, AssociationType, Probability).
*/
association(person1, person2, assocType1, 0.4).
association(person1, person2, assocType2, 0.8).

/* Severity is a measure that combines the precedence value of an association
   and its probability */
severity(PrecedenceValue, Probability, Severity) :- 
    Severity is PrecedenceValue * Probability.

/* Association severity */
associationSeverity(Person1, Person2, AssocType, Severity) :-
    association(Person1, Person2, AssocType, Probability),
    precedenceLookup(AssocType, PrecedenceValue),
    severity(PrecedenceValue, Probability, Severity).

/* Associations between two persons */
associations(Person1, Person2, Associations) :- 
    findall(A, association(Person1, Person2, A, _), Associations).

/* Severities between two persons 
   severities(Person1, Person2, Associations, Severities).
*/
severities(_, _, [], []).
severities(Person1, Person2, [AH|AT], [SH|ST]) :-
    precedenceLookup(AH, PrecedenceValue),
    association(Person1, Person2, AH, Probability),
    severity(PrecedenceValue, Probability, SH),
    severities(Person1, Person2, AT, ST).

/* Associations and their severities */
associationSeverities(Person1, Person2, Associations, Severities) :-
    associations(Person1, Person2, Associations),
    severities(Person1, Person2, Associations, Severities).

/* Given a list of values V and their probabilities P, find the value that 
   maximises the probability */
argMaxHelper([], [], PartialMax, PartialMax, PartialV, PartialV).
argMaxHelper([V1|V2], [P1|P2], PartialMax, FinalMax, _, FinalV) :- 
    P1>PartialMax, argMaxHelper(V2, P2, P1, FinalMax, V1, FinalV).
argMaxHelper([_|V2], [P1|P2], PartialMax, FinalMax, PartialV, FinalV) :- 
    P1=<PartialMax, argMaxHelper(V2, P2, PartialMax, FinalMax, PartialV, FinalV).
argMax(V, P, PMax, VMax) :- argMaxHelper(V, P, 0, PMax, 0, VMax).

/* Find the highest severity association */
highestSeverity(Person1, Person2, HighestAssociation, HighestSeverity) :-
    associationSeverities(Person1, Person2, Associations, Severities),
    argMax(Associations, Severities, HighestSeverity, HighestAssociation).