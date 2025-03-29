/* Role inference from hierarchy 

   The structure is:

   event --> inference --> role
*/

/* Events

   event(EventType, Id, Confidence).
*/

event(eventA, 1, low).
event(eventA, 2, high).

/* Event inference */
inference(Event, Id, Confidence) :-
    Confidence = low, \+ event(Event, Id, _) ;
    Confidence = medium, event(Event, Id, low) ;
    Confidence = high, event(Event, Id, high).

/* Test queries

   inference(eventX, 1, Confidence).  => Confidence = low
   inference(eventA, 1, Confidence).  => Confidence = medium 
   inference(eventA, 2, Confidence).  => Confidence = high
*/

/* Role inference */
role(Event, Id, Confidence) :-
    inference(Event, Id, InferenceConfidence),
    ( (Confidence = low, InferenceConfidence == low) ; 
      (Confidence = high, InferenceConfidence == medium) ; 
      (Confidence = high, InferenceConfidence == high) ).

/* Test queries

   role(eventX, 1, Confidence).  => Confidence = low
   role(eventA, 1, Confidence).  => Confidence = high
   role(eventA, 2, Confidence).  => Confidence = high

   role(eventA, Id, high).  => Id = 1 ; Id = 2
*/