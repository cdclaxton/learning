# Addressable fire alarm system

This simulation is very loosely based on a Kentec LH80161M2 addressable fire
alarm system.

## Local run using WASM

To run the simulation locally using WASM:

```bash
go run github.com/hajimehoshi/wasmserve@latest .
```

and then navigate to http://localhost:8080.

## Build WASM for the web

```bash
./build-wasm.sh
```

Copy to the website repo:

```bash
cp ./web/* ~/website/alarm/
```
