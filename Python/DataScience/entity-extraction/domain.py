from typing import Callable, Dict, List, NewType


# List of tokens
Tokens = List[str]

# Function to generator N text tokens
TextGenerator = Callable[[int], Tokens]

# Function to generate an entity
EntityGenerator = Callable[[], Tokens]

# Dict of entity ID to tokens for the entity
EntityToTokens = Dict[str, Tokens]
