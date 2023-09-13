# Merge JSON files

This code explores how to read two JSON files and merge them into a single JSON 
file.

For example, suppose one file contains:

```json
{
    "queue": {
        "length": 200,
        "port": 5051
    },
    "processor": {
        "threads": 4
    }
}
```

and a second file contains:

```json
{
    "server": {
        "port": 8080,
        "debug": false
    }
}
```

then the merged JSON is:


```json
{
    "queue": {
        "length": 200,
        "port": 5051
    },
    "processor": {
        "threads": 4
    },
    "server": {
        "port": 8080,
        "debug": false
    }    
}
```