---
name: loop
description: Schedule recurring checks in the current Codex task for a job or state that can be queried later, and stop when it reaches a terminal result.
---

# Loop

Use a scheduled task in the current conversation when the user wants to check a durable job or external state over time. A queued compute job, remote test, deployment, transfer, or workflow run can all qualify. An ordinary request to “keep going” or “check again” means continue now unless the user also asks for recurring checks.

## Start a loop

1. Identify the exact target, a way to query its status later, the terminal outcomes, and any requested cadence or deadline. Ask only when a missing detail changes what will be monitored or when the loop should stop.
2. Check the target now unless the user asked to start later. If it is terminal, report the result and do not schedule a loop. If it is still pending, look for an existing matching scheduled task in this conversation; update it instead of creating a duplicate.
3. Create or update a current-conversation heartbeat with the automation tool. Choose a supported cadence that fits the expected change rate. Do not promise a 30-second interval unless the tool supports it. Keep the schedule and conversation target in automation fields, not in the task prompt. Do not create a new conversation or a standalone job solely to choose a model.
4. Prefer GPT-6 Luna for the probe if the same-conversation scheduler offers a per-run model choice. If it does not, keep the same-conversation loop and tell the user that a separate probe model could not be selected. Do not claim that Luna or any other model was selected when the tool did not accept that setting.
5. Save a self-contained prompt that tells each run to check the target once, stay quiet while its status is unchanged and no action is needed, and report meaningful changes in this conversation. On success, failure, cancellation, or another terminal outcome, report the verified result and stop the scheduled task through the available automation control. If the task cannot be stopped, say so rather than claiming the loop ended. If a status query fails repeatedly, report the problem instead of silently polling forever. Never rerun or alter the target job unless the user requested that action.
6. Confirm the created or updated schedule and report the target, cadence, stop condition, and model choice or its limit. Do not rename the conversation unless the user asks.

For a short wait on a command already running in the current turn, wait for that command directly. Use a loop when its status will remain available for a later scheduled check. For inspect, pause, resume, change, or delete requests, resolve the existing scheduled task and preserve fields the user did not change. If the automation tool is unavailable, say so; do not emit raw scheduling directives.
