FROM python:3.12.13-slim-bookworm@sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2 AS build

WORKDIR /build
COPY requirements-runtime.txt ./
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --only-binary=:all: --no-deps -r requirements-runtime.txt

COPY pyproject.toml ./
COPY gateway ./gateway
RUN python -m pip install --no-cache-dir setuptools==80.9.0 \
    && python -m pip wheel --no-deps --no-build-isolation --wheel-dir /wheels . \
    && /opt/venv/bin/pip install --no-cache-dir --no-deps /wheels/*.whl \
    && /opt/venv/bin/pip check

FROM python:3.12.13-slim-bookworm@sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2

ARG SOURCE_COMMIT
LABEL org.opencontainers.image.source="https://github.com/ITPD-Almo/modular-llm-gateway" \
      org.opencontainers.image.revision="${SOURCE_COMMIT}"

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/opt/llmgw \
    XDG_CONFIG_HOME=/run/llmgw

WORKDIR /opt/llmgw
COPY --from=build /opt/venv /opt/venv
COPY examples ./examples

USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=2s --start-period=10s --retries=3 \
    CMD ["llmgw", "health"]
ENTRYPOINT ["llmgw"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000", "--provider", "fake"]
