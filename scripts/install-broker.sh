
printf "Building Broker Package"

BROKER_DOCKER_PATH="/workspace/src/broker"
cd $BROKER_DOCKER_PATH

# python3 -m build
pip install --upgrade .
if [ $? -ne 0 ]; then
    printf "Couldn't build broker package, exiting...\n"
    exit 1
fi