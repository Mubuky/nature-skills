# Scheduling a literature pipeline

<!-- New in this derivative; see ../../../NOTICE. -->

Choose the scheduler available in the user's environment: a native recurring
task, cron/systemd timer, CI schedule, cloud job, or an explicitly requested
agent scheduler. Do not assume a product or machine uptime.

## Deployment contract

Record:

- timezone and recurrence;
- command or workflow entry point;
- configuration and archive paths;
- secret source without recording secret values;
- delivery authorization;
- lock/concurrency policy;
- retry and timeout limits;
- last-success and failure-log locations;
- manual dry-run and disable procedure.

## Safe rollout

1. Run the pipeline once in dry-run mode with a small candidate budget.
2. Verify saved query, dedup, reading labels, output paths, and delivery preview.
3. Obtain authorization before enabling external delivery or knowledge-base
   writes.
4. Create the schedule with overlap prevention.
5. Inspect the first real run and record its outcome.

On repeated source failure, degrade to the remaining sources and label the
coverage loss. Do not retry indefinitely or deliver a stale digest as current.
