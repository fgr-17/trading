
printf "Building Broker Package"

cd $BROKER_DOCKER_PATH

# python3 -m build
pip install --upgrade -e .
if [ $? -ne 0 ]; then
    printf "Couldn't build broker package, exiting...\n"
    exit 1
fi