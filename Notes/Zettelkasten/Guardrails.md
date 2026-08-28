#AI 

Help control AI behaviour

- **Inference time guardrails** -- define rules in the system prompt as to how it should generate text
	- Similar to [[LLM fine-tuning]]
- **Pre-inference / input guardrails** -- filter user input before using it in a prompt. Could be as simple as checking for the presence of certain keywords or using an LLM to detect undesirable topics (as in [[LLM-as-a-judge]]). A specialised LLM with one focus might have a better chance of detecting undesirable output, but increases cost and latency. Use to detect:
	- Undesirable topics
	- [[Prompt injection]] attempts
	- Personally Identifiable Information (PII) -- e.g. usernames and passwords, passport numbers, addresses (could be a problem if using [[LLM-as-a-service]] and so use [[Self-hosting LLMs]])
- **Post-inference / output guardrails** -- filter the generated output text

Could use non-LLM ML models to detect undesirable topics.

**Jailbreaking** -- act of bypassing guardrails

LLM guardrail frameworks exist

Test using:
- **Redteaming** -- develop own adversarial prompts
- Evals
- Monitoring -- find issues in production and then adapt guardrails
