# Use una imagen Ubuntu para ARM64 como base
FROM arm64v8/ubuntu:latest

LABEL maintainer="Yonier Gómez"

ENV runner_token=AG7G5YNU4ULPQGRSSHI3HLLFCAAC6 \
    runner_user=runner \
    runner_home_dir=/home/runner \
    runner_url=https://github.com/YonierGomezOrganization

# Actualiza el sistema e instala las dependencias
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    curl lsb-release apt-transport-https ca-certificates software-properties-common && \
    apt-get clean

# Crea usuario, asigna permisos, Descarga y configura el runner
RUN groupadd -g 999 docker && useradd -mU -d $runner_home_dir $runner_user && \ 
    mkdir -p $runner_home_dir/actions-runner && \
    cd $runner_home_dir/actions-runner && \
    curl -o actions-runner-linux-arm64-2.309.0.tar.gz -L \
    https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-arm64-2.309.0.tar.gz && \
    tar xzf ./actions-runner-linux-arm64-2.309.0.tar.gz && \
    chown -R $runner_user:$runner_user $runner_home_dir/actions-runner && \
    usermod -aG docker $runner_user && \
    ./bin/installdependencies.sh

# Agrega la clave GPG oficial de Docker, agrega el repositorio de Docker,
# y luego instala Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean

# Cambia al usuario "$runner_user" y establece el directorio de trabajo
USER $runner_user
WORKDIR $runner_home_dir/actions-runner

# CMD para iniciar el servicio de Docker dentro del contenedor
CMD ./config.sh --url $runner_url \
    --token $runner_token --name $runner_user --runnergroup default \
    --labels 'self-hosted,Linux,ARM64' --work _work && ./run.sh && dockerd