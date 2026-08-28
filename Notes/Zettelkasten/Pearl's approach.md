#Bayesian

Handles uncertain information (soft evidence)

```mermaid
graph LR
	f(("f")) --> g(("g"))
```

The CPT for $g$ is given by:

|     |     | $g$   |       |
| --- | --- | ----- | ----- |
|     |     | 0     | 1     |
| $f$ | 0   | $r$   | $1-r$ |
|     | 1   | $1-r$ | $r$   |
$r$ is the probability of observing factor $f$ correctly.