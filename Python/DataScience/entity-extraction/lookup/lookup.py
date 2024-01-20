class Lookup:
    """Holds two lookups."""

    def __init__(self):
        self.token_to_entries = {}
        self.entry_to_tokens = {}

    def add(self, entry_id, tokens):
        """Add an entry to the lookup."""
        assert type(entry_id) == int
        assert type(tokens) == list
        assert len(tokens) > 0

        # Store the tokens for the entry
        assert entry_id not in self.entry_to_tokens, f"entry {entry_id} already exists"
        self.entry_to_tokens[entry_id] = tokens

        # Store the entry for the tokens
        for t in tokens:
            if t not in self.token_to_entries:
                self.token_to_entries[t] = set()

            self.token_to_entries[t].add(entry_id)

    def tokens_for_entry(self, entry_id):
        """Get tokens for an entry given its ID."""

        assert type(entry_id) == int
        return self.entry_to_tokens.get(entry_id, None)

    def entries_for_token(self, token):
        return self.token_to_entries.get(token, None)

    def matching_entries(self, tokens):
        """Find the matching entries in the lookup given the tokens."""

        assert type(tokens) == list
        assert len(tokens) > 0

        # Get the entries for each token
        for idx, t in enumerate(tokens):
            es = self.entries_for_token(t)

            if es is None:
                return None

            if idx == 0:
                entries = es
            else:
                entries = entries.intersection(es)

            # No entries match, so there's no point looking at any further tokens
            if len(entries) == 0:
                return None

        return entries
