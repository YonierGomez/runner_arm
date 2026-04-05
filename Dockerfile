FROM alpine:latest

LABEL maintainer="Yonier Gómez"

ARG RUNNER_VERSION

ENV runner_token="" \
    runner_user=runner \
    runner_home_dir=/home/runner \
    runner_url=https://github.com/YonierGomezOrganization \
    # Suppress .NET diagnostics warning when lttng-ust is absent
    COMPlus_EnableDiagnostics=0

# gcompat     → glibc compatibility shim (runner binary is glibc-linked)
# libgcc / libstdc++ → C++ runtime required by .NET (runner core)
# icu-libs    → globalization support for .NET
# krb5-libs   → Kerberos (used by some GitHub auth flows)
# zlib        → compression
# docker-cli  → allows jobs to run Docker commands
RUN apk add --no-cache \
    bash curl tar ca-certificates \
    gcompat libgcc libstdc++ \
    icu-libs krb5-libs zlib \
    docker-cli

# Create docker group + unprivileged runner user
# adduser without -G auto-creates a group with the same name (runner:runner)
# then we add runner to docker as a supplementary group
RUN addgroup docker && \
    adduser -D -h "$runner_home_dir" -s /bin/bash "$runner_user" && \
    adduser "$runner_user" docker

# Download and extract the runner
RUN [ -n "${RUNNER_VERSION}" ] || { echo "ERROR: RUNNER_VERSION build-arg is required"; exit 1; } && \
    mkdir -p "$runner_home_dir/actions-runner" && \
    cd "$runner_home_dir/actions-runner" && \
    curl -fL -o runner.tar.gz \
      "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-arm64-${RUNNER_VERSION}.tar.gz" && \
    tar xzf runner.tar.gz && \
    rm runner.tar.gz && \
    chown -R "$runner_user:$runner_user" "$runner_home_dir/actions-runner"

USER $runner_user
WORKDIR $runner_home_dir/actions-runner

CMD ./config.sh --url "$runner_url" \
    --token "$runner_token" --name "$runner_user" --runnergroup default \
    --labels 'self-hosted,Linux,ARM64' --work _work && ./run.sh
