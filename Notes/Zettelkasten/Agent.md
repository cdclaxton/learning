#AI

[[LLM]]-powered software that acts upon the real-world, e.g.
* Search web
* Query and update databases
* Send emails
* Call APIs

Core concepts:
- [[Function calling]]
- [[Agent loop]]
- Agentic workflow

Failure modes [Ref: Wengrow2026]:
- Broken tool
- Suboptimal tool
- Ignoring a tool
- Hallucinating a tool (tool doesn't exist)
- Calling the wrong tool
- Too many tools available (some model providers indicate a threshold)
- Passing invalid arguments (number or type)
- Passing suboptimal arguments
- Ignoring tool results
- Drawing incorrect conclusions from the tool
- Running an infinite loop or a loop that is too long
- Using a wrong or suboptimal plan -- give the LLM a plan or tell it to generate a plan

Use [[Evals]] to assess agent performance

To constrain an agent:
- Use a broad approach and prompt it with a high-level sentence
- Use an allow-list (list of things it can do), but this limits the agent's capability (trades flexibility for safety)
- Change the ability to run arbitrary SQL to a set of deterministic functions
- 