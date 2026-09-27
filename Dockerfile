FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY runner_fleet ./runner_fleet
RUN python -m pip install --no-cache-dir .
RUN groupadd --gid 10001 runner-fleet \
    && useradd --uid 10001 --gid 10001 --no-create-home runner-fleet \
    && mkdir -p /data \
    && chown -R 10001:10001 /data

ENV RUNNER_FLEET_DATABASE=/data/runner-fleet.db
EXPOSE 8080

USER 10001:10001

CMD ["uvicorn", "runner_fleet.app:app", "--host", "0.0.0.0", "--port", "8080"]
