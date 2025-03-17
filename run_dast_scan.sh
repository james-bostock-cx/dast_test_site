#!/bin/bash

if [[ -z "$API_KEY" ]]
then
	echo "API_KEY not set"
	exit 1
fi

# Note that the current directory is mounted on /demo so, if the config file
# is in the current directory, the --config argument shoud be /demo/<file>

docker run -e CX_APIKEY=$API_KEY --rm \
       	-v $(pwd):/demo checkmarx/dast:latest \
       	web \
       	--output=/demo/test_output \
       	--timeout=10000 \
       	--update-interval=10 \
       	--jvm-properties=-Xmx3G \
	"$@"
