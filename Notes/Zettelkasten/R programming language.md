#Programming

- `all.equal(x,y)` -- equal up to the precision of the computer (e.g. for floats)
- `c()` -- combine, e.g. to make a vector
- Negative indices in vector means don't include
- Elements of a vector can have optional names (set using `names()`)
- Convert a vector to a factor: `factor(x, levels=c(...), ordered=TRUE)`
	- Use `as.numeric(x)` to get the factor indices
	- Convert factor to a vector: `as.vector(x)`
- `list` -- vector where elements can be of different types and named
	- Access named elements with `$`
	- Get contents by numerical index using `[[i]]`
	- Get name and contents using `[i]`
- `aggregate()` -- groups data by factors and applies a function
- `proc.time()` -- use to time functions