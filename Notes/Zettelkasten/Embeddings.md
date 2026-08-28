#AI #ML

Used in RAG:
* Divide corpus into chunks (need to choose a **chunking strategy**, e.g. sections, chapters)
* Convert each chunk to an embedding vector using a model:
	* Dense -- designed for semantic search
	* Sparse -- ideal for keyword search
* Store embeddings in a **vector database** (e.g. Pinecone)
* Use database to find chunks relevant to a query
	* Need to choose K in the top-K results
	* If K is too low, then chunks will be missed
	* If K is too high, the prompt will be unnecessarily long, thus costing more and taking longer