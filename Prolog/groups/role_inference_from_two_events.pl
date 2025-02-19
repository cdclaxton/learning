/* Role inference from two events

   The structure is:

   Event A ---|
              |---> Role
   Event B ---|

   where Events of type A and B can have confidences of {absent, low, high}.
*/

/* Events 

   event(EventType, Id, Confidence).
*/
event(eventA, 1, absent).
event(eventB, 1, absent).

event(eventA, 2, absent).
event(eventB, 2, low).

event(eventA, 3, low).
event(eventB, 3, absent).

event(eventA, 4, absent).
event(eventB, 4, high).

event(eventA, 5, high).
event(eventB, 5, absent).

event(eventA, 6, high).
event(eventB, 6, high).

/* Role inference */
roleFromEvents(EventA, EventB, Id, Confidence) :-
    Confidence = low, event(EventA, Id, absent), event(EventB, Id, absent) ;
    Confidence = medium, event(EventA, Id, absent), event(EventB, Id, Present), (Present = low ; Present = high) ;
    Confidence = medium, event(EventA, Id, Present), (Present = low ; Present = high), event(EventB, Id, absent) ;
    Confidence = high, event(EventA, Id, high), event(EventB, Id, high).

/* Test queries 

   roleFromEvents(eventA, eventB, 1, Confidence).  => Confidence = low
   roleFromEvents(eventA, eventB, 2, Confidence).  => Confidence = medium
   roleFromEvents(eventA, eventB, 3, Confidence).  => Confidence = medium
   roleFromEvents(eventA, eventB, 4, Confidence).  => Confidence = medium
   roleFromEvents(eventA, eventB, 5, Confidence).  => Confidence = medium
   roleFromEvents(eventA, eventB, 6, Confidence).  => Confidence = high
*/