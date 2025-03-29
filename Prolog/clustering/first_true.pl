/* Return the highest precedence true statement.
*/

/* Event

   event(Id, EventType, Datetime).

   The event type precedence is event2 > event1.
*/

event(1, event1, 1).

event(2, event1, 2).
event(3, event2, 2).

event(4, event2, 3).

/* Test queries

   highest(Id, Event, 1).  => Id = 1, EventType = event1 ;
   highest(Id, Event, 2).  => Id = 3, EventType = event2 ;
   highest(Id, Event, 3).  => Id = 4, EventType = event2 ;
*/

highest(Id, EventType, Datetime) :-
    EventType = event2, event(Id, event2, Datetime) ;
    EventType = event1, event(Id, event1, Datetime), \+ event(_, event2, Datetime).

