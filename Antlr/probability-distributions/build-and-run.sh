java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser ProbabilityDistributions.g4
go build
./probabilitydistributions