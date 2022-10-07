FROM python:3.9-slim

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

RUN printf "\nalias ls='ls --color=auto'\n" >> ~/.bashrc
RUN printf "\nalias ll='ls -alF'\n" >> ~/.bashrc

ENV BROKER_DOCKER_PATH="/workspace/src/broker"
ENV STRATEGY_DOCKER_PATH="/workspace/src/strategy"
# CMD ["cd $BROKER_DOCKER_PATH && pip install ."]
