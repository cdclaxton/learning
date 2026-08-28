#AI

Modifying prompts in an iterative process to achieve better responses to:
- Eliminate ambiguity
- Put RAG chunks into the developer [[Prompt]] (maybe improve the chunks themselves to be more precise)
- Rewrite the conversation history
- Use XML-style tags / Markdown to define sections within a long prompt
- Use bullet points in the prompt to separate instructions
- Move instructions to the beginning or end of the prompt or repeat in both places
- Instruct the LLM to be faithful to the RAG chunks
- Emotional pleas and threats
- Ask LLM to cite sources
- Few-shot prompting -- give the LLM example responses
- Give the LLM permission to say "I don't know"
- Use [[Chain-of-thought prompting]]

Look at model-specific prompt engineering guides

Test **automated prompt optimisation** (e.g. in OpenAI developer dashboard)

Using the above techniques may increase the size of the prompt, thus increasing its [[Cost]]
