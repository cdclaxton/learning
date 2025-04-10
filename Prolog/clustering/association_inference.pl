/* Association inference */

/* Person
 
   person(Name).
*/
person(person1).
person(person2).
person(person3).
person(person4).


/* Role 

   role(Person, Role).   
*/
role(person1, roleA).
role(person2, roleB).
role(person3, roleC).
role(person4, roleD).

/* Association

   association(PersonA, PersonB, AssociationType).
*/
association(person1, person2, assoc1).
association(person3, person4, assoc1).

undirectedAssociation(PersonA, PersonB, Assoc) :- 
    association(PersonA, PersonB, Assoc) ; 
    association(PersonB, PersonA, Assoc).

roles(PersonA, PersonB, RoleA, RoleB) :-
   (role(PersonA, RoleA), role(PersonB, RoleB)) ;
   (role(PersonB, RoleA), role(PersonA, RoleB)).

/* Inferred association */
inferredAssociation(PersonA, PersonB, InferredAssociation) :-
    undirectedAssociation(PersonA, PersonB, Assoc),
    ( InferredAssociation = inferredAssoc1, Assoc == assoc1, 
      roles(PersonA, PersonB, roleA, roleB) ;
      InferredAssociation = inferredAssoc2, Assoc == assoc1,
      roles(PersonA, PersonB, roleC, roleD) ).

/* Test queries 

   inferredAssociation(person1, person2, Assoc).  => Assoc = inferredAssoc1
   inferredAssociation(person2, person1, Assoc).  => Assoc = inferredAssoc1

   inferredAssociation(person3, person4, Assoc).  => Assoc = inferredAssoc2
   inferredAssociation(person4, person3, Assoc).  => Assoc = inferredAssoc2

   inferredAssociation(person1, person3, Assoc).  => false
*/

