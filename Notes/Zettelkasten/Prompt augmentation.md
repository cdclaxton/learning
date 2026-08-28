#AI

* Add additional details to the [[Prompt]] and then include the user's input, e.g. 
	* Assign a role to an LLM (e.g You are a pirate)
	* Tell it to translate some text or fix the grammar [Wengrow2026]
* Multi-turn dialogue
	* Include entire conversation history in the prompt to overcome statelessness
	* Each subsequent prompt is more expensive (higher [[Cost]]), can take longer to process, and could exceed the context window
* Knowledge-based prompt augmentation
	* Add proprietary / private date to the prompt
* **Developer message** / **system prompt**
	* Add information to the prompt that the user doesn't see
* OpenAPI SDK allows the input to be a **message array** of dicts (with keys 'role' and 'content')
	* Example roles: developer (system prompt), assistant (LLM), user (human)