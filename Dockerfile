FROM python:3.12-slim
WORKDIR /code
RUN pip install --no-cache-dir uv
COPY pyproject.toml ./
RUN uv sync --no-dev
COPY app ./app
ENV PATH="/code/.venv/bin:$PATH"
CMD ["python", "-c", "print('job-agent image ready')"]
