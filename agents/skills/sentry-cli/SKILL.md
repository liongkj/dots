---
name: sentry-cli
description: Inspect Sentry error-tracking issues, events, traces, and releases with the native sentry CLI. Use for sentry.io issue links and Sentry investigations, not SolarSENS Observers.
---

# Sentry CLI

Use the installed `sentry` command. It owns authentication and reads its stored OAuth session automatically. A missing `SENTRY_AUTH_TOKEN` environment variable does not mean the CLI is signed out.

For an issue link, read the organization and numeric issue ID from the URL, then run:

```sh
sentry issue view <org>/<issue-id> --fresh --json --fields id,shortId,title,status,priority,culprit,count,firstSeen,lastSeen,project
```

Discover additional commands with `sentry <command> --help`. Issue detail can include the latest event. Select scalar evidence fields, for example `event.dateCreated,event.occurrence.evidenceData.numRepeatingSpans` for a captured N+1 query.

Do not select whole `event.tags`, `event.entries`, or request objects for display. Tags can contain user IPs and request parameters. If a task needs a value inside an array, capture JSON in a process and filter it before printing. Do not print raw event payloads, credentials, emails, or IP addresses.

If a request fails authentication, check the existing CLI session before asking the user to configure anything:

```sh
sentry auth status --json --fields authenticated,source,configPath
```

If the stored session is signed out, use `sentry auth login` with the user's authorization. Never request a token in chat or use `--show-token`. Do not route an API investigation through browser sign-in when the CLI is authenticated.

An issue link or check request is read-only. A code repair does not authorize resolving or archiving the Sentry issue, deployment, or production mutation. Report the issue's current state, captured evidence, source cause when traced, and the limits of verification.
