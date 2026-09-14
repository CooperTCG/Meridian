# Running Meridian

Meridian spans five languages. Rather than install five toolchains, this
repository ships a container that has all of them, pinned to one version, so it
behaves the same on every machine. Getting it running should take one step.

## Option A — VS Code (recommended)

1. Install **Docker Desktop** (or OrbStack) and the VS Code **Dev Containers**
   extension.
2. Open this folder in VS Code and choose **Reopen in Container** when prompted.
   The first build takes a couple of minutes; after that it is instant.
3. In the container terminal:

   ```sh
   ./run.sh
   ```

4. Open <http://localhost:8080> for the console. The API is on
   <http://localhost:8081>.

## Option B — GitHub Codespaces (no local install)

Open the repository in a Codespace. The same container is built for you in the
browser. Run `./run.sh` in the terminal and use the forwarded ports.

## Option C — plain Docker (no VS Code)

```sh
docker build -t meridian-dev -f .devcontainer/Dockerfile .
docker run --rm -it -p 8080:8080 -p 8081:8081 -v "$PWD":/workspace -w /workspace meridian-dev bash
# then, inside the container:
make all && ./run.sh
```

## What `make` and `run.sh` do

- `make all` builds the FORTRAN model, the C collector, and the Java services.
  (The console has no build step.)
- `run.sh` generates a season of telemetry, ingests it, runs the forecast, and
  starts the API and the console.

You do **not** need Java, gfortran, Node, Python, or sqlite3 installed on your
own machine. They live in the container.
