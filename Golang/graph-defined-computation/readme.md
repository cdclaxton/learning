# Graph-defined computation

This experiment explores how computation can be defined in the form of a graph. 
An example of a graph is shown below.

```
 [Node 0   ] ---\
 [Extractor]     \
                 |---> [Node 3     ] ---\
                 /     [Computation]     \
 [Node 1   ] ---/                        |---> [Node 5     ]
 [Extractor]                             /     [Computation]
                       [Node 4   ] -----/
                       [Extractor]
```

An **Extractor** node takes a `Data` object and calculates a value from that 
data. In this project, the type that is passed between nodes is simply an `int`.

The types of extractors that are defined:

* ConstantExtractor -- produces the same `int` value, regardless of the `Data`;
* NumValuesExtractor -- produces the number of occurrences of a given element
in the `Data`;
* CountExtractor -- produces the total number of occurrences in the `Data`.

The data that is passed to the extractors is abstracted to an `interface` so
that the graph computation can handle a variety of different types of data, such
as lists, set, and graphs (e.g. DAGs).

A **Computation** node combines the results from its inputs given the required
mathematical function. The computation nodes that are defined are:

* Add
* Multiply

The graph is defined in a JSON file, an example of which is:

```json
{
    "computeNodes": [
        {
            "name": "a",
            "takesData": true,
            "computationType": "",
            "extractionConfig": {
                "type": "ConstantExtractor",
                "value": "2"
            }
        },
        {
            "name": "b",
            "takesData": true,
            "computationType": "",
            "extractionConfig": {
                "type": "NumValuesExtractor",
                "value": "a"
            }
        },
        {
            "name": "c",
            "takesData": false,
            "computationType": "Add",
            "extractionConfig": {}
        }
    ],
    "connections": [
        {
            "source": "a",
            "destination": "c"
        },
        {
            "source": "b",
            "destination": "c"
        }
    ]
}
```

The nodes are defined in the `computeNodes` object and `connections` defines the
directed links between nodes.

Extractor nodes have the form:

```json
{
    "name": "User-friendly name for the node",
    "takesData": true,
    "computationType": "",
    "extractionConfig": {
        "type": "Type of extractor node",
    }
}
```

The `extractionConfig` object contains configuration details for the extraction
node and the specific fields are dependent on the type of extractor defined
in `type`.

Computation nodes have the form:

```json
{
    "name": "User-friendly name for the node",
    "takesData": false,
    "computationType": "Computation type",
    "extractionConfig": {}
}
```

The `computationType` field must have a value that matches one of the predefined
computation types.
