# CLI example using Cobra

This example shows how to build a command line interface (CLI) using the Golang Cobra library.

```bash
# Show help
go run main.go --help
go run main.go add --help
go run main.go sub --help

# Run the root command
go run main.go

# Add two numbers using a subcommand
go run main.go add 2 3
go run main.go add 2.25 3.189 -r

# Subtract two numbers using a subcommand
go run main.go sub 2.25 3.189
go run main.go sub 2.25 3.189 -r
```