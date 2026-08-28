#AI

Hard constraints:
* Language the LLM was trained on

Soft constraints
* Quality of LLM's responses
	* Accuracy
	* Relevance
	* Adherence to prompt instructions
	* Safety
* [[Cost]]
* Latency
	* Number of tokens / second (speed)
	* Streaming tokens vs. entire response in one go
		* **Time to first token** (TTFT) when streaming
* **Context window** -- maximum prompt size 
* Specialised models:
	* Reasoning models -- breaks a problem down into steps; tends to be slower and more expensive; can 'overthink'

**LLM gateways**:
- Make it easier to switch models or providers (e.g. if one goes down)