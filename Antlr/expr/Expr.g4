grammar Expr;
import LexerRulesExpr;

// The start rule (begin parsing here)
prog : stat+ ;

stat : expr NEWLINE          # printExpr
     | ID '=' expr NEWLINE   # assign
     | NEWLINE               # blank
     ;

expr : expr ('*'|'/') expr   # MulDiv
     | expr ('+'|'-') expr   # AddSub
     | INT                   # int 
     | ID                    # id
     | '(' expr ')'          # parens
     ;
    
