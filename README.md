# Boiler

## About

Boiler is a Docker orchestration software built on top of nginx & docker-compose.

## Prerequisites

You need a server with `git`, `python-pip`, `docker`, `docker-compose` & `nginx` installed.

## Usage

Deploy a project

```bash
python boiler.py [boil|deploy] [repository-url] [options]
```

Here's the options available:
- `project_name`: The project name. Default to the repository's name.
- `tag_or_branch`: The tag or the branch to deploy. Default to `master`.
- `skip_clean`: Skip the clean at the end of the deployment. `1` or `0`. Defaults to `0`.
- `skip_build`: Skip the docker build. `1` or `0`. Defaults to `0`.s

Example with Arena

```bash
python boiler.py git@github.com:thefirstspine/arena.git --tag_or_branch=1.0.0
```

## About `.boiler` directory in projects

Each project needs a `.boiler` directory with:

- a `docker-compose.yml` file that contains the services
- a `Dockerfile` to build the app
- and an optional `nginx` file that will be copied in the Nginx config directory

## Configuring a project

Each project needs a dotenv file in the `configs` directory. For example, the `arena` project will need a `config/arena.env` file to work. It's a safe way to manage credentials and other sensitive data across containers.
