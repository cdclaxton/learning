# HTTP sub-routers using Gorilla Mux

```bash
# Run the HTTP server
go run main.go

# In a new terminal, run the following:
curl -XGET http://localhost:8000/a
curl -XGET http://localhost:8000/1/b
curl -XGET http://localhost:8000/1/c
curl -XGET http://localhost:8000/1/d
```