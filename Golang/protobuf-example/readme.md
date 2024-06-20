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
./app server localhost:5000
```

and in another terminal run:

```bash
./app client localhost:5000

```

To run the server on a Windows machine, in Git Bash run `ifconfig` and note the IP address of the machine under `Wireless LAN adapter WiFi -> IPv4 address`. Run the server using `./app server 0.0.0.0:5000` and on another machine run `./app client <IP>:5000`.

On a Mac, click `System Settings -> Wi-Fi -> Details ...` and the see the `IP address` field.