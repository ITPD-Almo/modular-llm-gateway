# Assumptions

These are the six assumptions from the Week 1 value proposition, in the same order. None has been verified. The [October 9 meeting](../reports/week-02/meeting-report.md) clarified the plugin workflow, but did not settle these six beliefs. The checks and owners below are proposed team tasks, not Customer decisions.

## ASM-01

The Customer needs policy revision and decision evidence but can accept a narrow event trail.

- **Status:** Open
- **How to check:** In a proposed Week 3 follow-up, Ali12hamdan will show a concrete decision record and ask about a recent incident and body retention. The brief agreement with the text flow did not settle this belief; see the [open questions](../reports/week-02/meeting-report.md#open-questions).

## ASM-02

A LiteLLM callback or existing Azure controls do not already satisfy the same workflow with acceptable effort.

- **Status:** Open
- **How to check:** In Week 3, atkond2point0 will check a LiteLLM callback with the same event fields, and Mohammed-Nour will check Azure policy-version correlation. [DEC-004](decisions.md#dec-004) allows using an existing tool if it fits; the check still needs evidence.

## ASM-03

Static caller credentials and one provider are acceptable for the initial trial.

- **Status:** Open
- **How to check:** In a proposed Week 3 follow-up, Mohammed-Nour will ask about callers, identity integration, and the first real provider. [DEC-005](decisions.md#dec-005) permits a fake provider for the first interaction; it does not accept static credentials for a real trial.

## ASM-04

The narrow starter takes fewer mandatory services or manual steps than a matched existing gateway setup.

- **Status:** Open
- **How to check:** Ali12hamdan and Mohammed-Nour, who took over spaghetti-n-spaghetti's tasks, will compare services and manual steps for the same policy job in Week 3, following the team plan. Report the result even if LiteLLM wins.

## ASM-05

A fixed-format masking rule serves a real trial need.

- **Status:** Open
- **How to check:** In a proposed Week 3 follow-up, atkond2point0 will ask for synthetic examples and expected masking results. Do not collect real personal data. The masking illustration did not verify this belief; see the [open questions](../reports/week-02/meeting-report.md#open-questions).

## ASM-06

Three people can deliver the bounded trial with policy error handling and tests.

- **Status:** Open
- **How to check:** The whole team will estimate the Must Have stories in Week 3, following the team plan, before choosing a language or promising a delivery date.
