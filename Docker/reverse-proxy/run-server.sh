while true; do
	cat index.http | nc -l -v -q 1 8080;
done
