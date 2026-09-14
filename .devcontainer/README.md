# Running Meridian

Meridian spans five languages. Rather than install five toolchains, this
repository ships a container that has all of them, pinned to one version, so it
behaves the same on every machine. Getting it running should take one step.

## Run it (recommended)

Install Docker (Docker Desktop, or OrbStack on a Mac), then from this folder:

```sh
docker build -t meridian-dev -f .devcontainer/Dockerfile .
docker run --rm -p 8080:8080 -p 8081:8081 -v "$PWD":/workspace -w /workspace \
    meridian-dev sh -c "make all && ./run.sh"
```

- `build` reuses cached layers after the first time, so it returns in seconds.
- `run` compiles the FORTRAN model, the C collector and the Java services,
  generates a season of telemetry, ingests it, runs the forecast, and starts
  the API and the console.

Leave that terminal running, then open **http://localhost:8080** in your
browser. The API is on **http://localhost:8081**.

To start over from clean data (for example after changing the station list),
clear the generated files first:

```sh
docker run --rm -p 8080:8080 -p 8081:8081 -v "$PWD":/workspace -w /workspace \
    meridian-dev sh -c "rm -f data/*.bin data/*.db; make all && ./run.sh"
```

## What `make` and `run.sh` do

- `make all` builds the FORTRAN model, the C collector, and the Java services.
  (The console has no build step.)
- `run.sh` generates the telemetry spool, ingests it, runs the forecast, and
  starts the API (8081) and the console (8080).

You do **not** need Java, gfortran, Node, Python, or sqlite3 installed on your
own machine. They live in the container.

## VS Code (optional)

There is a `devcontainer.json` here if you use the VS Code **Dev Containers**
extension ("Reopen in Container"). It works, but the first connection can hang
while VS Code downloads its server into the container on some networks. If that
happens, use the plain `docker` commands above instead — they are the
supported path.
