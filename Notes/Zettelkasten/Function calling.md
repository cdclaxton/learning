#AI

AKA **Tool use**

LLM acts as an [[Agent]]

Technically, the LLM itself doesn't call a function, but instead creates text that can be parsed by the chatbot to call a function

Steps (without using an in-built tools API):
1. User asks question that requires the use of a tool
2. LLM outputs arbitrary special notation, e.g. `<<multiply(10,20)>>`
3. Special notation is detected in the main conversation loop
4. Function called, e.g. `multiply(10,20)`
5. Insert answer into a new user prompt
6. Call the LLM and tell it that it should use the answer provided
7. LLM outputs the final response

Use built-in API if one is provided

Avoid sending PII as a parameter and instead use a UID. The tool should then look up the PII given the UID.