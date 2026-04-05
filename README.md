runner_arm — Self-hosted GitHub Actions Runner for ARM64
==========================================================

## Quick Reference

- **What is a Runner?**
- **What do we use it for?**
- **How to use this image?**
- **Supported architecture**
- **Environment variables**
- **Volumes**

## What is a Runner?

### GitHub's definition

Runners are the machines that execute jobs in a GitHub Actions workflow. For example, a runner can clone your repository locally, install testing software, and then run commands that evaluate your code.

> [GitHub Actions Docs](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners)

![runner](https://docs.github.com/assets/cb-72692/mw-1440/images/help/actions/overview-github-hosted-runner.webp)

## What do we use it for?

Running self-hosted GitHub Actions runners on ARM-based hardware: Raspberry Pi, Orange Pi, Apple Silicon Macs, AWS Graviton instances, and any other ARM64 device.

The image is automatically rebuilt every Monday to track the latest `actions/runner` release.

## How to use this image?

You can use Docker CLI or Docker Compose to create containers based on this image.

### docker-compose (recommended)

```yaml
---
version: '3'
services:
  runner_arm:
    image: neytor/runner_arm
    container_name: runner_arm_container
    restart: always
    environment:
      - runner_user=runner          # optional
      - runner_token=YOUR_TOKEN     # required
      - runner_url=https://github.com/YOUR_ORG_OR_REPO  # required
      - runner_home_dir=/home/runner  # optional
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    privileged: true
```

> **Tip:** You can replace `environment` with `env_file` and point to a `.env` file.

### docker cli

```bash
docker container run \
   --name runner \
   -v /var/run/docker.sock:/var/run/docker.sock \
   -e runner_url=https://github.com/YonierGomez/runner_github \
   -e runner_token=YOUR_TOKEN \
   --privileged \
   -d neytor/runner_arm
```

## Supported Architecture

| Architecture | Available | Pull command |
| ------------ | --------- | ------------ |
| linux/arm64  | ✅        | `docker pull neytor/runner_arm` |

## Environment Variables

| Variable | Required | Default | Description |
| -------- | -------- | ------- | ----------- |
| `runner_user` | No | `runner` | OS user that runs the agent |
| `runner_token` | **Yes** | — | Token from `Settings → Actions → Runners → New self-hosted runner` (Configure section) |
| `runner_url` | **Yes** | — | URL of your org or repository, e.g. `https://github.com/YonierGomez/my-repo` |
| `runner_home_dir` | No | `/home/runner` | Home directory for the runner user |

## Volumes

| Volume | Required | Description |
| ------ | -------- | ----------- |
| `-v /var/run/docker.sock:/var/run/docker.sock` | Only if you run Docker steps inside your jobs | Mounts the host Docker socket into the container |



#### Ejemplo completo

```bash
docker container run \
   --name runner -v /var/run/docker.sock:/var/run/docker.sock \
   -e runner_url=https://github.com/YonierGomez/runner_github \
   -e runner_token=AG7G5YPBONZOYXLPRRQCX53FCCB7W --privileged \
   -d neytor/runner_arm
```

## Environment variables desde archivo (Docker secrets)

Se recomienda pasar la variable `runner_token`a través de un archivo.

[![Try in PWD](https://github.com/play-with-docker/stacks/raw/cff22438cb4195ace27f9b15784bbb497047afa7/assets/images/button.png)](http://play-with-docker.com?stack=https://raw.githubusercontent.com/docker-library/docs/db214ae34137ab29c7574f5fbe01bc4eaea6da7e/wordpress/stack.yml)

## Te invito a visitar mi web

Puedes ver nuevos eventos en [https://www.yonier.com/](https://www.yonier.com)
