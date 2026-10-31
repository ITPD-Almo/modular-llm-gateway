#!/usr/bin/env bash
# Executes QR-02 QRT-01's HTTP requests; never changes VM configuration.
# Usage: bash campus-qr02.sh STAGING_URL FULL_SHA GITHUB_USERNAME campus|local|tailnet
set -euo pipefail
umask 077
if (( $# != 4 )); then
    printf '%s\n' 'Usage: campus-qr02.sh STAGING_URL FULL_SHA GITHUB_USERNAME campus|local|tailnet' >&2
    exit 2
fi
STAGING_URL=${1%/}
RELEASE_COMMIT=$2
RUNNER=$3
NETWORK=$4
python3 - "$STAGING_URL" "$RELEASE_COMMIT" "$RUNNER" "$NETWORK" <<'PY'
import ipaddress,re,sys
from urllib.parse import urlsplit
url,sha,runner,network=sys.argv[1:]
p=urlsplit(url)
if (p.scheme not in ('http','https') or not p.hostname or p.username or p.password
        or p.query or p.fragment or p.path not in ('','/')):
    raise SystemExit('Use a base URL without embedded credentials or a path')
if not re.fullmatch('[0-9a-f]{40}',sha) or not re.fullmatch('[A-Za-z0-9-]{1,39}',runner):
    raise SystemExit('Use the full source SHA and a GitHub username')
if network not in ('campus','local','tailnet'):
    raise SystemExit('Declare the actual client network')
if network=='campus':
    try: ip=ipaddress.IPv4Address(p.hostname)
    except ValueError: raise SystemExit('Campus evidence uses the direct university IPv4')
    if ip.is_loopback or ip in ipaddress.IPv4Network('100.64.0.0/10'):
        raise SystemExit('Use the university LAN IPv4, not loopback or the tailnet address')
PY
CURL_OPTIONS=(--noproxy '*')
if [[ -n "${GATEWAY_CURL_CONFIG:-}" ]]; then
    python3 - "$GATEWAY_CURL_CONFIG" "$STAGING_URL" <<'PY'
import os,stat,sys
from pathlib import Path
from urllib.parse import urlsplit
path=Path(sys.argv[1]);info=path.lstat()
if (not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid() or info.st_mode & 0o077
        or urlsplit(sys.argv[2]).scheme!='https'):
    raise SystemExit('Private curl credentials require an owned mode-600 regular file and HTTPS')
PY
    CURL_OPTIONS=(--config "$GATEWAY_CURL_CONFIG" --noproxy '*')
fi
mkdir -p private/campus-evidence
evidence=$(mktemp -d private/campus-evidence/qr02-XXXXXXXX)
printf '%s\n' "$STAGING_URL" > "$evidence/private-url.txt"
curl "${CURL_OPTIONS[@]}" -sS --max-time 5 -o "$evidence/initial-health.json" \
    -w 'initial %{http_code} %{time_total}\n' "$STAGING_URL/health" \
    > "$evidence/initial.metrics" 2> "$evidence/private-errors.log" || true
curl "${CURL_OPTIONS[@]}" -sS -o "$evidence/hung.json" -w 'hung %{http_code} %{time_total}\n' --max-time 10 \
    -H 'Content-Type: application/json' \
    -d '{"messages":[{"role":"user","content":"sleep"}]}' \
    "$STAGING_URL/v1/chat/completions" \
    > "$evidence/hung.metrics" 2>> "$evidence/private-errors.log" || true
curl "${CURL_OPTIONS[@]}" -sS -o "$evidence/health.json" -w 'health %{http_code} %{time_total}\n' --max-time 5 \
    "$STAGING_URL/health" > "$evidence/health.metrics" 2>> "$evidence/private-errors.log" || true
for i in 1 2 3 4 5 6 7 8 9 10; do
    curl "${CURL_OPTIONS[@]}" -sS -o "$evidence/next-$i.json" -w "next-$i %{http_code} %{time_total}\n" --max-time 5 \
        -H 'Content-Type: application/json' \
        -d '{"messages":[{"role":"user","content":"hello"}]}' \
        "$STAGING_URL/v1/chat/completions" \
        > "$evidence/next-$i.metrics" 2>> "$evidence/private-errors.log" || true
done
python3 - "$evidence" "$RELEASE_COMMIT" "$RUNNER" "$NETWORK" <<'PY'
from datetime import datetime,timezone
from pathlib import Path
import json,sys
directory=Path(sys.argv[1]);sha,runner,network=sys.argv[2:]
def body(name):
    try:return json.loads((directory/name).read_text())
    except (OSError,ValueError):return {}
def metric(name):
    try:
        fields=(directory/(name+'.metrics')).read_text().split()
        return {'status':int(fields[-2]),'seconds':float(fields[-1])}
    except (OSError,ValueError,IndexError):return {'status':0,'seconds':None}
initial,hung,health=[metric(n) for n in ['initial','hung','health']]
detail=body('hung.json').get('detail','')
normal=[]
for i in range(1,11):
    result=metric('next-'+str(i))
    try:content=body('next-'+str(i)+'.json')['choices'][0]['message']['content']
    except (KeyError,IndexError,TypeError):content=None
    normal.append({**result,'expected_content':content=='fake: HELLO'})
checks={
    'initial_health':initial['status']==200 and body('initial-health.json')=={'status':'ok'},
    'hung_status_504':hung['status']==504,
    'hung_within_one_second':hung['seconds'] is not None and hung['seconds']<=1.0,
    'named_plugin_and_stage':isinstance(detail,str) and 'SlowPlugin' in detail and 'request' in detail,
    'health_status_200':health['status']==200,
    'health_within_one_second':health['seconds'] is not None and health['seconds']<=1.0,
    'ten_normal_chats':all(r['status']==200 and r['expected_content'] for r in normal),
}
summary={'test':'QR-02 QRT-01','timestamp_utc':datetime.now(timezone.utc).isoformat(),
         'expected_source_sha_supplied_by_operator':sha,'runner_github_username':runner,
         'client_network_self_reported':network,
         'scope':'Timeout, health and ten normal chats; resource growth is not measured by this QRT.',
         'provenance':'Source SHA and client network require operator confirmation; no campus location is inferred automatically.',
         'checks':checks,'hung':hung,'health':health,'normal_chats':normal,
         'passed':all(checks.values()),'normal_staging_restore':'Pending deployment owner action'}
(directory/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('Evidence directory: '+str(directory))
print('Share summary.json only; URL and transport errors stay private. Tell Ali to restore normal staging.')
raise SystemExit(0 if summary['passed'] else 1)
PY
