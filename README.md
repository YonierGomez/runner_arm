Runner - Agente github action basado en arm
======================

## Referencia rápida

-	**¿Qué es un Runner?**
-	**¿Cuál es nuestro uso?**
-	**¿Cómo usar esta imagen?**
-	**Arquitectura soportada**
-	**Variables**
- **Volumenes**
-	**Te invito a visitar mi web**

## ¿Qué es un runner?

### Definición de GiHub

Los Runner son las máquinas que ejecutan trabajos (jobs) en un flujo de trabajo de Acciones de GitHub (GitHub Actions workflow). Por ejemplo, un ejecutor puede clonar tu repositorio localmente, instalar software de pruebas y, a continuación, ejecutar comandos que evalúen tu código.



> [GitHub Action Doc](https://docs.github.com/es/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners)

![runner](https://docs.github.com/assets/cb-72692/mw-1440/images/help/actions/overview-github-hosted-runner.webp)

## ¿Cuál es nuestro uso?

Crear runners basados en arquitecturas ARM como en una raspberry, orange pi, mac con arquitecturas arm, graviton, etc.

![Polymart Downloads](https://img.shields.io/polymart/downloads/323)

## ¿Cómo usar esta imagen?

Puede hacer uso de docker cli o docker compose para crear sus contenedores basados en esta imagen.

### Login por defecto

Para acceder a su recurso compartido siga la sintaxis descrita en la tabla:

### docker-compose (recomendado)

```yaml
---
version: '3'
services:
  runner_arm:
    image: neytor/runner_arm
    container_name: runnger_arm_container
    restart: always
    environment:
    	- runner_user=runner #OPCIONAL
    	- runner_token=SDJFDFYVEJHSD #OPCIONAL
    	- runner_url=https://github.com/YonierGomez/docker-cat-container #OPCIONAL
    	- runner_home_dir=/home/runner #OPCIONAL
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    privileged:  true
...
```

> Nota: Puedes reemplazar environment por env_file y pasarle un archivo .env como valor, recuerde que el archivo .env debe tener las variables deseadas.

### docker cli

```bash
docker container run \
   --name runner -v /var/run/docker.sock:/var/run/docker.sock \
   -e runner_url=https://github.com/YonierGomez/runner_github \
   -e runner_token=AG7G5YPBONZOYXLPRRQCX53FCCB7W --privileged \
   -d neytor/runner_arm
```

## Arquitectura soportada

La arquitectura soportada es la siguiente:

| Arquitectura | Disponible | Tag descarga                 |
| ------------ | ---------- | ---------------------------- |
| arm64        | ✅          | docker pull neytor/runner_arm

## Variables

Puedes pasar las siguientes variables al crear el contenedor

| Variable      | Función                                                      |
| ------------- | ------------------------------------------------------------ |
| `-e runner_user`     | Opcional: Define el usuario con el que se ejecutará el runner, por defecto `runner`         |
| `-e runner_token` | Obligatorio: Es el token que generas en tu proyecto, `SETTING -> ACTIONS -> RUNNERS -> new self-hosted runner`. Lo puedes visualizar en el apartado de **configure** |
| `-e runner_url`  | Obligatorio: La url de su proyecto, ej https://github.com/YonierGomez/runner_github |
| `-e runner_dir`      | Opcional: Por defecto `/home/runner` |

## Volumenes

Puedes pasar las siguientes variables al crear el contenedor

| Variable      | Función                                                      |
| ------------- | ------------------------------------------------------------ |
| `-v /var/run/docker.sock:/var/run/docker.sock`     | Solo es obligatorio si desea ejecutar tareas de Docker en su job.         |



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
