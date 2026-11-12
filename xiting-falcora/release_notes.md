#### What's New
- Authentication now uses HTTP Basic with a Falcora connection credential (Administration > Tenants > (tenant) > Technical Users). Microsoft Entra ID authentication (Username and Password and Client Credentials flows) has been removed.
- Tenant ID is now required in the configuration, because a connection credential is valid for exactly one tenant.
- The health check verifies the credential with a narrow alert query on the configured tenant instead of `/info/me`.
- Clearer error messages when a credential is rejected or not permitted to call an endpoint.
- New action Get Alert Updates and the playbooks `Xiting Falcora > Sync Alerts` and `> Xiting Falcora > Update Record`, which mirror changes in Falcora (triage, owner feedback, case, processing status) into the ingested FortiSOAR alerts on a schedule.
- Connector documentation with input parameters, output schemas, sample responses, value reference, error handling and data ingestion setup.
- Data ingestion: the ingestion parameters set in the Data Ingestion Wizard are now applied, alert severity is derived from `AlertData.PRIO` or the Falcora triage verdict and false-positive score, and the severity picklist lookup has been fixed.
- Output schemas include `UserAgent`, `CaseLinkageReason`, `ProcessingMode` and the structure of `AlertData`.

#### Removed
The following actions are not available to a connection credential and have been removed, together with their sample playbooks:
- Alerts: Assign Alert to Case, Retry Triage, Bulk Retry Triage, Re-evaluate Triage.
- Cases: Get Case Graph, Update Case Comment, Get Eligible Processors, Finalize Case Evaluation, and the Integration User option of Assign Case Processor.
- Enrichment: Get Systems, Get System Details, Get System Custom Attribute Definitions, Get SLAs, Get SLA Details, Get Users, Get User Details, Get Current User.
- MITRE ATT&CK: Get MITRE Technique, Get MITRE Matrices, Get MITRE Matrix.
