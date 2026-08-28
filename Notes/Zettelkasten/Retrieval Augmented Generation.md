#AI 

Augment the [[Prompt]] only with relevant information (chunks) to the user's input

Use a search engine
* Keyword / lexical / term search -- search for exact word
* Semantic search (using [[Embeddings]])
* Hybrid search uses the above two

Measures:
* **Recall** = retrieved relevant docs / all relevant docs (how good it is at not missing relevant docs)
* **Precision** = retrieved relevant docs / all retrieved docs (how good it is at not including irrelevant docs)

The larger top-K, the greater the chance the search engine has to get good recall, but it might lower the precision

**Query expansion** (**Agentic RAG**):
- Use an LLM to construct the search query given the conversation (this could include determining tags so they can be used to filter docs in the vector database)
- Use a faster, cheaper LLM
- Let the LLM choose the top-K parameter
- Perform an additional search if all retrieved chunks are relevant (as there may be some missed chunks)
- Rewrite the query if none of the retrieved chunks are relevant
- Detect user prompts that are too vague and so RAG shouldn't be performed (saves time and money)