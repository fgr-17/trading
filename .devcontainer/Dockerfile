FROM python:3.9-slim

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python3 -m pip install --upgrade build



# RUN /workspace/menu.py