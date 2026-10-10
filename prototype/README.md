# Policy decision trail spike

This disposable Week 2 prototype asks whether a body-free decision record, tied to the policy revision loaded at startup, gives an operator enough evidence to explain a mask or rejection. It uses synthetic data and a local fake provider. It is prototype code and must never be merged into `main`.

The policy file is JSON-compatible YAML, so the spike uses only the Python standard library. It was tested with Python 3.14.8 and has no third-party dependencies.

## Start with revision r1

In PowerShell, from this directory:

```powershell
$env:DEMO_CALLER_TOKEN = 'replace-with-a-demo-only-value'
python proxy.py
```

The process reads `policy.yaml` once. Changing the file has no effect until the process restarts.

## Send synthetic requests

In another PowerShell window, use the same demo-only value locally:

```powershell
$demoToken = 'replace-with-a-demo-only-value'
$headers = @{
  Authorization = "Bearer $demoToken"
  'Content-Type' = 'application/json'
}
$body = '{"model":"fake","messages":[{"role":"user","content":"Check EMP-123456"}]}'
$response = Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://127.0.0.1:8000/v1/chat/completions -Headers $headers -Body $body
$requestId = $response.Headers['X-Request-ID']
$response.Content
python lookup.py $requestId
```

The response and server console show `[EMPLOYEE-ID]` reaching the fake provider. The lookup names `r1`, `mask-employee-id`, and `redact`, without storing the request or response body.

For the allow path, send content with no matching identifier. For the reject path, omit the Authorization header:

```powershell
$allowBody = '{"model":"fake","messages":[{"role":"user","content":"No identifier here"}]}'
Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://127.0.0.1:8000/v1/chat/completions -Headers $headers -Body $allowBody

try {
  Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://127.0.0.1:8000/v1/chat/completions -ContentType application/json -Body $body
} catch {
  $rejectId = $_.Exception.Response.Headers['X-Request-ID']
  python lookup.py $rejectId
}
```

The rejection record uses caller `unknown`, rule `credential-check`, decision `reject`, and reason code `invalid_caller_credential`. The server console says `provider_called=false`.

## Restart with revision r2

Stop the server with Ctrl+C. Change only the revision, leaving `decisions.jsonl` in place:

```powershell
$policy = Get-Content -Raw policy.yaml | ConvertFrom-Json
$policy.revision = 'r2'
$policy | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 policy.yaml
python proxy.py
```

In the request window, repeat the masked request and capture its new ID:

```powershell
$newResponse = Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://127.0.0.1:8000/v1/chat/completions -Headers $headers -Body $body
$newRequestId = $newResponse.Headers['X-Request-ID']
$newResponse.Content
python lookup.py $requestId
python lookup.py $newRequestId
```

The old record remains on r1 and the new record names r2. An unknown ID produces an explicit message and exit code 1:

```powershell
python lookup.py does-not-exist
$LASTEXITCODE
```

## Run the integration check

```powershell
python -m unittest -v test_spike.py
```

The check exercises masking, allow, rejection without a provider call, restart from r1 to r2 while retaining old records, the exact body-free record schema, successful lookup, and unknown-ID lookup.

To generate evidence pages directly from a fresh run, without manually copying IDs or records:

```powershell
python capture_evidence.py evidence-capture
```

The command runs real r1 and r2 server processes, sends the HTTP requests, verifies the records, and writes sanitized HTML sources plus a local capture manifest. Capture the three HTML pages as PNGs with the required filenames. The manifest is provenance for the screenshots and is local runtime evidence; do not add it to the documentation PR.
