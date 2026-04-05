# runner_arm

[![Docker Pulls](https://img.shields.io/docker/pulls/neytor/runner_arm)](https://hub.docker.com/r/neytor/runner_arm)
[![Docker Image Size](https://img.shields.io/docker/image-size/neytor/runner_arm/latest)](https://hub.docker.com/r/neytor/runner_arm)
[![Architecture](https://img.shields.io/badge/arch-linux%2Farm64-blue)](https://hub.docker.com/r/neytor/runner_arm)
[![Auto-updated](https://img.shields.io/badge/updated-weekly-green)](https://github.com/YonierGomez/runner_arm/actions)

A self-hosted **GitHub Actions runner** packaged for **linux/arm64**. Runs natively on Raspberry Pi, Orange Pi, Apple Silicon, AWS Graviton, and any other ARM64 machine — no QEMU, no emulation.

The image is rebuilt automatically every Monday to track the latest [`actions/runner`](https://github.com/actions/runner/releases) release.

---

## Supported Architectures

| Architecture | Tag |
|---|---|
| `linux/arm64` | `latest`, `<version>` |

---

## Quick Start

### docker-compose (recommended)

```yaml
services:
  runner_arm:
    image: neytor/runner_arm:latest
    container_name: runner_arm
    restart: always
    environment:
      - runner_token=YOUR_TOKEN
      - runner_url=https://github.com/YOUR_ORG_OR_REPO
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    privileged: true
```

> **Tip:** swap `environment` for `env_file` and point to a `.env` file to keep secrets out of compose files.

### docker cli

```bash
docker run -d \
  --name runner_arm \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e runner_token=YOUR_TOKEN \
  -e runner_url=https://github.com/YOUR_ORG_OR_REPO \
  neytor/runner_arm:latest
```

---

## How to get the token

1. Go to your repository or organization on GitHub.
2. Navigate to **Settings → Actions → Runners → New self-hosted runner**.
3. Select **Linux** and **ARM64**.
4. Copy the token shown in the **Configure** section.

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `runner_token` | ✅ Yes | — | Registration token generated in GitHub |
| `runner_url` | ✅ Yes | — | URL of the target org or repository |
| `runner_user` | No | `runner` | OS user that owns the runner process |
| `runner_home_dir` | No | `/home/runner` | Home directory for the runner user |

---

## Volumes

| Mount | When needed |
|---|---|
| `/var/run/docker.sock:/var/run/docker.sock` | Only when your jobs need to run Docker commands |

> Mount the socket and add `privileged: true` to give the runner access to the host Docker daemon.

---

## Source

- **GitHub:** [YonierGomez/runner_arm](https://github.com/YonierGomez/runner_arm)
- **Maintainer:** Yonier Gómez


Se recomienda pasar la variable `runner_token`a través de un archivo.

[![Try in PWD](https://github.com/play-with-docker/stacks/raw/cff22438cb4195ace27f9b15784bbb497047afa7/assets/images/button.png)](http://play-with-docker.com?stack=https://raw.githubusercontent.com/docker-library/docs/db214ae34137ab29c7574f5fbe01bc4eaea6da7e/wordpress/stack.yml)

## Te invito a visitar mi web

Puedes ver nuevos eventos en [https://www.yonier.com/](https://www.yonier.com)
