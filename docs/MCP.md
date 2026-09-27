# MCP Interface

The MCP server provides read-only operational context to AI clients.

## Tools

| Tool | Purpose | Mutates infrastructure |
| --- | --- | --- |
| `get_fleet_status` | Latest queue, runner, failure, and cost snapshot | No |
| `get_slo_report` | Current targets, actuals, and breaches | No |
| `recommend_runner_capacity` | Advisory capacity calculation | No |
| `list_recent_incidents` | Synthetic SLO-breach evidence | No |
| `get_cost_estimate` | Latest synthetic compute estimate and exclusions | No |

## Local stdio configuration

```json
{
  "mcpServers": {
    "runner-fleet-reliability": {
      "command": "C:\\PersonalAI\\Portfolio\\runner-fleet-reliability-platform\\.venv\\Scripts\\runner-fleet-mcp.exe",
      "args": [],
      "env": {
        "RUNNER_FLEET_DATABASE": "C:\\PersonalAI\\Portfolio\\runner-fleet-reliability-platform\\data\\runner-fleet.db"
      }
    }
  }
}
```

## Safety decision

Tools do not expose `kubectl`, Helm, OpenTofu, AWS APIs, runner registration,
or scaling mutations. An AI client may explain evidence and recommend a
capacity target, but a person must review and execute changes through the
normal infrastructure workflow.
