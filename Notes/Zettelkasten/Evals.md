#AI

Evals = Evaluation system

To develop example queries for chatbot:
- If automating an existing system, use actual user queries and logs
- Consider categories of questions (product support, refunds, etc.)
- Devise customer personas (e.g. tech savvy, age, demographics, communication level), e.g. using an LLM

Run each query and generate a [[Trace]]

**Open coding** (assigning a label to a trace):
* Need to decide **failure modes**
	* Inclusion of irrelevant details
	* Tone (e.g. too formal or too informal)
	* Factual mistake
* Annotate trace with whether the test passes or what failure occurred

**Axial coding**:
- Review open codes and group into a smaller set of categories (e.g. one category could be Hallucinates)
- Place PASS or FAIL in the appropriate axial code for each trace
- Over time look for which axial codes are increasing or decreasing in frequency

Correct errors using:
- [[Prompt engineering]]

**Reference-based evals**
- Where accuracy can be tested using deterministic code
- LLM is used to generate an element from a category or to generate a tool call
- Can be tested using a unit testing framework

Automate tests that can't use deterministic code using [[LLM-as-a-judge]] -- ask it to decide whether a failure mode is present