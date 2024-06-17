# Protobuf example

## Setup

Download the Protobuf compiler (`protoc`) and pop it in the local directory for ease:

```bash
wget https://github.com/protocolbuffers/protobuf/releases/download/v27.1/protoc-27.1-linux-x86_64.zip
unzip protoc-27.1-linux-x86_64.zip -d protoc
rm readme.txt
```

Setup the Go Protobuf compiler:

```bash
export GOBIN=`pwd`
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
export PATH=`pwd`:$PATH
```

Compile the Protobuf message formats to Go code:

```bash
./compile-protobuf.sh
```

Build the executable:

```bash
./build.sh
```

## Run

In one terminal run:

```bash
./app server
```

and in another terminal run:

```bash
./app client

```