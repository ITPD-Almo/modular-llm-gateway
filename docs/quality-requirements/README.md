# Quality requirements

The quality bars the gateway is checked against, sorted by business importance and then technical risk.

| QR | Outcome | Business importance | Technical risk | Characteristic | Sub-characteristic | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [QR-02](qr/QR-02.md) | A plugin hook that never returns fails only the request it is processing, and the gateway serves the next request normally. | High | High | Reliability | Fault Tolerance | Active |
| [QR-01](qr/QR-01.md) | Every behavior of the plugin pipeline can be checked by automated tests that need no network access and no provider key. | High | Medium | Maintainability | Testability | Active |
| [QR-03](qr/QR-03.md) | Nothing the gateway itself writes for diagnosis or returns as an error contains the content of a request or a response. | Medium | Medium | Security | Confidentiality | Active |
| [QR-05](qr/QR-05.md) | At the default capacity, four concurrent healthy chat requests succeed, and excess concurrent traffic receives a bounded result while health and later requests remain available. | Medium | Medium | Performance Efficiency | Capacity | Active |
| [QR-04](qr/QR-04.md) | A developer new to the project installs and starts the gateway using only the setup guide. | Medium | Low | Flexibility | Installability | Active |
