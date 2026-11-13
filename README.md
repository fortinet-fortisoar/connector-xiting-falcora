# Xiting Falcora Connector for FortiSOAR

FortiSOAR&trade; connector for Xiting Falcora, a security operations platform for SAP landscapes. Falcora triages SAP security alerts with AI against customer SOPs, groups them into cases and collects system owner feedback.

The connector ingests Falcora alerts into FortiSOAR, keeps ingested alerts in sync with Falcora and provides playbook actions for alerts and cases.

**Version:** 1.0.0 &middot; **Compatible Falcora API:** Falcora Integration API 0.9

## Features

- **Data ingestion** of Falcora alerts into FortiSOAR alerts, with severity derived from the alert priority or the Falcora triage verdict.
- **Alert sync** that mirrors triage, owner feedback, case and processing status changes into ingested alerts on a schedule.
- **Actions:** Get Alerts, Get Alert Details, Get Alert Updates, Get Cases, Get Case Details, Get Case Alerts, Add Case Comment, Assign Case Processor, Trigger Case Analysis.
- **Sample playbooks** for every action, bundled as `Sample - Xiting Falcora - 1.0.0`.

## Requirements

- A Falcora connection credential (username and password), created under **Administration > Tenants > (tenant) > Technical Users**.
- The Falcora tenant ID the credential belongs to.

## Installation

Install the connector from the FortiSOAR **Content Hub**, or as root:

```
yum install cyops-connector-xiting-falcora
```

## Documentation

See the [connector documentation](xiting-falcora/docs/xiting-falcora-doc.md) for configuration parameters, action inputs and outputs, error handling and data ingestion setup.

## Repository layout

| Path | Content |
|---|---|
| `xiting-falcora/` | Connector source, `info.json`, playbooks and images |
| `xiting-falcora/docs/` | Connector documentation |
| `.github/workflows/` | Sanity checks and tests |

## License

[MIT](LICENSE)
