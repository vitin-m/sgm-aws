FROM python:3.13-alpine AS builder

WORKDIR /src

COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --frozen --no-install-project --no-dev

# Source .venv
ENV PYTHONPATH=/src PATH="/src/.venv/bin:$PATH"

# Install package
ADD . /src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Run stage
FROM python:3.13-alpine

# Copy package
COPY --from=builder --chown=app:app /src /src

WORKDIR /src
# Source .venv
ENV PYTHONPATH=/src PATH="/src/.venv/bin:$PATH"

CMD ["fastapi", "dev", "--host", "0.0.0.0", "app/main.py"]