grammar ArrayInit;

// Parser rule that matches comma-separated values between { ... }
init : '{' value (',' value)* '}'  ;

// A value is either a nested array or a simple integer
value : init
      | INT
      ;

// Lexer rules
INT : [0-9]+ ;  // Define token INT as one or more digits
WS : [ \t\r\n]+ -> skip ;  // Whitespace rule (ignored)
