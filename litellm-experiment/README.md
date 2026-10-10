# LiteLLM callback comparison

This disposable SDK-level check asks whether LiteLLM 1.104.2 can write the same body-free decision record as the policy-decision-trail spike. It uses `CustomLogger`, `mock_response`, synthetic messages, and no provider service or key.

## Set up and run

From this directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_comparison.py
```

The runner starts three fresh Python processes. The first loads `policy-r1.yaml` and evaluates a masking rule. The second loads `policy-r2.yaml` and evaluates the same synthetic request. Both use the same append-only decision file, so the old r1 record remains after the r2 process. The third loads r2 and records a credential rejection before any provider completion.

## Result and limitation

The success callback writes the seven required fields after the policy layer passes its dynamically evaluated revision, rule, decision, reason, caller, and request ID through LiteLLM metadata. LiteLLM does not derive those policy facts automatically.

A request rejected before `litellm.completion` produces no success or failure callback. The experiment therefore calls the same body-free logger explicitly from the policy rejection path. A full LiteLLM Proxy could put equivalent logic in a proxy pre-call hook, but this SDK test does not verify that deployment path.

The check requires no service beyond the local Python process. It verifies separate r1/r2 process loads, retained old records, regex-derived mask decisions, pre-provider rejection, the exact record schema, and absence of request bodies, response bodies, and credentials in the log.

Run this to count the custom Python code, excluding blank and comment-only lines:

```powershell
(Get-Content callback_check.py,run_comparison.py | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('#') }).Count
```

`callback-decisions.jsonl`, `.venv/`, and Python caches are disposable runtime output and must not be committed.
