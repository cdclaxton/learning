/* Demonstration */

/* Persons

   person(Name, AgeGroup).
*/



/* Events

   event(Person, EventType, Datetime).
*/
event(person1, eventA1, 2).
event(person1, eventA2, 3).
event(person1, eventA3, 4).
event(person1, eventA4, 5).

event(person2, eventB1, 2).
event(person2, eventB2, 3).

event(person3, eventC1, 2).
event(person3, eventC2, 3).
event(person3, eventC3, 4).

eventAtOrBeforeTime(Person, Event, Datetime) :-
    event(Person, Event, EventDateTime), (Datetime >= EventDateTime).

/* Inference

   inference(Person, Inference, DateTime, InferredConfidence).
*/

inference(Person, inferenceA1, Datetime, InferredConfidence) :-
    InferredConfidence = low, 
        \+ eventAtOrBeforeTime(Person, eventA1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventA2, Datetime) ;
    InferredConfidence = medium,
        \+ eventAtOrBeforeTime(Person, eventA1, Datetime),
        eventAtOrBeforeTime(Person, eventA2, Datetime) ;
    InferredConfidence = medium, 
        eventAtOrBeforeTime(Person, eventA1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventA2, Datetime) ;
    InferredConfidence = high, 
        eventAtOrBeforeTime(Person, eventA1, Datetime),
        eventAtOrBeforeTime(Person, eventA2, Datetime) .

inference(Person, inferenceA2, Datetime, InferredConfidence) :-
    InferredConfidence = low, 
        \+ eventAtOrBeforeTime(Person, eventA3, Datetime),
        \+ eventAtOrBeforeTime(Person, eventA4, Datetime) ;
    InferredConfidence = medium,
        \+ eventAtOrBeforeTime(Person, eventA3, Datetime),
        eventAtOrBeforeTime(Person, eventA4, Datetime) ;
    InferredConfidence = medium, 
        eventAtOrBeforeTime(Person, eventA3, Datetime),
        \+ eventAtOrBeforeTime(Person, eventA4, Datetime) ;
    InferredConfidence = high, 
        eventAtOrBeforeTime(Person, eventA3, Datetime),
        eventAtOrBeforeTime(Person, eventA4, Datetime) .

inference(Person, inferenceC1, Datetime, InferredConfidence) :-
    InferredConfidence = low, 
        \+ eventAtOrBeforeTime(Person, eventC1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventC2, Datetime) ;
    InferredConfidence = medium,
        \+ eventAtOrBeforeTime(Person, eventC1, Datetime),
        eventAtOrBeforeTime(Person, eventC2, Datetime) ;
    InferredConfidence = medium, 
        eventAtOrBeforeTime(Person, eventC1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventC2, Datetime) ;
    InferredConfidence = high, 
        eventAtOrBeforeTime(Person, eventC1, Datetime),
        eventAtOrBeforeTime(Person, eventC2, Datetime) .

/* Inferred role

   inferredRole(Person, Role, Datetime, InferredConfidence).
*/

inferredRole(Person, roleA, Datetime, InferredConfidence) :-
    inference(Person, inferenceA1, Datetime, ConfidenceA1),
    inference(Person, inferenceA2, Datetime, ConfidenceA2),
    ( InferredConfidence = low, (
        ConfidenceA1 = low, ConfidenceA2 = low ;
        ConfidenceA1 = low, ConfidenceA2 = medium ;
        ConfidenceA1 = medium, ConfidenceA2 = low 
      ) ;
      InferredConfidence = medium, (
        ConfidenceA1 = low, ConfidenceA2 = high ;
        ConfidenceA1 = medium, ConfidenceA2 = medium ;
        ConfidenceA1 = high, ConfidenceA2 = low 
      ) ;
      InferredConfidence = high, (
        ConfidenceA1 = medium, ConfidenceA2 = high ;
        ConfidenceA1 = high, ConfidenceA2 = medium ;
        ConfidenceA1 = high, ConfidenceA2 = high 
      )
    ).

inferredRole(Person, roleB, Datetime, InferredConfidence) :-
    InferredConfidence = low, 
        \+ eventAtOrBeforeTime(Person, eventB1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventB2, Datetime) ;
    InferredConfidence = medium,
        \+ eventAtOrBeforeTime(Person, eventB1, Datetime),
        eventAtOrBeforeTime(Person, eventB2, Datetime) ;
    InferredConfidence = medium, 
        eventAtOrBeforeTime(Person, eventB1, Datetime),
        \+ eventAtOrBeforeTime(Person, eventB2, Datetime) ;
    InferredConfidence = high, 
        eventAtOrBeforeTime(Person, eventB1, Datetime),
        eventAtOrBeforeTime(Person, eventB2, Datetime) .

inferredRole(Person, roleC, Datetime, InferredConfidence) :-
    inference(Person, inferenceC1, Datetime, InferredConfidenceC1),
    ( InferredConfidence = low,  
        (InferredConfidenceC1 = low ; 
         InferredConfidenceC1 = medium, \+ eventAtOrBeforeTime(Person, eventC3, Datetime)) ;
      InferredConfidence = medium,
        ((InferredConfidenceC1 = medium, eventAtOrBeforeTime(Person, eventC3, Datetime)) ; 
         (InferredConfidenceC1 = high, \+ eventAtOrBeforeTime(Person, eventC3, Datetime))) ;
      InferredConfidence = high, InferredConfidenceC1 = high, eventAtOrBeforeTime(Person, eventC3, Datetime)
    ).

/* Inferred association 

   inferredAssociation(PersonA, PersonB, Datetime, Association, Confidence).
*/



/* Member of the same group 

   memberOfSameGroup(PersonA, PersonB, Datetime).
*/