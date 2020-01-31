# Boiler

## About

Boiler is a Docker orchestration software built on top of nginx & docker-compose.

## Prerequisites

You need a server with `git`, `python-pip`, `docker`, `docker-compose` & `nginx` installed.

## Usage

Deploy a project

```bash
python boiler.py [repository-url]
```

Example with Arena

```bash
python boiler.py git@github.com:thefirstspine/arena.git
```

## About `.boiler` directory in projects

Each project needs a `.boiler` directory with:

- a `docker-compose.yml` file that contains the services
- a `Dockerfile` to build the app
- and an optional `nginx` file that will be copied in the Nginx config directory
