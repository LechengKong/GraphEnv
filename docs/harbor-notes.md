# Harbor and infrastructure notes

Tested with Harbor 0.27.0, Docker 29 with Compose v5, on Slurm compute nodes.

## Task features used
- **Sidecar.** `environment/docker-compose.yaml` adds an `oracle` service next to Harbor's `main`
  service. `main` has `depends_on: oracle: condition: service_healthy`, and the oracle image
  defines a `HEALTHCHECK`.
- **Separate verifier.** In `task.toml`, `[verifier] environment_mode = "separate"`. With a
  `tests/Dockerfile`, the verifier image is built from `tests/`, so the hidden instance ships
  there and never enters the agent's image.
- **Artifacts from a service.** `[[artifacts]] source = "/state", service = "oracle"`. Harbor
  collects `/state` from the oracle after the agent phase and re-materializes it at `/state` in
  the separate verifier container.
- **Portability.** The tasks need a Compose-capable environment provider. Local Docker works;
  many cloud sandboxes don't.

## Running agents on Bedrock
- **Credentials.** Harbor's `claude-code` agent uses Bedrock when `CLAUDE_CODE_USE_BEDROCK=1`. It
  forwards `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` and `AWS_REGION` into
  the container. `tools/aws_env.py` exports temporary credentials from the current AWS profile,
  and `tools/run_agent.sh` wires it together.
- **Model names.** Use `-m bedrock/us.anthropic.claude-opus-5-5`.
- **Retries.** Use `--max-retries 2`, because Bedrock occasionally returns "unexpected error during
  processing" mid-run.
- **Credential lifetime.** Temporary credentials last about an hour. Use one Slurm job per batch
  of trials so each batch gets fresh credentials.

## Gotchas we hit
- **Hanging globs.** A recursive glob over `/` (`/**/x`) walks `/proc` and hangs. Search specific
  directories instead.
- **Live progress.** The agent log (`/logs/agent/claude-code.txt`) is only copied to the host at
  the end of a trial. To watch progress live, run `docker exec` into the trial's `main` or
  `oracle` container on the compute node (`srun --jobid=<id> --overlap`).
- **Container CPUs.** Containers get `cpus = 2`. Agents that launch dozens of parallel processes
  stall, and that is a real failure mode under the timeout.
- **Editing scripts mid-run.** Don't edit a shell script while a job is executing it. Bash reads
  scripts incrementally.
