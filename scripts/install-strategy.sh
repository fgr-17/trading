
printf "Building Broker Package"

cd $STRATEGY_DOCKER_PATH && ls
# python3 -m build
pip install --upgrade .
if [ $? -ne 0 ]; then
    printf "Couldn't build broker package, exiting...\n"
    exit 1
fi