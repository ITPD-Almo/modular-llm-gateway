# Gateway check for the written demo

Checked on October 17, 2026, from a fresh clone of main at [71cb6ff3eac0da2172d6563229d2a76f7d2598b2](https://github.com/ITPD-Almo/modular-llm-gateway/commit/71cb6ff3eac0da2172d6563229d2a76f7d2598b2). These are local technical results. The Customer has not accepted or rejected the stories yet.

## Setup

Followed the POSIX setup in [the setup guide](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/docs/setup.md): cloned with submodules, created a Python 3.12 environment, upgraded pip, installed `.[test]`, and copied `.env.example` to `.env`. Windows PowerShell was not tested.

Started the server with:

```console
python -m uvicorn gateway.main:create_app --factory --env-file .env --reload
```

The health endpoint returned `{"status":"ok"}`. Sent the setup guide's request with curl:

```sh
curl -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"fake","messages":[{"role":"user","content":"hello"}]}'
```

No real provider key was used. Each configuration was checked after stopping and restarting the server. The original configuration was restored afterwards.

## Story checks

| Story and criterion | Observed result |
| --- | --- |
| [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), AC-01 | A clean clone starts with MetadataPlugin and UppercasePlugin from `config/plugins.json`. |
| US-01, AC-02 | With metadata first and uppercase second, both the response trace and the request/response audit entries follow that order. |
| US-01, AC-03 | Reversing the list and restarting changes the trace to uppercase then metadata. The text stays `fake: HELLO`. Removing uppercase and restarting changes the text to `fake: hello`. |
| [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), AC-01 | [The plugin contract](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/docs/plugins.md) documents dictionaries in and out, request and response methods, configuration order, startup loading, and failure handling. |
| US-02, AC-02 | [MetadataPlugin](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/gateway/plugins/add_metadata.py) and [UppercasePlugin](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/gateway/plugins/uppercase.py) implement `process_request` and `process_response`. Both are loaded from their configured import paths and run through those methods. |
| [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), AC-01 | The documented curl request returns HTTP 200 from the fake provider with `fake: HELLO`. |
| US-03, AC-02 | `plugin_changes` lists metadata/request, uppercase/request, metadata/response, and uppercase/response. Each entry names the plugin, stage, and change. |
| US-03, AC-03 | Two identical requests returned identical JSON in each of the three configurations, without a real provider key. |

## Default response

```json
{
  "id": "fake-response",
  "model": "fake",
  "provider": "fake",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "fake: HELLO"
      }
    }
  ],
  "plugin_trace": [
    "metadata",
    "uppercase"
  ],
  "plugin_changes": [
    {
      "plugin": "metadata",
      "stage": "request",
      "change": "added metadata.gateway=modular"
    },
    {
      "plugin": "uppercase",
      "stage": "request",
      "change": "uppercased message content"
    },
    {
      "plugin": "metadata",
      "stage": "response",
      "change": "recorded metadata transformation"
    },
    {
      "plugin": "uppercase",
      "stage": "response",
      "change": "recorded uppercase transformation"
    }
  ]
}
```

The metadata request change is reported in the audit list. The response does not include the full request metadata object. On the response side, the example plugins add trace and audit entries; they do not change the provider's message text.

## Tests and CI

`python -m pytest --basetemp /tmp/itpd-week03-main-pytest -p no:cacheprovider` passed all five tests with pytest 9.1.1 and Python 3.12.3. One upstream TestClient/httpx deprecation warning was reported.

On the same main revision, the [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228883), [link check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228923), [Markdown check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228873), and [documentation build and deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228886) passed.

## Week 2 action points

These outcomes were checked after the October 16 meeting, rather than presented during it. The original actions are in [the Week 2 report](../week-02/meeting-report.md#action-points).

| Action | Outcome on October 17 |
| --- | --- |
| Draft the proposed system flow and plugin interface, including inputs, outputs, ordering, and loading. | Implemented in [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48), with the contract in [plugins.md](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/docs/plugins.md), the loader in [config.py](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/gateway/config.py), and the pipeline in [main.py](https://github.com/ITPD-Almo/modular-llm-gateway/blob/71cb6ff3eac0da2172d6563229d2a76f7d2598b2/gateway/main.py). The local run checks that documented sequence. |
| Prepare a small working interaction with two simple plugins and a fake provider. | Implemented in PR #48. The clean-start and curl checks above run both plugins and the fake provider. Customer demonstration and verdicts are still pending. |

## Week 2 open questions

| Question | Current position |
| --- | --- |
| Does the revised story set cover the usable workflow? | All three stories are implemented; the Customer still needs to judge the set. |
| What does a plugin receive and return, and how do failures work? | Dictionaries pass through request and response methods; loading errors stop startup, plugin errors return a named HTTP 500, and provider errors return HTTP 502. The Customer still needs to assess the contract, including timeout and debugging needs. |
| Is policy-version tracking needed, and what content may be kept? | Still open; the example audit does not settle production retention. |
| Can an existing gateway support the same workflow? | Still open; the matched comparison has not been supplied. |
| Are static credentials and one provider enough? | A deterministic fake provider runs without a real key. Authentication and trial limits still need agreement. |
| Which synthetic data should a masking plugin handle? | Still open. These examples add metadata and uppercase text; they are not masking plugins. |
| May we publish a sanitized transcript or share it privately? | Still unconfirmed. No source transcript or recording is published here. |

## Next step

Ali will forward the checked demo and ask the Customer for a separate accept or reject verdict for US-01, US-02 and US-03, plus clarification about two or three example plugins. No story is closed and no verdict decision is added on the basis of these local checks alone.
