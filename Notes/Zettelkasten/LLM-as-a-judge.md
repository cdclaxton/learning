#AI 

One model judges the output of another model

Could use a stronger model or a reasoning model

The judge also needs to be evaluated using the approach:
1. Create the LLM judge system prompt
2. Run the LLM judge on labelled traces (called the ground-truth judgment) and calculate TP, TN, FP, and FN
3. Iterate the prompt, e.g. with few-shot examples
4. Check the accuracy on the held-out validation set