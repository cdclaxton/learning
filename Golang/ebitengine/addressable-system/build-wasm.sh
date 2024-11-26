#!/usr/bin/bash

echo Building WASM file ...
env GOOS=js GOARCH=wasm go build -o ./web/alarm.wasm .

cp /usr/local/go/misc/wasm/wasm_exec.js ./web