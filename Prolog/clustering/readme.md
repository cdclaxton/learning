# Deterministic clustering

## Introduction

Prolog has been used to investigate a first-order logic approach to overlappying graph clustering.

## Building blocks

### Infer the role of an entity from a single event

The role of an entity can be inferred from the events to which it is related. In the specification of the probability of a role, it is necessary to consider that an event may not have occurred, i.e. it is deemed absent. If the event is present then, for the purposes of this example, it may have a probability that is low or high, i.e. $c_e \in \{ \text{low}, \text{high} \}$. The probability of the inferred role $c_r \in \{ \text{low}, \text{medium}, \text{high} \}$.

The logical inference is from an event to a role:

```
event --> role
```

The probability of the role given the event's presence or absence and its probability is defined as:

| Event   | Event probability | Role probability |
|---------|-------------------|------------------|
| Absent  | -                 | low              |
| Present | low               | medium           |
| Present | high              | high             |

This is implemented in: `role_inference_from_single_event.pl`. To run experiments:

```bash
prolog role_inference_from_single_event.pl 
```

and then enter a query, e.g.

```prolog
roleFromEvent(event1, Probability).
```

and press `;` to find all variables that satisfy the predicate.

### Infer the role of an entity from two events

Suppose that there are two types of events that contribute to the probability of an inferred role, as illustrated below.

```
event A ---|
           |---> role
event B ---|
```

The (discrete) probability associated with an event of a given type (A or B) is given by $e \in \{ \text{absent}, \text{low}, \text{high} \}$. The probability of the role $c_r \in \{ \text{low}, \text{medium}, \text{high} \}$.

The probability of the role given the event A or B's presence or absence and its probability (if present) is defined as:

| Event A  | Event B  | Role probability |
|----------|----------|------------------|
| Absent   | Absent   | low              |
| Absent   | low/high | medium           |
| low/high | Absent   | medium           |
| high     | high     | high             |

This is implemented in: `role_inference_from_two_events.pl`.

### Infer a role from an intermediary inference

The previous two cases considered a direct connection from a single event or two events to an inferred role. However, events may lead to an inference, which in turn leads to an inferred role. This is illustrated below.

```
event --> inference --> role
```

Suppose the intermediate inference has a truth table as shown:

| Event  | Inference |
|--------|-----------|
| Absent | low       |
| low    | medium    |
| high   | high      |

The role inference using the intermediate inference as an input has the following truth table:

| Inference | Role |
|-----------|------|
| low       | low  |
| medium    | high |
| high      | high |

This is implemented in: `role_inference_from_hierarchy.pl`.

### Infer an association between persons using their roles that have no uncertainty

Suppose there exists a type of association (`Type`) between two persons (`PersonA` and `PersonB`), which can be represented with the predicate `association(PersonA, PersonB, Type)`. A person has a certain role (i.e. it is not probabilistic), which is represented with the predicate `role(Person, Role)`. From the roles of two persons and an association, an inferred association can be determined with the predicate `inferredAssociation(PersonA, PersonB, InferredAssociation)`.

As an example, there are four persons (1 through 4), where each person has an assigned role as shown on the diagram below.

```
[Role A]              [Role B]
Person 1 --[assoc1]-- Person 2
   |                      |
   |---[inferredAssoc1]---|


[Role C]              [Role D]
Person 3 --[assoc1]-- Person 4
   |                      |
   |---[inferredAssoc1]---|   
```

The graph structure and inferences are implemented in `association_inference.pl`.

### Infer an association between persons with a discrete probability

The events to which a person is associated allows the role of a person to be determined, along with a probability of that role assignment. Two persons can have an association of a given type, which could also have a probability associated with it.

```
   Person ------------ association ------------ Person
      |                     |                      |
      |                     |                      |
      v                     v                      v
  Inferred role ---> inferred association <-- Inferred role
```

In the simplest case, consider the association between two persons to be binary. The inferred role of a person can take on one of three values, where $p \in \{ \text{low}, \text{medium}, \text{high} \}$. If there is just a single association and 3 probability values, that means there are $3 \times 3 = 9$ combinations to consider, as illustrated below where each column represents the probability of an attribute.

| Role 1 | Role 2 | Inferred association |
|--------|--------|----------------------|
| low    | low    | $P_0$                |
| low    | medium | $P_1$                |
| low    | high   | $P_2$                |
| medium | low    | $P_3$                |
| medium | medium | $P_4$                |
| medium | high   | $P_5$                |
| high   | low    | $P_6$                |
| high   | medium | $P_7$                |
| high   | high   | $P_8$                |

This is implemented in `association_inference_with_uncertainty.pl`.

### Infer whether two persons are in the same cluster

This is implemented in `cluster_inference.pl`.

## Demo

The facts are:

* `person(Name, AgeGroup)`
* `event(Person, Role, Event, Datetime)`
* `association(PersonA, PersonB, AssociationType)`

The rules are:

* `inferredRole(Person, Role, Datetime, Probability)`
* `inference(Person, Role, InferenceName, Datetime, Probability)`
* `inferredAssociation(Person1, Person2, Association, Datetime, Probability)`
* `membersOfSameGroup(Person1, Person2, Datetime)`

Role A is inferred from the graph below:

```
event A1 ---|
            |---> inference A1 ---|
event A2 ---|                     |
                                  |---> role A
event A3 ---|                     |
            |---> inference A2 ---|
event A4 ---|                     
```

The probability of inference A1 is:

| event A1 | event A2 | inference A1 |
|----------|----------|--------------|
| 0        | 0        | low          |
| 0        | 1        | medium       |
| 1        | 0        | medium       |
| 1        | 1        | high         |

The probability of inference A2 is:

| event A3 | event A4 | inference A2 |
|----------|----------|--------------|
| 0        | 0        | low          |
| 0        | 1        | medium       |
| 1        | 0        | medium       |
| 1        | 1        | high         |

The probability of role A is given by:

| inference A1 | inference A2 | role A |
|--------------|--------------|--------|
| low          | low          | low    |
| low          | medium       | low    |
| low          | high         | medium |
| medium       | low          | low    |
| medium       | medium       | medium |
| medium       | high         | high   |
| high         | low          | medium |
| high         | medium       | high   |
| high         | high         | high   |

Role B is inferred from two events:

```
event B1 ---|
            |---> role B
event B2 ---|
```

Role C is inferred from one intermediate inference and an event:

```
event C1 ---|
            |---> inference C1 ---|
event C2 ---|                     |---> role C
                                  |
event C3 -------------------------|
```

