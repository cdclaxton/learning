# Optimisation of the key-value store for a graph database.
# 
# Entity files:
# - Entity ID
# - Entity label
#
# Document files:
# - Document ID
# - Document label (+ date)
#
# Links files:
# - Entity ID
# - Document ID
#
# Approach 1: One entry per entity and per document
# - Entity ID: (entity label, document IDs) --> key = e#<entity ID>, value = entity
# - Document ID: (document label, entity IDs) --> key = d#<entity ID>, value = document
#
# Approach 2: Entity and document information stored separately from links.
# - Entity ID: (entity label) --> key = e#<entity ID>, value = entity label
# - Document ID: (document label) --> key = d#<document ID>, value = document label
# - Entity-document link --> key = edl#<entity ID>#<document ID>, value = None
# - Document-entity link --> key = del#<document ID>#<entity ID>, value = None
#

class EntityApproach1:
    """Entity for approach 1."""

    def __init__(self, entity_id, entity_label, documents):
        self.entity_id = entity_id
        self.entity_label = entity_label
        self.documents = documents

    def __repr__(self) -> str:
        return f"EntityApproach1({self.entity_id, self.entity_label, self.documents})"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == EntityApproach1 and \
            self.entity_id == __value.entity_id and \
            self.entity_label == __value.entity_label and \
            self.documents == __value.documents


class DocumentApproach1:
    """Document for approach 1."""

    def __init__(self, document_id, document_label, entities=[]):
        self.document_id = document_id
        self.document_label = document_label
        self.entities = entities

    def __repr__(self) -> str:
        return f"DocumentApproach1({self.document_id}, {self.document_label}, {self.entities})"

    def __eq__(self, __value: object) -> bool:
        return type(__value) == DocumentApproach1 and \
            self.document_id == __value.document_id and \
            self.document_label == __value.document_label and \
            self.entities == __value.entities


class KeyValueStore:
    def __init__(self):
        self.num_reads: int = 0
        self.num_writes: int = 0
        self.num_range_queries: int = 0
        self.store: dict = {}

    def get(self, key: str):
        """Get a value from the store."""

        assert type(key) == str
        self.num_reads += 1
        
        if key in self.store:
            return self.store[key]
        else:
            return None

    def get_startswith(self, beginning: str):
        """Get key-values where the key starts with a certain string."""

        assert type(beginning) == str
        self.num_range_queries += 1

        # Sorted list of keys
        keys = sorted(self.store.keys())

        matching = [(key, self.store[key]) for key in keys \
                    if key.startswith(beginning)]
        self.num_reads += len(matching)

        return matching        

    
    def put(self, key: str, value):
        """Put a value in the store."""

        assert type(key) == str
        self.num_writes += 1

        self.store[key] = value

    def stats(self):
        """Return statistics as a dict."""

        return {
            "num_reads": self.num_reads,
            "num_writes": self.num_writes,
            "num_range_queries": self.num_range_queries
        }

    def __repr__(self):
        return f"KeyValueStore(num_entries={len(self.store)})"
    
    def __str__(self):
        return self.__repr__()


def test_key_value_store():
    store = KeyValueStore()
    assert store.num_reads == 0
    assert store.num_writes == 0

    # Try to get a non-existent value
    assert store.get("a") is None
    assert store.num_reads == 1

    # Put a key-value pair in the store
    store.put("a", "b")
    assert store.num_writes == 1

    assert store.get("a") == "b"
    assert store.num_reads == 2
    assert store.num_writes == 1

    assert store.get_startswith("a") == [("a", "b")]

    store.put("e100#3", "e-1")
    store.put("e101#3", "e-2")
    assert store.get_startswith("e10") == [("e100#3", "e-1"), ("e101#3", "e-2")]

    # Test the store with entities and documents
    store = KeyValueStore()
    e1 = EntityApproach1("e1", "Entity 1", [])
    store.put("e1", e1)
    assert store.get("e1") == EntityApproach1("e1", "Entity 1", [])

    e2 = EntityApproach1("e2", "Entity 2", [])
    store.put("e2", e2)
    assert store.get("e2") == EntityApproach1("e2", "Entity 2", [])

    e1.documents.append("d1")
    store.put("e1", e1)
    assert store.get("e1") == EntityApproach1("e1", "Entity 1", ["d1"])
    assert store.get("e2") == EntityApproach1("e2", "Entity 2", [])

    e = store.get("e2")
    e.documents.append("d3")
    store.put("e2", e)
    assert store.get("e1") == EntityApproach1("e1", "Entity 1", ["d1"])
    assert store.get("e2") == EntityApproach1("e2", "Entity 2", ["d3"])



def generate_data():
    """Generate data for a simple network."""

    # Network:                                  Key:
    #                    /--[d3]--\              e1 = entity 1
    #  e1 ----[d1]---- e2         e3            [d1] = document 1
    #  |                |\--[d4]--/
    # [d2]              |
    #  |               [d5]
    #  |                |
    #  e4 ----[d6]---- e5
    #                   |   /----[d8]----\
    #                 [d7] /              \
    #                   | /------[d9]------\
    #                  e6                  e7
    #                     \------[d10]-----/

    entities = {
        "e" + str(idx): "Entity " + str(idx) for idx in range(1, 8)
    }

    documents = {
        "d" + str(idx): "Document " + str(idx) for idx in range(1, 11)
    }

    link_defns = [
        "e1-d1-e2",
        "e2-d3-e3",
        "e2-d4-e3",
        "e1-d2-e4",
        "e4-d6-e5",
        "e2-d5-e5",
        "e5-d7-e6",
        "e6-d8-e7",
        "e6-d9-e7",
        "e6-d10-e7"
    ]

    # List of links in the form of (entity ID, document ID)
    links = []
    for link_defn in link_defns:
        src, doc, dst = link_defn.split("-")
        links.append((src, doc))
        links.append((dst, doc))    

    # Return a tuple of the entity data, document data and list of links
    return (entities, documents, links)


class BipartiteStoreApproach1:
    """Bipartite store using approach 1."""

    def __init__(self):
        self.store = KeyValueStore()

    def _entity_key(self, entity_id):
        return "e#" + entity_id
    
    def _document_key(self, document_id):
        return "d#" + document_id

    def add_entity(self, entity_id, entity_label, docs):
        entity = EntityApproach1(entity_id, entity_label, docs)
        self.store.put(self._entity_key(entity_id), entity)

    def add_document(self, document_id, document_label, entities):
        doc = DocumentApproach1(document_id, document_label, entities)
        self.store.put(self._document_key(document_id), doc)

    def add_link(self, entity_id, document_id):
        entity = self.store.get(self._entity_key(entity_id))
        assert entity is not None, f"Can't find entity with ID: {entity_id}"

        document = self.store.get(self._document_key(document_id))
        assert document is not None, f"Can't find document with ID: {document_id}"

        entity.documents.append(document_id)
        document.entities.append(entity_id)

        self.store.put(self._entity_key(entity_id), entity)
        self.store.put(self._document_key(document_id), document)

    def get_entity(self, entity_id):
        return self.store.get(self._entity_key(entity_id))
    
    def get_document(self, document_id):
        return self.store.get(self._document_key(document_id))
    

class EntityApproach2:
    def __init__(self, entity_id, entity_label) -> None:
        self.entity_id = entity_id
        self.entity_label = entity_label

    def __repr__(self) -> str:
        return f"EntityApproach2({self.entity_id}, {self.entity_label})"


def entity_approach_2_to_1(entity, documents) -> EntityApproach1:
    """Convert an EntityApproach2 to a EntityApproach1."""
    assert type(entity) == EntityApproach2
    assert type(documents) == list

    return EntityApproach1(entity.entity_id, entity.entity_label, documents)


def document_approach_2_to_1(document, entities) -> DocumentApproach1:
    """Convert a DocumentApproach2 to a DocumentApproach1."""
    assert type(document) == DocumentApproach2
    assert type(entities) == list

    return DocumentApproach1(document.document_id, document.document_label, entities)


class DocumentApproach2:
    def __init__(self, document_id, document_label) -> None:
        self.document_id = document_id
        self.document_label = document_label

    def __repr__(self) -> str:
        return f"DocumentApproach2({self.document_id}, {self.document_label})"


class BipartiteStoreApproach2:
    """Bipartite store using approach 2."""

    # Entity ID: (entity label) --> key = e#<entity ID>, value = entity label
    # Document ID: (document label) --> key = d#<document ID>, value = document label
    # Entity-document link --> key = edl#<entity ID>#<document ID>, value = None
    # Document-entity link --> key = del#<document ID>#<entity ID>, value = None

    def __init__(self):
        self.store = KeyValueStore()

    def _entity_key(self, entity_id):
        return "e#" + entity_id
    
    def _document_key(self, document_id):
        return "d#" + document_id
    
    def _make_entity_document_key(self, entity_id, document_id):
        # Entity-document key for creation
        return "edl#" + entity_id + "#" + document_id

    def _entity_document_key(self, entity_id):
        # Entity-document key for retrieval
        return "edl#" + entity_id + "#"
    
    def _make_document_entity_key(self, document_id, entity_id):
        # Document-entity key for creation
        return "del#" + document_id + "#" + entity_id
    
    def _document_entity_key(self, document_id):
        # Document-entity key for retrieval
        return "del#" + document_id + "#"
    
    def _add_entity_document_link(self, entity_id, document_id):
        self.store.put(self._make_entity_document_key(entity_id, document_id), None)
        self.store.put(self._make_document_entity_key(document_id, entity_id), None)

    def add_entity(self, entity_id, entity_label, docs):
        entity = EntityApproach2(entity_id, entity_label)
        self.store.put(self._entity_key(entity_id), entity)

        # Add all docs
        for d in docs:
            self._add_entity_document_link(entity_id, d)

    def add_document(self, document_id, document_label, entities):
        doc = DocumentApproach2(document_id, document_label)
        self.store.put(self._document_key(document_id), doc)

        # Add all entities
        for e in entities:
            self._add_entity_document_link(e, document_id)

    def add_link(self, entity_id, document_id):
        self._add_entity_document_link(entity_id, document_id)

    def get_entity(self, entity_id: str) -> EntityApproach1:
        assert type(entity_id) == str

        # Get the entity
        entity = self.store.get(self._entity_key(entity_id))
        assert type(entity) == EntityApproach2

        # Get the entity's documents
        document_keys = self.store.get_startswith(self._entity_document_key(entity_id))
        assert type(document_keys) == list
        documents = [key[0].split("#")[2] for key in document_keys]
        
        return entity_approach_2_to_1(entity, documents)
    
    def get_document(self, document_id: str) -> DocumentApproach1:
        assert type(document_id) == str

        # Get the document
        document = self.store.get(self._document_key(document_id))
        assert type(document) == DocumentApproach2
        
        # Get the document's entities
        entity_keys = self.store.get_startswith(self._document_entity_key(document_id))
        assert type(entity_keys) == list

        entities = [key[0].split("#")[2] for key in entity_keys]

        return document_approach_2_to_1(document, entities)


def load(store, entities, documents, links):
    """Load a bipartite store."""

    assert type(entities) == dict
    assert type(documents) == dict
    assert type(links) == list

    # Load the entities
    for entity_id, entity_label in entities.items():
        store.add_entity(entity_id, entity_label, [])

    # Load the documents
    for document_id, document_label in documents.items():
        store.add_document(document_id, document_label, [])

    # Load the links
    for entity_id, document_id in links:
        store.add_link(entity_id, document_id)

    

if __name__ == '__main__':

    # Run tests
    test_key_value_store()

    # Create the test data
    entities, documents, links = generate_data()

    # Approach 1
    bipartite1 = BipartiteStoreApproach1()
    load(bipartite1, entities, documents, links)
    print(f"Approach 1: {bipartite1.store.stats()}")  
    assert bipartite1.get_entity("e1") == EntityApproach1("e1", "Entity 1", ["d1", "d2"])

    # Approach 2
    bipartite2 = BipartiteStoreApproach2()
    load(bipartite2, entities, documents, links)
    print(f"Approach 2: {bipartite2.store.stats()}")   
    assert bipartite2.get_entity("e1") == EntityApproach1("e1", "Entity 1", ["d1", "d2"]), bipartite2.get_entity("e1") 
    
    # Run an integrity check
    for entity_id, _ in entities.items():
        e1 = bipartite1.get_entity(entity_id) 
        e2 = bipartite2.get_entity(entity_id) 
        assert e1 == e1, f"e1 = {e1}, e2 = {e2}"
    
    for document_id, _ in documents.items():
        d1 = bipartite1.get_document(document_id)
        d2 = bipartite2.get_document(document_id)
        assert d1 == d2, f"d1 = {d1}, d2 = {d2}"
    