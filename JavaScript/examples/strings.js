// String concatenation
"Hello, " + "World!";  // 'Hello, World!'

// charAt() -- character at position
"Nice job".charAt(5); // j

// charCodeAt() -- returns an integer between 0 and 65535 representing the UTF-16 code unit at given index
"Nice job".charCodeAt(5);  // 106

// indexOf() -- index of first occurrence (case sensitive)
"Hello, World!".indexOf("W");  // 7
"Hello, World!".indexOf("w");  // -1

// lastIndexOf() -- index of last occurrence
"This is very good".lastIndexOf("s"); // 6

// length -- string length (not a method)
"Hello, World!".length;  // 13

// replace() -- regular expression matching replace
"Good morning".replace(/morning/gi, "afternoon");  // 'Good afternoon'

// search() -- regular expression matching
"good mode mood".search("mo{2}d");  // 10

// slice() -- extracts a section of a string
"Good morning".slice(5);  // 'morning'
"Good morning".slice(5, 7);  // 'mo'

// split() -- turns a String into an array of strings
"dog".split("");  // [ 'd', 'o', 'g' ]
"dog cat".split(" ");  // [ 'dog', 'cat' ]

// substring(start, end) -- substring
"This is very nice".substring(8,12);  // 'very'

// toLowerCase()
"VERY nice".toLowerCase();  // 'very nice'

// toUpperCase()
"nice work".toUpperCase(); // 'NICE WORK'