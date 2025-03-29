/* Role inference from a single event.

   event --> role

   Event absent => role has a low confidence
   Event present with a low confidence => role has a medium confidence
   Event present with a medium or high confidence => role has a high confidence
*/

/* Events 
   event(EventName, Confidence).
*/
event(event1, low).
event(event2, medium).
event(event3, high).

/* Role inference */
roleFromEvent(Event, Confidence) :-
    Confidence = low, \+ event(Event, _) ; 
    Confidence = medium, event(Event, low) ;
    Confidence = high, (event(Event, medium) ; event(Event, high)).

/* Queries to run:

   roleFromEvent(event, Confidence).   => Confidence = low
   roleFromEvent(event1, Confidence).  => Confidence = medium
   roleFromEvent(event2, Confidence).  => Confidence = high
   roleFromEvent(event3, Confidence).  => Confidence = high

   Except for the first case in the predictate roleFromEvent, it is possible
   to find the event(s) that cause a given confidence.

   roleFromEvent(Event, low).  => false
   roleFromEvent(Event, medium).  => Event = event1
   roleFromEvent(Event, high).  => Event = event2 ; Event = event3
*/