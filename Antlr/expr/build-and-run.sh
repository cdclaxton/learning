clear
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Expr.g4
go run main.go