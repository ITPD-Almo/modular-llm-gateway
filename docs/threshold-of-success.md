# Threshold of success

## TOS-01

The Customer accepts the first usable plugin workflow: start the gateway, add two plugins, send a request, and see the result.

- **Status:** Open
- **Measure:** an accepted verdict, recorded as a `DEC-nnn`, on every candidate story of [MLS-03](project-plan.md#mls-03), by the end of Week 4, 2026-10-23.

## TOS-02

A person outside the team runs the gateway from a clean checkout and completes the core task by following the documentation alone.

- **Status:** Open
- **Measure:** one usability-test session in which a participant outside the team follows `docs/setup.md`, sends a request through two plugins, and sees the result without help, by the end of Week 7, 2026-11-13.

## TOS-03

A developer outside the team writes a working plugin from the plugin documentation without changing the gateway core.

- **Status:** Open
- **Measure:** one plugin, written by a developer outside the team against `docs/plugins.md`, that loads from the configuration file and changes a request, with no commit to the core, by the end of Week 7, 2026-11-13.

## TOS-04

The gateway runs in a deployed environment and processes requests through its configured plugins there.

- **Status:** Open
- **Measure:** a request sent to the deployed gateway passes through two plugins and returns the fake provider's response, shown in the release notes of `REL-05`, by the end of Week 5, 2026-10-30.

## Failure And Success Statements

| Goal              | Success statement                                                                   | Failure statement                                                       |
| ----------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [TOS-01](#tos-01) | The Customer accepts the plugin workflow as usable.                                 | The Customer never accepted the plugin workflow.                        |
| [TOS-01](#tos-01) | The Customer sees the plugins' effect on a real request in a running gateway.       | We only ever showed slides and text concepts, never a running gateway.  |
| [TOS-02](#tos-02) | Someone outside the team runs the gateway by following the setup page.              | Nobody outside the team could run the gateway.                          |
| [TOS-03](#tos-03) | An outside developer writes a plugin from the documentation alone.                  | A plugin could only be written by reading the core, not the docs.       |
| [TOS-04](#tos-04) | The gateway runs somewhere other than a team member's laptop.                       | The gateway only ever ran on a team member's laptop.                    |
| —                 | The gateway forwards to a real LLM provider.                                        | The gateway never talked to a real LLM provider.                        |
| —                 | A failing plugin returns an error for its request without stopping the gateway.     | One broken plugin took the whole gateway down.                          |
