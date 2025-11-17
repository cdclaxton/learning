# ArchiMate

## Introduction

- Open standard maintained by The Open Group
- Describes the architecture of organisations:
  - Business processes
  - Organisational structures
  - Information flows
  - IT systems
  - Technical infrastructure
- ArchiMate provides:
  - Language to describe architectures
  - Framework to organise concepts
  - Graphical notation
  - Visualisations for different stakeholders

* Level of detail:

- Details:
  - small part of the architecture with a high level of detail
  - e.g. for software engineer designing and implementing a component
- Coherence:
  - spans multiple aspects or layers and shows their relations
  - e.g. for an operational manager responsible for IT support across a number of business processes
- Overview:
  - abstract, comprehensive view of multiple aspects and layers
  - for enterprise architects and upper-level managers

* Model:

  - Collection of **concepts** (element or relationship)
  - Element:
    - behaviour
    - structure
    - motivation
    - composite
  - More common to model types (class) rather than instances

* Layers:
  - **Strategy** -- model an organisation's capabilities
  - **Motivation**
  - **Business** (Yellow) -- business services offered to customers, which are realised in the organisation by business processes performed by business actors
  - **Application** (Blue)
    - services that support the business
    - software applications that support business processes
    - interfaces that permit the exchange of information between applications
  - **Technology** + **Physical** (Green)
    - processing, storage, communication services required to run applications
    - computer, communication hardware and system software to realise those services.
  - **Implementation and migration** -- program, portfolio and project management elements
  - **Physical** -- models equipment, facilities, distribution networks and materials

- BDAT:
  - Business -- strategy, organisation, processes, governance, standards
  - Data -- logical and physical assets, data management resources
  - Application --
  - Technical -- hardware, software, network infrastructure

* Core framework **aspects**

  - **Active structure** (Square corners) -- subject ('who')
    - business actors, application components, devices
    - **collaboration** = aggregate of 2+ internal active structure elements
    - **interface** = 1+ services exposed to environment
    - **external** -- interfaces (expose behaviour)
    - **internal** -- business actors, application components,
  - **Behaviour** (Round corners) -- verb ('how')

    - processes, functions, events, services performed by actors
    - dynamic aspects
    - **process** = sequence of behaviours that achieves a specific result
    - **function** = collection of behaviour based on criteria
    - **interaction** = unit of collective behaviour
    - **service**
    - **event** -- state change
    - behaviour types:
      - **external** -- service
      - **internal** -- unit of activity performed by one or more active structural elements
      - **events** -- state change

  - **Passive structure** (Square corners) -- object ('what')

    - objects on which behaviour is performed
    - accessed by behaviour elements
    - information objects in Business Layer
    - data objects in Application Layer
    - physical objects

- **Business** layer -- model operational organisation in a technology-independent manner

  - Active structure elements -- static structure of the organisation (entities and their relationships)

    - **Business actor** -- business entity that is capable of performing behaviour; e.g. humans, departments, business units; includes entities outside of the organisation (e.g. customers, partners, companies, regulators); actor can be assigned 1+ roles; can be specific individuals or organisations or be more generic (e.g. customer / supplier);

    - **Business role** -- responsibility for performing specific behaviour or the part an actor plays in a particular action or event; abstract sort of actor;

    - **Business collaboration** -- aggregate of 2+ business internal active structure elements that work together to perform collective behaviour; specialisation of a Business Role;

    - **Business interface** -- point of access where a business service is made available; exposes functionality of a service to business roles or actors; channel (e.g. telephone, Internet, local office); visible manifestation of a role;

  - Behaviour elements:

    - **Business process** -- defined based on products or services; represents a sequence (flow) of business behaviours that achieve a specific result (products or services);

    - **Business function** -- functionality for 1+ business processes; groups behaviour based on required skills, resources, application support, etc.;

    - **Business interaction** -- unit of collective business behaviour performed by 2+ business actors, business roles or business collaborations; roles in the collaboration share the responsibility for performing the interaction;

    - **Business event** -- something that happens externally; may influence business processes, functions or interactions;

    - **Business service** -- externally visible behaviour; explicitly defined behaviour that a business role, business actor or business collaboration exposes to the environment; can be external, customer-facing services or internal support services;

  - Passive structure elements:

    - **Business object** -- concept used within a particular domain; typically models an object type (class as opposed to instance); e.g. payment, bank account, bill;

    - **Contract** -- formal/informal specification of agreement between provider and consumer that specifies rights and obligations associated with a product; specialisation of a Business Object;

    - **Representation** -- perceptible form of the information carried by a business object; representation that can be shared with others;

    - **Product** -- coherent collection of services and/or passive structure elements, accompanied by a contract/set of agreements, offered whole to customers (internal or external);

- **Application** layer:

  - Active structure elements:

    - **Application component** -- encapsulation of application functionality, modular, replaceable; performs 1+ application functions; exposes services and makes them available through interfaces; use to model entire applications or individual parts.

    - **Application collaboration** -- aggregate of 2+ application elements that work together to perform collective behaviour; specialisation of an Application Component;

    - **Application interface** -- point of access where application services are made available to use, component or node; includes APIs, GUIs, web service;

  - Behaviour elements:

    - **Application function** -- automated behaviour that can be performed by an application component; describes internal behaviour of component;

    - **Application interaction** -- unit of collective application behaviour performed by 2+ application components;

    - **Application process** -- sequence of application behaviours that achieves a specific result; internal behaviour performed by application component;

    - **Application event** -- represents application state change; event is instantaneous; can be generated externally or internally;

    - **Application service** -- represents explicitly defined exposed application behaviour;

  - Passive structure elements:

    - **Data object** -- data structured for automated processing;

- **Implementation and migration** elements: supports the implementation and migration of architectures;

  - **Work package** -- series of actions identified and designed to achieve specific results within specified time and resource constraints; can be used to model sub-projects or tasks within a project; unique one-off process; produces a deliverable;

  - **Deliverable** -- precisely-defined result of a work package; e.g. reports, papers, services, software, physical products; can produce intangible results, e.g. organisation change;

  - **Implementation event** -- state change related to implementation or migration; instantaneous; work packages may be triggere or interrupted by an implementation event;

  - **Plateau** -- stable state of the architecture that exists during a limited period of time; allows for individual work packages and projects to be grouped into managed programs;

  - **Gap** -- statement of difference between two plateaus (e.g. baseline and target architectures or consecutive transition architectures);

- Grouping:
  - aggregates or composes concepts that belong together
- Location:
  - conceptual or physical place where concepts are located or performed
- Relationships:

  - Structural
    - **Realisation** -- entity plays a critical role in creation, achievement, sustenance, or operation of a more abstract entity
      - business process realises a business service
      - data object realises a business object
      - core element realises a motivation element
    - **Assignment** -- allocation of responsibility, performance of behaviour, storage, execution; active -> behaviour -> passive;
    - **Aggregation** (part-of) -- element combines 1+ concepts,
    - **Composition** (has-a) -- element consists of 1+ concepts, whole/part relationship; child cannot exist independently of the parent;
  - Dependency
    - **Association** -- dependency; unspecified relationship;
    - **Influence** -- impact dependency; element affects the implementation or achievement of some motivation element (not critical); can be ++, +, 0, -, -- or [0,10]
    - **Access** -- data dependency; ability of behaviour and active structure elements to observe or act upon passive structure elements; always depicts a behavioural element accessing a passive element;
    - **Serving** -- control dependency; element provides its functionality to another element
  - Dynamic -- model behavioural dependencies
    - **Triggering** -- temporal or causal relationship between elements; some part of the source element should be completed before the target element can start;
    - **Flow** -- represents transfer from one element to another; flow of information, goods, money; does not imply causal relationship
  - Other
    - **Specialisation** -- element is a particular kind of another element

- Relationship connectors:

  - Junction -- used to connect relationships of the same type
  - AND junction -- all elements must participate
  - OR junction -- at least one of the elements participates

- Core framework **layers**:
  - Strategy
  - Business
  - Application
  - Technology
  - Physical
  - Implementation and migration

```
                       OBJECT                           SUBJECT
                        NOUN              VERB           NOUN
|                | Passive structure | Behaviour | Active structure |
|----------------|-------------------|-----------|------------------|
| Business       |                   |           |                  |
| Application    |                   |           |                  |L A Y E R S
| Technology     |                   |           |                  |
                                  A S P E C T S
```
