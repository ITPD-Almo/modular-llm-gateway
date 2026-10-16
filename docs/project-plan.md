# Project plan

## Milestones

### MLS-03

- **Due:** 2026-10-17
- **Sprints:** [SPRINT-03](#sprint-03)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01)

A DevOps operator starts the gateway with two plugins listed in a configuration file, sends a request to a fake provider, and sees each plugin's effect on the request and the response.
The plugin interface is documented, so a plugin can be written against it rather than against the core, per [DEC-006](decisions.md#dec-006).
Restarting after a configuration change is allowed, per [DEC-005](decisions.md#dec-005).

### MLS-05

- **Due:** 2026-10-30
- **Sprints:** [SPRINT-04](#sprint-04), [SPRINT-05](#sprint-05)
- **Advances:** [TOS-04](threshold-of-success.md#tos-04)

The gateway runs in a deployed environment that continuous integration updates from `main`, and a failing plugin there fails only its own request.

### MLS-07

- **Due:** 2026-11-13
- **Sprints:** [SPRINT-06](#sprint-06), [SPRINT-07](#sprint-07)
- **Advances:** [TOS-02](threshold-of-success.md#tos-02), [TOS-03](threshold-of-success.md#tos-03)

People outside the team run the gateway and write a plugin of their own from the documentation alone, observed in the usability test.

## Sprints

### SPRINT-03

A DevOps operator starts the gateway with two plugins from a configuration file, sends a request to the fake provider, and sees each plugin's effect.

- **Due:** 2026-10-17
- **Sprint Backlog:** [the issues scheduled into SPRINT-03](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/1)

#### REL-03

### SPRINT-04

A plugin that raises an error or times out fails only its own request with a clear error, and the quality goals and architecture draft describe the plugin pipeline.

- **Due:** 2026-10-23

#### REL-04

### SPRINT-05

Provisional: the gateway is deployed from `main` by continuous integration and processes a request through two plugins in that environment.

- **Due:** 2026-10-30

#### REL-05

### SPRINT-06

Provisional: the operator sees how often each plugin changed or rejected a request, from the gateway's own usage events.

- **Due:** 2026-11-06

#### REL-06

### SPRINT-07

Provisional: the usability-test protocol is ready, and outside participants can run the gateway and write a plugin from the documentation.

- **Due:** 2026-11-13

#### REL-07

### SPRINT-08

Provisional: every release can be rebuilt from its tag, with its configuration and plugin versions recorded.

- **Due:** 2026-11-20

#### REL-08

### SPRINT-09

Provisional: the final release addresses the usability findings and is frozen for the final demonstration.

- **Due:** 2026-11-27

#### REL-09

## Progress Monitoring

- **Review:** the team's weekly review, every Wednesday at 19:00 online, before the Friday customer meeting; it reads [threshold-of-success.md](threshold-of-success.md) and [risks.md](risks.md) and settles what changed.
- **Checked by:** the `Accountable` member of each scheduled issue reports its state, and the team walks the sprint's GitHub milestone against the sprint's goal.
- **Visible at:** the [GitHub project's table view](https://github.com/orgs/ITPD-Almo/projects), grouped by milestone, and the [sprints' GitHub milestones](https://github.com/ITPD-Almo/modular-llm-gateway/milestones).
