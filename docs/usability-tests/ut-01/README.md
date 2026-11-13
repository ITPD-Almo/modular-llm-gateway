# UT-01: Configure and use the gateway unaided

- **Status:** Planned
- **Design sprint:** [SPRINT-07](../../project-plan.md#sprint-07)
- **Run sprint:** [SPRINT-08](../../project-plan.md#sprint-08)

## Goal

A representative operator can configure the gateway, complete its primary flow and show a plugin result without help.

## Research questions

1. Can a representative operator complete the main flow independently within the time limit?
2. Can the operator diagnose a plugin failure and recover using the documentation?
3. Can the operator integrate a small custom plugin without changing gateway core?

## The Requirement

This test serves [QR-09](../../quality-requirements/qr/QR-09.md). Its pass bar is **at least 2/3 of at least 3 valid
participants completing the main task unaided**.

The design assesses the configured request/response flow in [FR-001](../../functional-requirements/fr/FR-001.md), the
plugin contract in [FR-003](../../functional-requirements/fr/FR-003.md), visible plugin changes in
[FR-005](../../functional-requirements/fr/FR-005.md) and bounded hook execution in
[FR-007](../../functional-requirements/fr/FR-007.md).

## Participant Profile

Recruit adult developers or DevOps operators with basic terminal and Python skills who are unfamiliar with this gateway and
plausibly configure integrations or write plugins. Recruit through university developer groups, lab contacts or classmates
who match the profile. Target five valid sessions and require at least three representative participants aged 18 or older.
Sessions use the team's laptop or a supported campus staging workstation on the university network. A teammate, Customer,
instructor or course staff member is not a counted participant. An exploratory session outside this profile is not counted.
Assign `P-01`, `P-02` and later codes in booking order; retire unused, refused, withdrawn or broken-session codes and never
reuse them.

## The Tasks

The tasks are identical and run in this fixed order. The facilitator reads each scenario verbatim. Interface labels, screens,
procedure steps and step counts remain in facilitator material, not in the participant-facing scenarios.

### Main task - bring up the gateway and show a plugin result

- **Scenario:** You have received this gateway and want to try it with a harmless synthetic message. Make it available and
  show what the configured plugins changed.
- **Start point:** A clean synthetic workspace and setup guide are supplied; the service is not running.
- **End state:** The participant sends a synthetic chat through both bundled plugins, identifies the visible transformation
  and shows the plugin trace.
- **Time limit:** 12 minutes.
- **Help rule:** Neutral clarification of the scenario and a think-aloud prompt are allowed. A hint, suggested command,
  interface explanation or facilitator action that advances the task is assistance and is recorded.
- **Success criterion:** `Unaided` if the full end state is reached within 12 minutes with only the supplied materials and
  neutral facilitation; `Assisted` if it is reached within the limit after recorded help; `Failed` if a valid attempt ends
  without the full end state.

### Secondary task 1 - diagnose a slow plugin and recover

- **Scenario:** A configured hook has become slow. Determine what happened and make the gateway usable again.
- **Start point:** A freshly reset slow-plugin fixture and supported examples are available.
- **End state:** The participant shows the named slow-plugin 504, a healthy check and a successful follow-up chat.
- **Time limit:** 8 minutes.
- **Help rule:** Use the main-task help rule; every hint or facilitator action is recorded.
- **Success criterion:** `Unaided`, `Assisted` or `Failed` using the definitions above.

### Secondary task 2 - add a small custom plugin

- **Scenario:** You want a small third-party plugin to change a request before it reaches the fake provider.
- **Start point:** A separate disposable fake-provider workspace, plugin guide and synthetic marker goal are supplied.
- **End state:** A configured plugin changes a request and the fake reply contains the assigned marker without a gateway-core
  change.
- **Time limit:** 15 minutes.
- **Help rule:** Use the main-task help rule; every hint or facilitator action is recorded.
- **Success criterion:** `Unaided`, `Assisted` or `Failed` using the definitions above.

Define `Unaided` as reaching the full end state within the limit with only supplied materials and neutral facilitation.
Define `Assisted` as reaching it within the limit after a hint, suggested command or facilitator action that advances the
task. Define `Failed` as a valid attempt ending without the full end state. Stop on the limit, withdrawal, missing consent or
a broken environment; distinguish an invalid session from a valid failed task.

The 2026-11-13 teammate dry run is uncounted and is not evidence. Its actual wording, timing, reset and telemetry outcome
must be recorded in the private session record and applied here before the first counted session.

## Protocol

Every counted session is in person, on the university network, against staging, with the clean seed reset before each
session and instrumentation verified before timing. The facilitator welcomes the participant, checks durable consent and the
recorder, administers the [pre-test](surveys.md#pre-test), gives the [think-aloud instruction](sessions/README.md#script),
reads the three scenarios in order, observes without solving the task, records start/stop times and assistance, administers
the [SEQ](surveys.md#seq-after-each-task) after each task, then administers [SUS](surveys.md#sus-after-all-tasks) and the
[open-ended post-test](surveys.md#open-ended-post-test), and closes with a debrief.

The facilitator reads the scenario verbatim, answers only questions about the scenario and does not solve the task. At least
two team members attend each session. Stop on the time limit, participant withdrawal, missing consent or a broken
environment; record the reason. A session stopped before complete data is not a valid completed session.

## Measures

Each session records task outcome, help, time, SEQ after every task, SUS responses and score, pre-test background,
think-aloud observations and open-ended post-test responses. The quality requirement reads the main task's unaided
completion rate; all other measures are diagnostic. The analysis reports main-task median time, every task's median SEQ,
SUS mean and median with `n`, and the qualitative themes.

## Instrumentation

Main task and secondary task 1 use the dedicated staging test instance and reuse the Week 6 events
[`gateway_configuration_used`, `gateway_chat_started` and `gateway_chat_finished`](../../analytics.md#the-events), with
`source=usability-test` and `environment=staging`. The first configured chat, started/finished attempt, visible result, slow
plugin timeout and recovery are kept in the staging export. Operational usage queries exclude the test source; the test
funnel is read separately.

Before timing, the facilitator supplies the reviewed checkout, preloaded image, free port and private Compose settings path.
The participant starts the instrumented service, checks health and sends the synthetic chat. The session window is captured
as `[start, end)` in UTC Unix microseconds. Another facilitator retrieves the allowlisted slice by those bounds, then joins
opaque run and attempt IDs; the `P-nn` and window mapping remain private. The export contains no names, content, IP,
location, user agent, referrer, credentials or raw logs.

Secondary task 2 uses a separate disposable fake-provider workspace with telemetry disabled and no shared credentials. Ali's
facilitator-side `ut01_plugin_probe` writes a private timestamped `marker_seen` record joined by the same session window; it
stays outside the analytics registry. HTTP events and the local probe cannot establish documentation discovery, help,
reasoning or the source of plugin-workflow friction; the observer and surveys cover those blind spots.

The uncounted teammate dry run checks wording, limits, reset and telemetry delivery/linking. With the default SPRINT-08 run,
a separate instrumentation verification is required before the first counted session and by the start of SPRINT-09.

## Analysis Plan

Count only valid sessions: profile match, age declaration, durable consent, recording, complete data and no technical break.
The denominator includes valid assisted and failed attempts; withdrawals, missing consent/recording, broken sessions and
missing required data are excluded and their codes are retired. Report main-task unaided, assisted and failed counts and
rates, main-task median time, each task's median SEQ, and SUS mean/median with `n=<count>`.

The QRT passes only when **at least 2/3 of at least 3 valid participants completing the main task unaided** is met. Code
themes from observation, friction, help and sanitized quotes as Critical, Major or Minor with a reason. Compare telemetry
with observation, name instrumentation blind spots, state the small-sample limitation and conclude only from valid sessions.
Publish only sanitized evidence in SPRINT-08; no result is claimed in this design sprint.

## Schedule

The teammate dry run is Friday 2026-11-13 and is explicitly uncounted. Recruit five eligible participants and arrange at
least three valid in-person sessions in SPRINT-08 on the university network against staging. Results are due by 2026-11-21.
Reset the clean seed and verify instrumentation before the first counted session. If sessions move into another sprint,
update this field and the index.

## Roles

- **Facilitator:** Mohammed-Nour for every counted session.
- **Observer and environment operator:** Ali12hamdan.
- **Raw-notes and recordings custodian:** atkond2point0.

The actual roles used in the uncounted dry run are recorded privately.

## Environment

Use the reviewed staging deployment on the university network, a clean supplied workspace, the pinned preloaded image, a
reserved loopback port and the reset synthetic fixture. Main and secondary task 1 use staging; secondary task 2 uses a
separate disposable fake-provider workspace. No real provider key, user content, payment or production data is used.

## Consent And Data

The [consent template](consent.md) is completed before each counted session. It covers participation, age, recording,
sanitized results, optional anonymized quotes, private repository and cloud-folder access, team/instructor access, tools,
withdrawal, deletion of tool copies and deletion after grading. Recording and consent to sanitized results are required;
declining optional quotes is allowed. Identities, consent records, recordings, raw notes, filtered telemetry and the mapping
are private and never committed here.

The private text repository is [ITPD-Almo/modular-llm-gateway-usability-data](https://github.com/ITPD-Almo/modular-llm-gateway-usability-data).
Its text-only layout contains consent, identity mapping, raw notes, filtered telemetry, working analysis and the recordings
folder link/access instructions. The team-owned recordings folder and instructor-access confirmation are private-only and
are supplied through Moodle/team channels. After grading, delete the private repository, its history and recordings while
keeping this sanitized public record.

## Evidence Map

| Evidence | Location |
| --- | --- |
| Design and protocol | This record and [session instructions](sessions/README.md) |
| Surveys | [surveys.md](surveys.md) |
| Consent template | [consent.md](consent.md) |
| Counted sanitized notes | `sessions/P-nn.md`, added after sessions |
| Results, findings and triage | [results.md](results.md), currently an empty template |
| Private text evidence | [private usability-data repository](https://github.com/ITPD-Almo/modular-llm-gateway-usability-data) |
| Recordings | Team-owned cloud folder, linked only in private submission |
| Quality verdict | [QR-09 QRT-01](../../quality-requirements/qr/QR-09.md#qrt-01) |
