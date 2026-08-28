#AI 

Logging many details about the [[LLM]]-powered app [Wengrow2026]:
- Timestamp
- Version of the codebase
- Specific LLM(s) used
- [[LLM sampling parameters]], [[LLM temperature]]
- System [[Prompt]]
- User input
- Tool calls and tool outputs ([[Function calling]])
- Data retrieved in [[Retrieval Augmented Generation]] pipelines
- Interventions performed by [[Guardrails]]
- Errors and stack traces
- Conversation history rewrites
- Number of tokens at each step
- Cost and latency of each step

Set up alerts to trigger on:
- Cost
- Latency
- Post-inference guardrails activated

Arize Phoenix -- open-source observability cloud-based platform