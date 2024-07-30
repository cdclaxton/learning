#!/bin/bash

# Number of requests to make
n_requests=100;

# Number of Curl requests to make in parallel
parallelism=3;

function check {
    r=`curl -s -o /dev/null -D - http://localhost:5000/ | grep '200'`
    if [ ${#r} -eq 0 ]; then
        echo "Failure occurred"
    fi
}

export -f check

seq 1 ${n_requests} | xargs -I {} -P ${parallelism} bash -c 'check'