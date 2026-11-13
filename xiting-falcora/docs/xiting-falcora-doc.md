## About the connector
Xiting Falcora is a security operations platform for SAP landscapes. It triages SAP security alerts with AI against customer SOPs, groups them into cases, collects system owner feedback and supports the analyst up to the final verdict.
<p>This document provides information about the Xiting Falcora Connector, which facilitates automated interactions with a Xiting Falcora server using FortiSOAR&trade; playbooks. Add the Xiting Falcora Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Xiting Falcora, such as ingesting Falcora alerts, reading alerts and cases, adding enrichment comments to cases and re-running the AI case analysis.</p>
### Version information

Connector Version: 1.0.0

Authored By: Fortinet CSE

Contributors: Julian Petersohn

Certified: No

Compatible Falcora API: Falcora Integration API 0.9

## Installing the connector
<p>Use the <strong>Content Hub</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.</p><p>You can also use the <code>yum</code> command as a root user to install the connector:</p>
<pre>yum install cyops-connector-xiting-falcora</pre>

## Prerequisites to configuring the connector
- A Falcora connection credential (username and password) for the tenant you want to connect. The Falcora administrator creates it under <strong>Administration &gt; Tenants &gt; (tenant) &gt; Technical Users</strong>. The password is shown only once, at creation; if it is lost, rotate it in Falcora.
- The Falcora tenant ID the credential was created for. Falcora shows it next to the credential.
- The FortiSOAR&trade; server must have outbound connectivity to port 443 on the Falcora API host, for example <code>api.falcora.xiting.com</code>.

## Minimum Permissions Required
The connection credential is valid for exactly one tenant. It needs the following Falcora roles on that tenant:

<table border=1><thead><tr><th>Role</th><th>Used by</th></tr></thead><tbody>
<tr><td><code>Tenant.Alerts.Read</code></td><td>Health check, Get Alerts, Get Alert Details, Get Case Alerts, data ingestion</td></tr>
<tr><td><code>Tenant.Cases.Read</code></td><td>Get Cases, Get Case Details</td></tr>
<tr><td><code>Tenant.Cases.Write</code></td><td>Add Case Comment, Assign Case Processor, Trigger Case Analysis</td></tr>
</tbody></table>

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>Xiting Falcora</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations</strong> tab enter the required configuration details:</p>
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Environment</td><td>Falcora environment to connect to. Test and Production set the API URL automatically. Select Custom to enter it yourself.<br/>Options: <code>Test</code>, <code>Production</code>, <code>Custom</code><br/>Default: <code>Test</code><br/><em>Required</em></td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;API URL</td><td>If you choose <code>Custom</code>: Falcora API base URL including the /backend/api path prefix.<br/>Default: <code>https://api.falcora-test.xiting.com/backend/api</code><br/><em>Required</em></td></tr>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant the connection credential was created for. A credential is valid for exactly one tenant. Shown in Falcora next to the credential.<br/><em>Required</em></td></tr>
<tr><td>Username</td><td>Username of the Falcora connection credential (HTTP Basic authentication). Created by the Falcora administrator under Administration &gt; Tenants &gt; (tenant) &gt; Technical Users.<br/><em>Required</em></td></tr>
<tr><td>Password</td><td>Password of the Falcora connection credential. It is shown only once, at creation; if it is lost, rotate it in Falcora.<br/><em>Required</em></td></tr>
<tr><td>Verify SSL</td><td>Specifies whether the SSL certificate for the server is to be verified. By default, this option is set to True.<br/>Default: <code>True</code><br/><em>Optional</em></td></tr>
</tbody></table>

**Note:** The connector authenticates with HTTP Basic (<code>Authorization: Basic base64(username:password)</code>) on every request. The health check runs <code>GET /tenant/alerts?TenantId=&lt;Tenant ID&gt;&amp;TimestampRelative=LastHour</code>, so it verifies the credential, the tenant and the <code>Tenant.Alerts.Read</code> role at once.

## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations:
<table border=1><thead><tr><th>Function</th><th>Description</th><th>Annotation and Category</th></tr></thead><tbody>
<tr><td><a href="#operation-get-alerts">Get Alerts</a></td><td>Retrieves a list of alerts from Falcora, newest first, based on the time range and filters you have specified. The time range applies to the time Falcora received the alert. Falcora does not page this list, so keep time ranges short.</td><td>get_alerts <br/>Investigation</td></tr>
<tr><td><a href="#operation-get-alert-details">Get Alert Details</a></td><td>Retrieves the full details of a specific alert, including the raw event, triage justification, SOP, owner feedback and action log, based on the alert ID you have specified.</td><td>get_alert <br/>Investigation</td></tr>
<tr><td><a href="#operation-get-alert-updates">Get Alert Updates</a></td><td>Re-reads alerts that were already fetched from Falcora and reports which ones changed since, for example a new triage verdict, owner feedback, a different case or a new processing status. Use it to keep FortiSOAR alerts in sync with Falcora. Makes one request per alert.</td><td>get_alerts <br/>Investigation</td></tr>
<tr><td><a href="#operation-get-cases">Get Cases</a></td><td>Retrieves a list of cases from Falcora based on the time range and filters you have specified. The time range applies to the case creation time.</td><td>get_cases <br/>Investigation</td></tr>
<tr><td><a href="#operation-get-case-details">Get Case Details</a></td><td>Retrieves the full details of a specific case, including the summary, AI analysis, analyst decision, progress, latest AI investigation, history and comments, based on the case ID you have specified.</td><td>get_case <br/>Investigation</td></tr>
<tr><td><a href="#operation-get-case-alerts">Get Case Alerts</a></td><td>Retrieves the alerts linked to a specific case.</td><td>get_alerts <br/>Investigation</td></tr>
<tr><td><a href="#operation-add-case-comment">Add Case Comment</a></td><td>Adds enrichment to a case as a plain-text comment. Comments longer than 1000 characters are split into several comments. The sequence "${" is escaped automatically. Comments cannot be deleted and completed cases do not accept comments.</td><td>add_comment <br/>Investigation</td></tr>
<tr><td><a href="#operation-assign-case-processor">Assign Case Processor</a></td><td>Sets or clears the processor of a case.</td><td>assign_case <br/>Investigation</td></tr>
<tr><td><a href="#operation-trigger-case-analysis">Trigger Case Analysis</a></td><td>Re-runs the AI case analysis, for example after adding significant enrichment. Also reopens completed cases for analysis.</td><td>analyze <br/>Investigation</td></tr>
</tbody></table>

### operation: Get Alerts
Retrieves a list of alerts from Falcora, newest first, based on the time range and filters you have specified. The time range applies to the time Falcora received the alert. Falcora does not page this list, so keep time ranges short.

Falcora API: <code>GET /tenant/alerts</code>

Results are ordered by <code>ReceivedAt</code>, newest first. Falcora does not page this list, so keep time ranges short. The list does not include the raw event (<code>AlertData</code>); enable <strong>Include Alert Details</strong> to read each alert individually (one extra request per alert).

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Relative Time Range</td><td>Relative time range on the received time. Cannot be combined with Start Time or End Time.<br/>Options: <code>Last Hour</code>, <code>Last 24 Hours</code>, <code>Last 3 Days</code>, <code>Last 7 Days</code><br/><em>Optional</em></td></tr>
<tr><td>Start Time</td><td>Return records whose received time is at or after this time (inclusive).<br/><em>Optional</em></td></tr>
<tr><td>End Time</td><td>Return records whose received time is before this time (exclusive).<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>Return only alerts linked to this case.<br/><em>Optional</em></td></tr>
<tr><td>System ID</td><td>Return only alerts for this SAP system ID (exact match).<br/><em>Optional</em></td></tr>
<tr><td>Processing Status</td><td>Return only alerts in this processing status.<br/>Options: <code>Open</code>, <code>Triage In Progress</code>, <code>Waiting For Owner Input</code>, <code>Blocked Quota Exceeded</code>, <code>Completed</code>, <code>Error</code><br/><em>Optional</em></td></tr>
<tr><td>Triage</td><td>Return only alerts with this AI triage verdict.<br/>Options: <code>False Positive</code>, <code>True Positive</code><br/><em>Optional</em></td></tr>
<tr><td>System Owner ID</td><td>Return only alerts routed to this system owner (Falcora user object ID).<br/><em>Optional</em></td></tr>
<tr><td>Alert Type</td><td>Return only alerts of this source type.<br/>Options: <code>Xiting SIEM Connector</code>, <code>SAP ETD</code>, <code>Splunk</code>, <code>Unknown</code><br/><em>Optional</em></td></tr>
<tr><td>Include Details</td><td>Select to read every returned alert individually, adding the raw event (AlertData), the triage justification, SOP and owner feedback. This makes one extra request per alert.<br/>Default: <code>False</code><br/><em>Optional</em></td></tr>
<tr><td>Limit</td><td>Maximum number of alerts to return (applied after retrieval; newest first).<br/><em>Optional</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
[
    {
        "TenantId": "",
        "AlertId": "",
        "AlertType": "",
        "ReceivedAt": "",
        "ProcessingStatus": "",
        "ProcessingStatusString": "",
        "LLMTriage": "",
        "LLMTriageString": "",
        "LLMFalsePositiveScore": "",
        "LLMTriageEvaluatedAt": "",
        "PatternName": "",
        "SystemId": "",
        "SystemOwnerIds": [],
        "SystemOwnerClassification": "",
        "SystemOwnerFeedbackReceivedAt": "",
        "CaseId": "",
        "CaseLinkageReason": "",
        "UserIds": [],
        "SourceIPAddress": "",
        "UserAgent": "",
        "TriageFlags": [],
        "AlertSemanticDescription": "",
        "SOP": {
            "TenantId": "",
            "SOPId": "",
            "Version": ""
        },
        "CreatedBy": "",
        "ChangedBy": ""
    }
]
```

**Alert fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>TenantId</code></td><td>string</td><td>Falcora tenant the alert belongs to.</td></tr>
<tr><td><code>AlertId</code></td><td>string (UUID)</td><td>Unique ID Falcora assigned to the alert. Used as the FortiSOAR alert Source ID.</td></tr>
<tr><td><code>AlertType</code></td><td>string</td><td>Source format: <code>Xiting SIEM Connector</code>, <code>SAP ETD</code>, <code>Splunk</code> or <code>Unknown</code>.</td></tr>
<tr><td><code>ReceivedAt</code></td><td>ISO 8601</td><td>Time Falcora received the alert. The time-range filters apply to this field.</td></tr>
<tr><td><code>ProcessingStatus / ProcessingStatusString</code></td><td>int / string</td><td>Triage state, see <a href="#alert-processingstatus">Alert ProcessingStatus</a>.</td></tr>
<tr><td><code>LLMTriage / LLMTriageString</code></td><td>int / string</td><td>AI triage verdict: <code>1</code> false_positive, <code>2</code> true_positive. Absent while triage is pending.</td></tr>
<tr><td><code>LLMFalsePositiveScore</code></td><td>int 0-100</td><td>AI confidence that the alert is a false positive. Low values mean the alert is likely real.</td></tr>
<tr><td><code>LLMTriageEvaluatedAt</code></td><td>ISO 8601</td><td>Time the AI triage finished.</td></tr>
<tr><td><code>PatternName</code></td><td>string</td><td>Name of the detection pattern. Used as the FortiSOAR alert name.</td></tr>
<tr><td><code>SystemId</code></td><td>string</td><td>SAP system ID (SID) the alert concerns.</td></tr>
<tr><td><code>SystemOwnerIds</code></td><td>string[]</td><td>Falcora user object IDs of the system owners asked for feedback.</td></tr>
<tr><td><code>SystemOwnerClassification, SystemOwnerFeedbackReceivedAt</code></td><td>string, ISO 8601</td><td>The owner's classification and when it arrived. Present once an owner answered.</td></tr>
<tr><td><code>CaseId</code></td><td>string (UUID)</td><td>Case the alert is grouped into.</td></tr>
<tr><td><code>CaseLinkageReason</code></td><td>string</td><td>Why the alert was put into its case, for example <code>NEW_CASE</code>.</td></tr>
<tr><td><code>UserIds</code></td><td>string[]</td><td>SAP users involved in the event.</td></tr>
<tr><td><code>SourceIPAddress</code></td><td>string</td><td>Address that <em>sent</em> the alert to Falcora (for example the SIEM), not an address from the event.</td></tr>
<tr><td><code>UserAgent</code></td><td>string</td><td>User agent of the client that sent the alert.</td></tr>
<tr><td><code>TriageFlags</code></td><td>string[]</td><td>Triage hints, for example <code>NO_SOP</code> when no SOP matched.</td></tr>
<tr><td><code>AlertSemanticDescription</code></td><td>string</td><td>AI-written description of the event.</td></tr>
<tr><td><code>SOP</code></td><td>object</td><td>Standard operating procedure applied: <code>TenantId</code>, <code>SOPId</code>, <code>Version</code>.</td></tr>
<tr><td><code>CreatedBy, ChangedBy</code></td><td>string</td><td>A user object ID, <code>basic:&lt;credential&gt;</code> or <code>system:&lt;component&gt;</code>.</td></tr>
</tbody></table>

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
[
    {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "AlertId": "e2a7d9c1-6b4f-4e3a-9c85-1f0b7d2e4a96",
        "AlertType": "Xiting SIEM Connector",
        "ReceivedAt": "2026-11-11T16:51:25.442Z",
        "ProcessingStatus": 70,
        "LLMTriage": 2,
        "LLMFalsePositiveScore": 10,
        "LLMTriageEvaluatedAt": "2026-11-11T16:51:42.811Z",
        "PatternName": "Download of multiple files",
        "SystemId": "PRD",
        "CaseId": "91c2a6e4-3d7b-4f18-b0a5-6e2c8d4f1a73",
        "CaseLinkageReason": "NEW_CASE",
        "UserIds": [
            "JSMITH"
        ],
        "SourceIPAddress": "198.51.100.23",
        "UserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
        "TriageFlags": [
            "NO_SOP"
        ],
        "CreatedBy": "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64",
        "ChangedBy": "system:alert-triage-queue",
        "AlertSemanticDescription": "A user downloaded twelve files from the Production SAP ABAP system, generating a multiple-file download alert. The activity may indicate unauthorized data access or data exfiltration and warrants review of the downloaded content and business justification.",
        "LLMTriageString": "true_positive",
        "ProcessingStatusString": "completed"
    },
    {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "AlertId": "b8f0c6d2-1c3e-4f0a-8d7e-5a9b2c4e6f10",
        "AlertType": "Xiting SIEM Connector",
        "ReceivedAt": "2026-08-25T16:34:14.443Z",
        "ProcessingStatus": 50,
        "LLMTriage": 2,
        "LLMFalsePositiveScore": 4,
        "LLMTriageEvaluatedAt": "2026-08-25T16:34:32.831Z",
        "PatternName": "Assignment of authorizations to own user",
        "SystemId": "PRD",
        "SystemOwnerIds": [
            "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64"
        ],
        "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
        "UserIds": [
            "JSMITH"
        ],
        "SourceIPAddress": "198.51.100.23",
        "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "TriageFlags": [],
        "CreatedBy": "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64",
        "ChangedBy": "system:alert-triage-queue",
        "AlertSemanticDescription": "A production SAP ABAP system logged a user master change event indicating assignment of authorizations to the acting account’s own user in client 000. This is a self-authorization privilege escalation on a sensitive system and is suspicious because it can grant unauthorized access beyond approved business roles.",
        "SOP": {
            "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
            "SOPId": "AssignmentOfAuthorizationsToOwnUser",
            "Version": "1"
        },
        "LLMTriageString": "true_positive",
        "ProcessingStatusString": "waiting_for_owner_input"
    }
]
```

### operation: Get Alert Details
Retrieves the full details of a specific alert, including the raw event, triage justification, SOP, owner feedback and action log, based on the alert ID you have specified.

Falcora API: <code>GET /tenant/alerts/{TenantId}/{AlertId}</code>

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Alert ID</td><td>ID (UUID) of the Falcora alert.<br/><em>Required</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "TenantId": "",
    "AlertId": "",
    "AlertType": "",
    "ReceivedAt": "",
    "ProcessingStatus": "",
    "ProcessingStatusString": "",
    "LLMTriage": "",
    "LLMTriageString": "",
    "LLMFalsePositiveScore": "",
    "LLMTriageEvaluatedAt": "",
    "PatternName": "",
    "SystemId": "",
    "SystemOwnerIds": [],
    "SystemOwnerClassification": "",
    "SystemOwnerFeedbackReceivedAt": "",
    "CaseId": "",
    "CaseLinkageReason": "",
    "UserIds": [],
    "SourceIPAddress": "",
    "UserAgent": "",
    "TriageFlags": [],
    "AlertSemanticDescription": "",
    "SOP": {
        "TenantId": "",
        "SOPId": "",
        "Version": ""
    },
    "CreatedBy": "",
    "ChangedBy": "",
    "AlertData": {
        "ID": "",
        "NAME": "",
        "MESSAGE": "",
        "PRIO": "",
        "SYSID": "",
        "userid": "",
        "TIME_STAMP": "",
        "T_FIELDS": [
            {
                "MAP_ID": "",
                "VAL": ""
            }
        ],
        "T_CEF": [
            {
                "ID": "",
                "VAL": "",
                "LABEL": ""
            }
        ],
        "T_MATCHES": []
    },
    "LLMTriageJustification": "",
    "SOPActions": "",
    "SOPQuestionsForOwner": [],
    "SystemOwnerAnswers": [],
    "SystemOwnerFeedback": "",
    "AIAnsweredQuestions": [],
    "AutoResolvedByAI": "",
    "AIAnswerOverridden": "",
    "SapArtifacts": {
        "Version": "",
        "TransactionCodes": []
    },
    "ActionLog": [
        {
            "Timestamp": "",
            "Actor": "",
            "Type": "",
            "Details": ""
        }
    ],
    "ErrorMessage": "",
    "RetryCount": "",
    "LastRetryAt": ""
}
```

**All fields of Get Alerts, plus:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>AlertData</code></td><td>object</td><td>The raw event as received (Xiting SIEM Connector format): <code>ID</code>, <code>NAME</code>, <code>MESSAGE</code>, <code>PRIO</code>, <code>SYSID</code>, <code>TIME_STAMP</code> (YYYYMMDDhhmmss), <code>T_FIELDS</code>, <code>T_CEF</code>, <code>T_MATCHES</code>. <code>PRIO</code> is the priority as the source expresses it (free text or a number).</td></tr>
<tr><td><code>LLMTriageJustification</code></td><td>string</td><td>The AI's reasoning for the triage verdict.</td></tr>
<tr><td><code>SOPActions, SOPQuestionsForOwner</code></td><td>array</td><td>What the matched SOP prescribes, and the questions it asks the system owner (with step context and SAP tools to use).</td></tr>
<tr><td><code>SystemOwnerAnswers, SystemOwnerFeedback</code></td><td>array, string</td><td>The owner's answers and free-text feedback.</td></tr>
<tr><td><code>AIAnsweredQuestions, AutoResolvedByAI, AIAnswerOverridden</code></td><td>array, bool, bool</td><td>Owner questions the AI answered from context, and whether a human overrode them.</td></tr>
<tr><td><code>SapArtifacts</code></td><td>object</td><td>SAP objects recognised in the event, for example <code>{"Version":1,"TransactionCodes":["SE16N"]}</code>.</td></tr>
<tr><td><code>ActionLog</code></td><td>array</td><td>History: <code>[{"Timestamp","Actor","Type","Details"}]</code>.</td></tr>
<tr><td><code>ErrorMessage, RetryCount, LastRetryAt</code></td><td>string, int, ISO 8601</td><td>Present after a failed or retried triage.</td></tr>
</tbody></table>

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
{
    "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
    "AlertId": "b8f0c6d2-1c3e-4f0a-8d7e-5a9b2c4e6f10",
    "ProcessingStatus": 50,
    "AlertData": {
        "ID": "/PE_AUTOWNUSR",
        "NAME": "Assignment of authorizations to own user",
        "MESSAGE": "PRD - Assignment of authorizations to own user: JSMITH in client 000",
        "PRIO": "7",
        "SYSID": "PRD",
        "userid": "JSMITH",
        "TIME_STAMP": 20260825163404,
        "T_FIELDS": [
            {
                "MAP_ID": 1,
                "VAL": "JSMITH"
            },
            {
                "MAP_ID": 2,
                "VAL": "000"
            }
        ],
        "T_CEF": [
            {
                "ID": "sourceServiceName",
                "VAL": "PRD",
                "LABEL": ""
            }
        ],
        "T_MATCHES": [
            {
                "MANDT": "000",
                "SYSID": "PRD",
                "ID": "/PE_AUTOWNUSR",
                "GRP": "000",
                "POS": 20,
                "TIMESTAMP": 20260825163404,
                "CNT": 6,
                "STRUCT": "/SA_S_SAL_PROTOCOL",
                "MESSAGE": {
                    "SID": "PRD",
                    "MSCGLLID": "AUB",
                    "MSCDATE": "2026-08-25",
                    "MSCTIME": "16:34:04",
                    "SEVERORIG": 7,
                    "MANDT": "000",
                    "USERID": "JSMITH",
                    "MSG": "PRD - Assignment of authorizations to own user: JSMITH in client 000",
                    "AREA": "AU",
                    "SUBID": "B",
                    "INSTANCE": "sapprd01_PRD_00",
                    "SLGLTRM2": "-GMMJL9",
                    "TERM_IPV6": "203.0.113.45",
                    "SLGTC": "SE16N",
                    "SLGREPNA": "SAPMSSY4",
                    "SUBCLASID": 32,
                    "TXSUBCLASID": "User Master Changes",
                    "PARAM1": "JSMITH",
                    "PARAM2": "",
                    "PARAM3": "",
                    "PARAMX": "",
                    "XUTC": "2026-08-25T16:34:04Z"
                }
            }
        ]
    },
    "AlertType": "Xiting SIEM Connector",
    "SystemId": "PRD",
    "PatternName": "Assignment of authorizations to own user",
    "SourceIPAddress": "198.51.100.23",
    "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "ReceivedAt": "2026-08-25T16:34:14.443Z",
    "CreatedBy": "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64",
    "ChangedBy": "system:alert-triage-queue",
    "UserIds": [
        "JSMITH"
    ],
    "SOP": {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "SOPId": "AssignmentOfAuthorizationsToOwnUser",
        "Version": "1"
    },
    "AlertSemanticDescription": "A production SAP ABAP system logged a user master change event indicating assignment of authorizations to the acting account’s own user in client 000. This is a self-authorization privilege escalation on a sensitive system and is suspicious because it can grant unauthorized access beyond approved business roles.",
    "LLMFalsePositiveScore": 4,
    "LLMTriageJustification": "Self-authorization is an uncontrolled privilege escalation, and on a Production SAP system it poses direct risk to live business data and operations. No break-glass or other approved exception is indicated, and the alert content does not provide a benign operational explanation.",
    "LLMTriageEvaluatedAt": "2026-08-25T16:34:32.831Z",
    "LLMTriage": 2,
    "LLMTriageString": "true_positive",
    "SOPQuestionsForOwner": [
        {
            "QuestionId": "AUTH_ABAP_1_1",
            "Prompt": "Which roles or profiles did the user assign to their own account (name all that you can identify in the change documents)?",
            "ExpectedAnswerType": "string",
            "Required": true,
            "StepContext": {
                "Step": 1,
                "Action": "Identify which privileges the user assigned to themselves",
                "Details": "Use SUIM change documents for the affected user to find role and profile assignments where the same user appears both as the account owner and as the acting user. Focus on the time window around the alert.",
                "Tools": [
                    {
                        "Type": "Transaction",
                        "Name": "SUIM",
                        "Path": "User Information System → Change Documents → User → For Users"
                    }
                ]
            }
        }
    ],
    "TriageFlags": [],
    "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
    "SystemOwnerIds": [
        "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64"
    ],
    "ActionLog": [
        {
            "Timestamp": "2026-08-25T16:34:38.169Z",
            "Actor": "system:alert-triage-queue",
            "Type": "TRIAGED",
            "Details": {
                "TriageResult": "TRUE_POSITIVE",
                "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12"
            }
        }
    ],
    "SapArtifacts": {
        "Version": 1,
        "TransactionCodes": [
            "SE16N"
        ]
    },
    "ProcessingStatusString": "waiting_for_owner_input"
}
```

**Action-specific errors:**

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>404</td><td>The alert does not exist in the tenant: <code>{"Status":"NotFound","Message":"Alert not found"}</code>.</td></tr>
</tbody></table>

### operation: Get Alert Updates
Re-reads alerts that were already fetched from Falcora and reports which ones changed since, for example a new triage verdict, owner feedback, a different case or a new processing status. Use it to keep FortiSOAR alerts in sync with Falcora. Makes one request per alert.

Falcora API: <code>GET /tenant/alerts/{TenantId}/{AlertId} (once per alert)</code>

Pass the FortiSOAR alert records as they are, for example <code>{{vars.steps.Find_Alerts.data['hydra:member']}}</code>: the action reads the previously fetched Falcora alert from each record's Source Data (a JSON object or JSON string) and compares it with the current one. Only the fields listed under <em>Compared fields</em> count as a change; long texts are reported as <em>added</em> or <em>updated</em> without their content. The <code>Xiting Falcora &gt; Sync Alerts</code> playbook uses this action, see <a href="#keeping-ingested-alerts-in-sync">Keeping ingested alerts in sync</a>.

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Used for alerts whose stored data has no TenantId. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Alerts</td><td>List of the alerts to check, at most 200. Each entry can be a FortiSOAR alert record (its Source Data holds the previously fetched Falcora alert), a Falcora alert object, or a Falcora alert ID.<br/><em>Required</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "UpdatedCount": "",
    "Updated": [
        {
            "RecordIRI": "",
            "AlertId": "",
            "RecordSeverity": "",
            "Changes": [],
            "PreviousAlert": {},
            "Alert": {
                "TenantId": "",
                "AlertId": "",
                "AlertType": "",
                "ReceivedAt": "",
                "ProcessingStatus": "",
                "ProcessingStatusString": "",
                "LLMTriage": "",
                "LLMTriageString": "",
                "LLMFalsePositiveScore": "",
                "LLMTriageEvaluatedAt": "",
                "PatternName": "",
                "SystemId": "",
                "SystemOwnerIds": [],
                "SystemOwnerClassification": "",
                "SystemOwnerFeedbackReceivedAt": "",
                "CaseId": "",
                "CaseLinkageReason": "",
                "UserIds": [],
                "SourceIPAddress": "",
                "UserAgent": "",
                "TriageFlags": [],
                "AlertSemanticDescription": "",
                "SOP": {
                    "TenantId": "",
                    "SOPId": "",
                    "Version": ""
                },
                "CreatedBy": "",
                "ChangedBy": "",
                "AlertData": {
                    "ID": "",
                    "NAME": "",
                    "MESSAGE": "",
                    "PRIO": "",
                    "SYSID": "",
                    "userid": "",
                    "TIME_STAMP": "",
                    "T_FIELDS": [
                        {
                            "MAP_ID": "",
                            "VAL": ""
                        }
                    ],
                    "T_CEF": [
                        {
                            "ID": "",
                            "VAL": "",
                            "LABEL": ""
                        }
                    ],
                    "T_MATCHES": []
                },
                "LLMTriageJustification": "",
                "SOPActions": "",
                "SOPQuestionsForOwner": [],
                "SystemOwnerAnswers": [],
                "SystemOwnerFeedback": "",
                "AIAnsweredQuestions": [],
                "AutoResolvedByAI": "",
                "AIAnswerOverridden": "",
                "SapArtifacts": {
                    "Version": "",
                    "TransactionCodes": []
                },
                "ActionLog": [
                    {
                        "Timestamp": "",
                        "Actor": "",
                        "Type": "",
                        "Details": ""
                    }
                ],
                "ErrorMessage": "",
                "RetryCount": "",
                "LastRetryAt": ""
            }
        }
    ],
    "Unchanged": [
        {
            "RecordIRI": "",
            "AlertId": ""
        }
    ],
    "NotFound": [
        {
            "RecordIRI": "",
            "AlertId": ""
        }
    ],
    "Errors": [
        {
            "RecordIRI": "",
            "AlertId": "",
            "Error": ""
        }
    ]
}
```

**Response fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>UpdatedCount</code></td><td>int</td><td>Number of alerts that changed.</td></tr>
<tr><td><code>Updated[]</code></td><td>array</td><td>Alerts that changed since they were fetched.</td></tr>
<tr><td><code>Updated[].RecordIRI</code></td><td>string</td><td>IRI of the FortiSOAR alert record that was passed in (<code>@id</code>), or <code>null</code> for a plain alert ID.</td></tr>
<tr><td><code>Updated[].AlertId</code></td><td>string</td><td>Falcora alert ID.</td></tr>
<tr><td><code>Updated[].RecordSeverity</code></td><td>string</td><td>Severity IRI of the FortiSOAR record that was passed in. Used by the sync playbook to keep an analyst's severity.</td></tr>
<tr><td><code>Updated[].Changes</code></td><td>string[]</td><td>Human-readable list of what changed, for example <code>Processing status: waiting_for_owner_input -&gt; completed</code>.</td></tr>
<tr><td><code>Updated[].PreviousAlert</code></td><td>object</td><td>The alert as it was passed in (the stored Source Data).</td></tr>
<tr><td><code>Updated[].Alert</code></td><td>object</td><td>The alert as Falcora returns it now, with all fields of Get Alert Details.</td></tr>
<tr><td><code>Unchanged[]</code></td><td>array</td><td><code>{"RecordIRI","AlertId"}</code> of alerts without changes.</td></tr>
<tr><td><code>NotFound[]</code></td><td>array</td><td><code>{"RecordIRI","AlertId"}</code> of alerts Falcora no longer returns (HTTP 404).</td></tr>
<tr><td><code>Errors[]</code></td><td>array</td><td><code>{"RecordIRI","AlertId","Error"}</code> of alerts that could not be checked, for example without a Falcora alert ID. One failing alert does not stop the others.</td></tr>
</tbody></table>

**Compared fields:**

<table border=1><thead><tr><th>Field</th><th>Shown in Changes as</th><th>Comparison</th></tr></thead><tbody>
<tr><td><code>ProcessingStatusString</code></td><td>Processing status</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>LLMTriageString</code></td><td>Triage</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>LLMFalsePositiveScore</code></td><td>False-positive score</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>CaseId</code></td><td>Falcora case</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>TriageFlags</code></td><td>Triage flags</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>SystemOwnerIds</code></td><td>System owners</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>SystemOwnerClassification</code></td><td>Owner classification</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>SystemOwnerFeedback</code></td><td>Owner feedback</td><td>Reported as <em>added</em> or <em>updated</em></td></tr>
<tr><td><code>SystemOwnerAnswers</code></td><td>Owner answers</td><td>Number of entries compared</td></tr>
<tr><td><code>AIAnsweredQuestions</code></td><td>Questions answered by AI</td><td>Number of entries compared</td></tr>
<tr><td><code>AutoResolvedByAI</code></td><td>Auto-resolved by AI</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>AIAnswerOverridden</code></td><td>AI answer overridden</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>LLMTriageJustification</code></td><td>Triage justification</td><td>Reported as <em>added</em> or <em>updated</em></td></tr>
<tr><td><code>SOP</code></td><td>SOP</td><td>Reported as <em>old -&gt; new</em></td></tr>
<tr><td><code>ErrorMessage</code></td><td>Error</td><td>Reported as <em>added</em> or <em>updated</em></td></tr>
<tr><td><code>RetryCount</code></td><td>Retry count</td><td>Reported as <em>old -&gt; new</em></td></tr>
</tbody></table>

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
{
    "Updated": [
        {
            "RecordIRI": "/api/3/alerts/3c5e1f0a-8d2b-4b7e-9f61-0a4d2c8e7b15",
            "AlertId": "e2a7d9c1-6b4f-4e3a-9c85-1f0b7d2e4a96",
            "RecordSeverity": "/api/3/picklists/40187287-89f6-4e6c-89a8-4f4c2c4e2d5d",
            "Changes": [
                "Processing status: triage_in_progress -> completed",
                "Triage: none -> true_positive",
                "False-positive score: none -> 10",
                "Falcora case: none -> 91c2a6e4-3d7b-4f18-b0a5-6e2c8d4f1a73",
                "Triage flags: none -> NO_SOP",
                "Triage justification added"
            ],
            "PreviousAlert": {
                "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
                "AlertId": "e2a7d9c1-6b4f-4e3a-9c85-1f0b7d2e4a96",
                "ProcessingStatus": 30,
                "ProcessingStatusString": "triage_in_progress",
                "PatternName": "Download of multiple files"
            },
            "Alert": {
                "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
                "AlertId": "e2a7d9c1-6b4f-4e3a-9c85-1f0b7d2e4a96",
                "ProcessingStatus": 70,
                "ProcessingStatusString": "completed",
                "LLMTriage": 2,
                "LLMTriageString": "true_positive",
                "LLMFalsePositiveScore": 10,
                "PatternName": "Download of multiple files",
                "CaseId": "91c2a6e4-3d7b-4f18-b0a5-6e2c8d4f1a73",
                "TriageFlags": [
                    "NO_SOP"
                ],
                "…": "all fields of Get Alert Details"
            }
        }
    ],
    "Unchanged": [
        {
            "RecordIRI": "/api/3/alerts/7a2d9e4b-1c6f-4a3e-8b05-d9f2e1c7a640",
            "AlertId": "b8f0c6d2-1c3e-4f0a-8d7e-5a9b2c4e6f10"
        }
    ],
    "NotFound": [
        {
            "RecordIRI": "/api/3/alerts/c1e8b3d7-5f2a-4d96-a0b4-6e3f9c2d8a71",
            "AlertId": "0f6b2e9d-4c1a-4e7b-b3d8-5a9c0e2f6d14"
        }
    ],
    "Errors": [],
    "UpdatedCount": 1
}
```

### operation: Get Cases
Retrieves a list of cases from Falcora based on the time range and filters you have specified. The time range applies to the case creation time.

Falcora API: <code>GET /tenant/cases</code>

Results are unordered unless <strong>Top</strong> is set (then newest by <code>CreatedAt</code>). The Severity filter of the Falcora API matches nothing today, so the connector filters severity client-side on <code>AnalystSeverity</code>, falling back to <code>LLMAnalysisSeverity</code>.

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Top</td><td>Return only the newest N cases by creation time (1 to 1000).<br/><em>Optional</em></td></tr>
<tr><td>Relative Time Range</td><td>Relative time range on the creation time. Cannot be combined with Start Time or End Time.<br/>Options: <code>Last Hour</code>, <code>Last 24 Hours</code>, <code>Last 3 Days</code>, <code>Last 7 Days</code><br/><em>Optional</em></td></tr>
<tr><td>Start Time</td><td>Return records whose creation time is at or after this time (inclusive).<br/><em>Optional</em></td></tr>
<tr><td>End Time</td><td>Return records whose creation time is before this time (exclusive).<br/><em>Optional</em></td></tr>
<tr><td>Processing Status</td><td>Return only cases in this processing status.<br/>Options: <code>Open</code>, <code>Waiting For Owner</code>, <code>Ready For Analysis</code>, <code>Analysis In Progress</code>, <code>Ready For Review</code>, <code>Completed</code>, <code>Error</code><br/><em>Optional</em></td></tr>
<tr><td>Final Verdict</td><td>Return only cases the analyst finalized with this verdict.<br/>Options: <code>Malicious Behaviour</code>, <code>Improper Operation</code>, <code>Not An Issue</code><br/><em>Optional</em></td></tr>
<tr><td>Severity</td><td>Return only cases with this severity (analyst severity, or AI severity if not yet finalized). Filtered by the connector.<br/>Options: <code>Low</code>, <code>Medium</code>, <code>High</code>, <code>Very High</code><br/><em>Optional</em></td></tr>
<tr><td>Processor ID</td><td>Return only cases assigned to this Falcora user object ID.<br/><em>Optional</em></td></tr>
<tr><td>SAP User ID</td><td>Return only cases involving this SAP user name (case-insensitive).<br/><em>Optional</em></td></tr>
<tr><td>System ID</td><td>Return only cases involving this SAP system ID.<br/><em>Optional</em></td></tr>
<tr><td>Changed By</td><td>Return only cases last changed by this identity.<br/><em>Optional</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
[
    {
        "TenantId": "",
        "CaseId": "",
        "CaseTitle": "",
        "ProcessingStatus": "",
        "ProcessingStatusString": "",
        "LLMAnalysisSeverity": "",
        "LLMAnalysisSeverityString": "",
        "LLMRecommendedVerdict": "",
        "LLMRecommendedVerdictString": "",
        "ProcessorId": "",
        "UserIds": [],
        "SystemIds": [],
        "CreatedAt": "",
        "ChangedAt": "",
        "CreatedBy": "",
        "ChangedBy": "",
        "CaseSummaryPending": "",
        "ProcessingMode": "",
        "AnalystFinalVerdict": "",
        "AnalystFinalVerdictString": "",
        "AnalystSeverity": "",
        "AnalystSeverityString": ""
    }
]
```

**Case fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>TenantId, CaseId</code></td><td>string</td><td>Tenant and unique case ID (UUID).</td></tr>
<tr><td><code>CaseTitle</code></td><td>string</td><td>AI-generated case title.</td></tr>
<tr><td><code>ProcessingStatus / ProcessingStatusString</code></td><td>int / string</td><td>Case state, see <a href="#case-processingstatus">Case ProcessingStatus</a>.</td></tr>
<tr><td><code>LLMAnalysisSeverity / LLMAnalysisSeverityString</code></td><td>int / string</td><td>Severity from the AI case analysis, see <a href="#verdicts-and-severity">Verdicts and severity</a>.</td></tr>
<tr><td><code>LLMRecommendedVerdict / LLMRecommendedVerdictString</code></td><td>int / string</td><td>Verdict the AI recommends. The string is upper case, unlike the other <code>…String</code> fields.</td></tr>
<tr><td><code>ProcessorId</code></td><td>string</td><td>Falcora user object ID of the case processor. Only the processor can finalize a case.</td></tr>
<tr><td><code>UserIds, SystemIds</code></td><td>string[]</td><td>SAP users and SAP systems involved in the case.</td></tr>
<tr><td><code>CreatedAt, ChangedAt</code></td><td>ISO 8601</td><td>Creation time (the time filters apply to it) and last status change. <code>ChangedAt</code> moves on status changes only.</td></tr>
<tr><td><code>CreatedBy, ChangedBy</code></td><td>string</td><td>Identity that created or last changed the case.</td></tr>
<tr><td><code>CaseSummaryPending</code></td><td>bool</td><td>Always <code>true</code> in the list, because the list never carries the summary.</td></tr>
<tr><td><code>ProcessingMode</code></td><td>string</td><td>Falcora processing mode of the case, for example <code>Legacy</code>.</td></tr>
<tr><td><code>AnalystFinalVerdict(String), AnalystSeverity(String)</code></td><td>int / string</td><td>The analyst's final decision. Present once the case is finalized.</td></tr>
</tbody></table>

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
[
    {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
        "CaseTitle": "Self-authorization of authorizations on Production SAP system PRD",
        "ProcessingStatus": 15,
        "CreatedAt": "2026-08-25T16:34:37.625Z",
        "ChangedAt": "2026-08-25T16:34:38.268Z",
        "CreatedBy": "system:alert-triage-queue",
        "ChangedBy": "system:alert-triage-queue",
        "UserIds": [
            "JSMITH"
        ],
        "SystemIds": [
            "PRD"
        ],
        "CaseSummaryPending": true,
        "ProcessingMode": "Legacy",
        "ProcessingStatusString": "waiting_for_owner"
    },
    {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "CaseId": "91c2a6e4-3d7b-4f18-b0a5-6e2c8d4f1a73",
        "CaseTitle": "Multiple-file download activity in PRD SAP system involving 12 files in one recorded event",
        "ProcessingStatus": 70,
        "LLMAnalysisSeverity": 30,
        "LLMRecommendedVerdict": 2,
        "LLMRecommendedVerdictString": "IMPROPER_OPERATION",
        "CreatedAt": "2026-11-11T16:51:43.499Z",
        "ChangedAt": "2026-11-11T16:52:04.724Z",
        "CreatedBy": "system:alert-triage-queue",
        "ChangedBy": "system:case-signature-queue",
        "ProcessingMode": "Legacy",
        "UserIds": [
            "JSMITH"
        ],
        "SystemIds": [
            "PRD"
        ],
        "CaseSummaryPending": true,
        "ProcessingStatusString": "ready_for_review",
        "LLMAnalysisSeverityString": "high"
    }
]
```

### operation: Get Case Details
Retrieves the full details of a specific case, including the summary, AI analysis, analyst decision, progress, latest AI investigation, history and comments, based on the case ID you have specified.

Falcora API: <code>GET /tenant/cases/{TenantId}/{CaseId}</code>

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>ID (UUID) of the Falcora case.<br/><em>Required</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "TenantId": "",
    "CaseId": "",
    "CaseTitle": "",
    "ProcessingStatus": "",
    "ProcessingStatusString": "",
    "LLMAnalysisSeverity": "",
    "LLMAnalysisSeverityString": "",
    "LLMRecommendedVerdict": "",
    "LLMRecommendedVerdictString": "",
    "ProcessorId": "",
    "UserIds": [],
    "SystemIds": [],
    "CreatedAt": "",
    "ChangedAt": "",
    "CreatedBy": "",
    "ChangedBy": "",
    "CaseSummaryPending": "",
    "ProcessingMode": "",
    "AnalystFinalVerdict": "",
    "AnalystFinalVerdictString": "",
    "AnalystSeverity": "",
    "AnalystSeverityString": "",
    "CaseSummary": "",
    "CaseSummaryUpdatedAt": "",
    "LLMAnalysisAnalystExecutiveSummary": "",
    "LLMAnalysisAlertSummary": "",
    "LLMAnalysisSOFeedbackSummary": "",
    "LLMAnalysisImpact": "",
    "LLMAnalysisConfidenceLevel": "",
    "LLMAnalysisEvaluatedAt": "",
    "LLMRecommendedVerdictJustification": "",
    "LLMAnalysisRecommendedSteps": [],
    "LLMAnalysisReferences": [],
    "LLMAnalysisSOPIds": [],
    "AnalystUserId": "",
    "AnalystJustification": "",
    "AnalystDeviationReason": "",
    "AnalystEvaluatedAt": "",
    "IncidentLink": "",
    "CaseProgress": {
        "Alerts": {
            "Total": "",
            "TriageDone": "",
            "WaitingForOwnerInput": "",
            "Completed": "",
            "InError": ""
        },
        "OwnerFeedback": {
            "Answered": "",
            "AnsweredByAI": "",
            "Pending": ""
        },
        "Analysis": {
            "State": "",
            "CompletedAt": "",
            "Verdict": "",
            "Severity": "",
            "Confidence": ""
        },
        "AnalystDecision": {
            "State": "",
            "FinalizedAt": "",
            "Verdict": ""
        },
        "LastChangeAt": "",
        "LastChangeByType": ""
    },
    "AIInvestigation": {
        "InvestigationId": "",
        "Mode": "",
        "Status": "",
        "CompletedAt": "",
        "Verdict": "",
        "Confidence": "",
        "Summary": "",
        "EvidenceRefs": [],
        "EvidenceGaps": [],
        "StopReason": "",
        "ContentTrust": ""
    },
    "StatusHistory": [
        {
            "Status": "",
            "StatusName": "",
            "Timestamp": "",
            "ChangedBy": ""
        }
    ],
    "ActionLog": [
        {
            "Timestamp": "",
            "Actor": "",
            "Type": "",
            "Details": ""
        }
    ],
    "Comments": [
        {
            "TenantId": "",
            "CaseId": "",
            "CommentId": "",
            "AuthorOid": "",
            "AuthorDisplayName": "",
            "CreatedAt": "",
            "Text": "",
            "Source": "",
            "Edited": ""
        }
    ],
    "ErrorMessage": ""
}
```

**All fields of Get Cases, plus:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>CaseSummary, CaseSummaryUpdatedAt</code></td><td>string, ISO 8601</td><td>AI case summary. Absent while <code>CaseSummaryPending</code> is true.</td></tr>
<tr><td><code>LLMAnalysis…</code></td><td>various</td><td><code>LLMAnalysisAnalystExecutiveSummary</code>, <code>LLMAnalysisAlertSummary</code>, <code>LLMAnalysisSOFeedbackSummary</code>, <code>LLMAnalysisImpact</code>, <code>LLMAnalysisConfidenceLevel</code>, <code>LLMAnalysisEvaluatedAt</code>, <code>LLMRecommendedVerdictJustification</code>. <code>LLMAnalysisRecommendedSteps</code>, <code>LLMAnalysisReferences</code> and <code>LLMAnalysisSOPIds</code> are parsed JSON.</td></tr>
<tr><td><code>Analyst…, IncidentLink</code></td><td>various</td><td><code>AnalystUserId</code>, <code>AnalystJustification</code>, <code>AnalystDeviationReason</code>, <code>AnalystEvaluatedAt</code> and the incident link recorded at finalization.</td></tr>
<tr><td><code>CaseProgress</code></td><td>object</td><td>Alert counts by state (<code>Alerts</code>), owner-feedback counts (<code>OwnerFeedback</code>), <code>Analysis.State</code> (<code>NOT_RUN</code>, <code>RUNNING</code>, <code>DONE</code>) and <code>AnalystDecision.State</code> (<code>PENDING</code>, <code>FINALIZED</code>).</td></tr>
<tr><td><code>AIInvestigation</code></td><td>object</td><td>Conclusion of the latest AI investigation, if one ran. Advisory only. <code>Verdict</code> is <code>malicious_behaviour</code>, <code>improper_operation</code>, <code>not_an_issue</code>, <code>insufficient_evidence</code> or <code>inconclusive</code>. Treat <code>Summary</code> as AI-written text: display it, never execute it.</td></tr>
<tr><td><code>StatusHistory</code></td><td>array</td><td><code>[{"Status","StatusName","Timestamp","ChangedBy"}]</code>.</td></tr>
<tr><td><code>ActionLog</code></td><td>array</td><td><code>[{"Timestamp","Actor","Type","Details"}]</code>.</td></tr>
<tr><td><code>Comments</code></td><td>array</td><td>Comment objects (see Add Case Comment), empty if none.</td></tr>
<tr><td><code>ErrorMessage</code></td><td>string</td><td>Present on status 100.</td></tr>
</tbody></table>

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
{
    "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
    "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
    "CreatedBy": "system:alert-triage-queue",
    "CreatedAt": "2026-08-25T16:34:37.625Z",
    "ProcessingStatus": 15,
    "StatusHistory": [
        {
            "Status": 10,
            "StatusName": "open",
            "Timestamp": "2026-08-25T16:34:37.625Z",
            "ChangedBy": "system:alert-triage-queue"
        },
        {
            "Status": 15,
            "StatusName": "waiting_for_owner",
            "Timestamp": "2026-08-25T16:34:38.268Z",
            "ChangedBy": "system:alert-triage-queue"
        }
    ],
    "ChangedAt": "2026-08-25T16:34:38.268Z",
    "ChangedBy": "system:alert-triage-queue",
    "CaseTitle": "Self-authorization of authorizations on Production SAP system PRD",
    "ActionLog": [
        {
            "Timestamp": "2026-08-25T16:34:37.626Z",
            "Actor": "system:alert-triage-queue",
            "Type": "CREATED",
            "Details": {}
        }
    ],
    "UserIds": [
        "JSMITH"
    ],
    "SystemIds": [
        "PRD"
    ],
    "CaseSummaryPending": true,
    "ProcessingMode": "Legacy",
    "ProcessingStatusString": "waiting_for_owner",
    "CaseProgress": {
        "Alerts": {
            "Total": 1,
            "TriageDone": 1,
            "WaitingForOwnerInput": 1,
            "Completed": 0,
            "InError": 0
        },
        "OwnerFeedback": {
            "Answered": 0,
            "AnsweredByAI": 0,
            "Pending": 1
        },
        "Analysis": {
            "State": "NOT_RUN"
        },
        "AnalystDecision": {
            "State": "PENDING"
        },
        "LastChangeAt": "2026-08-25T16:34:38.268Z",
        "LastChangeByType": "SYSTEM"
    }
}
```

**Action-specific errors:**

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>404</td><td>The case does not exist. Case ID must be a UUID.</td></tr>
</tbody></table>

### operation: Get Case Alerts
Retrieves the alerts linked to a specific case.

Falcora API: <code>GET /tenant/alerts?TenantId={TenantId}&amp;CaseId={CaseId}</code>

A case does not list its alert IDs itself; this action queries the alert list by case ID.

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>ID (UUID) of the Falcora case.<br/><em>Required</em></td></tr>
<tr><td>Include Details</td><td>Select to read every alert individually to include the raw event and triage details.<br/>Default: <code>False</code><br/><em>Optional</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
[
    {
        "TenantId": "",
        "AlertId": "",
        "AlertType": "",
        "ReceivedAt": "",
        "ProcessingStatus": "",
        "ProcessingStatusString": "",
        "LLMTriage": "",
        "LLMTriageString": "",
        "LLMFalsePositiveScore": "",
        "LLMTriageEvaluatedAt": "",
        "PatternName": "",
        "SystemId": "",
        "SystemOwnerIds": [],
        "SystemOwnerClassification": "",
        "SystemOwnerFeedbackReceivedAt": "",
        "CaseId": "",
        "CaseLinkageReason": "",
        "UserIds": [],
        "SourceIPAddress": "",
        "UserAgent": "",
        "TriageFlags": [],
        "AlertSemanticDescription": "",
        "SOP": {
            "TenantId": "",
            "SOPId": "",
            "Version": ""
        },
        "CreatedBy": "",
        "ChangedBy": ""
    }
]
```

**Same fields as Get Alerts (or Get Alert Details with Include Alert Details):**

**Sample response** (from a Falcora test tenant, IDs, users and addresses anonymized):

```json
[
    {
        "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
        "AlertId": "b8f0c6d2-1c3e-4f0a-8d7e-5a9b2c4e6f10",
        "AlertType": "Xiting SIEM Connector",
        "ReceivedAt": "2026-08-25T16:34:14.443Z",
        "ProcessingStatus": 50,
        "LLMTriage": 2,
        "LLMFalsePositiveScore": 4,
        "LLMTriageEvaluatedAt": "2026-08-25T16:34:32.831Z",
        "PatternName": "Assignment of authorizations to own user",
        "SystemId": "PRD",
        "SystemOwnerIds": [
            "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64"
        ],
        "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
        "UserIds": [
            "JSMITH"
        ],
        "SourceIPAddress": "198.51.100.23",
        "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "TriageFlags": [],
        "CreatedBy": "2f6e1a90-8c4d-4b7e-a1f3-5d9c0e2b7a64",
        "ChangedBy": "system:alert-triage-queue",
        "AlertSemanticDescription": "A production SAP ABAP system logged a user master change event indicating assignment of authorizations to the acting account’s own user in client 000. This is a self-authorization privilege escalation on a sensitive system and is suspicious because it can grant unauthorized access beyond approved business roles.",
        "SOP": {
            "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
            "SOPId": "AssignmentOfAuthorizationsToOwnUser",
            "Version": "1"
        },
        "LLMTriageString": "true_positive",
        "ProcessingStatusString": "waiting_for_owner_input"
    }
]
```

### operation: Add Case Comment
Adds enrichment to a case as a plain-text comment. Comments longer than 1000 characters are split into several comments. The sequence "${" is escaped automatically. Comments cannot be deleted and completed cases do not accept comments.

Falcora API: <code>POST /tenant/cases/{TenantId}/{CaseId}/comments</code>

Comments are plain text, 1-1000 characters each. Longer text is split at line or word boundaries into several comments when <strong>Split Long Comments</strong> is enabled. The sequence <code>${</code> is rewritten to <code>$ {</code>, because the Falcora web application firewall rejects it. Comments cannot be deleted. The output is a wrapper the connector builds around the comments Falcora returned.

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>ID (UUID) of the Falcora case.<br/><em>Required</em></td></tr>
<tr><td>Comment</td><td>Plain text of the comment.<br/><em>Required</em></td></tr>
<tr><td>Prefix</td><td>Text placed in front of every comment so analysts can tell it apart from their own notes.<br/>Default: <code>[FortiSOAR]</code><br/><em>Optional</em></td></tr>
<tr><td>Split Long Comments</td><td>Select to split comments longer than 1000 characters into several comments. If cleared, long comments fail.<br/>Default: <code>True</code><br/><em>Optional</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "CommentCount": "",
    "Comments": [
        {
            "TenantId": "",
            "CaseId": "",
            "CommentId": "",
            "AuthorOid": "",
            "AuthorDisplayName": "",
            "CreatedAt": "",
            "Text": "",
            "Source": "",
            "Edited": ""
        }
    ]
}
```

**Response fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>CommentCount</code></td><td>int</td><td>Number of comments created. Greater than 1 when a long comment was split.</td></tr>
<tr><td><code>Comments[].CommentId</code></td><td>string (UUID)</td><td>ID of the created comment.</td></tr>
<tr><td><code>Comments[].AuthorOid, AuthorDisplayName</code></td><td>string</td><td>Author of the comment, that is, the connection credential.</td></tr>
<tr><td><code>Comments[].CreatedAt, EditedAt</code></td><td>int</td><td>Epoch milliseconds.</td></tr>
<tr><td><code>Comments[].Text</code></td><td>string</td><td>Text as stored, including the prefix. <code>${</code> is stored as <code>$ {</code>.</td></tr>
<tr><td><code>Comments[].Source</code></td><td>string</td><td><code>manual</code>, or <code>trigger-analysis</code> for comments created by Trigger Case Analysis.</td></tr>
<tr><td><code>Comments[].Edited</code></td><td>bool</td><td>Whether the comment was edited.</td></tr>
</tbody></table>

**Sample response** (example from the Falcora Integration API documentation):

```json
{
    "CommentCount": 1,
    "Comments": [
        {
            "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
            "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
            "CommentId": "e3b1a4c2-7f5d-4a9e-b2c6-8d1f3e5a7b90",
            "AuthorOid": "5c0b9e3a-2d4f-4e6a-8b1c-3f5d7e9a0b24",
            "AuthorDisplayName": "FortiSOAR Integration",
            "CreatedAt": 1790151302417,
            "Text": "[FortiSOAR] 10.20.4.17 also appears in FortiSIEM incident 88121 (VPN login from a new country, 07:52 UTC).",
            "Source": "manual",
            "Edited": false
        }
    ]
}
```

**Action-specific errors:**

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>400</td><td>Text is blank, longer than 1000 characters or otherwise invalid.</td></tr>
<tr><td>404</td><td>The case does not exist.</td></tr>
<tr><td>409</td><td>The case is completed (read-only), or an automated run or pending AI proposal holds it (<code>CASE_LOCKED_BY_RUN_…</code>, <code>CASE_LOCKED_BY_PROPOSAL_…</code>). Retry later.</td></tr>
</tbody></table>

### operation: Assign Case Processor
Sets or clears the processor of a case.

Falcora API: <code>POST /tenant/cases/{TenantId}/{CaseId}/actions/assign-processor</code>

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>ID (UUID) of the Falcora case.<br/><em>Required</em></td></tr>
<tr><td>Assignee</td><td>Select Specific User to assign the case to a Falcora user, or Clear Processor to remove the processor.<br/>Options: <code>Specific User</code>, <code>Clear Processor</code><br/>Default: <code>Specific User</code><br/><em>Required</em></td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;Processor ID</td><td>If you choose <code>Specific User</code>: Falcora user object ID of the new processor.<br/><em>Required</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "Status": "",
    "Message": "",
    "TenantId": "",
    "CaseId": "",
    "ProcessorId": ""
}
```

**Response fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>Status, Message</code></td><td>string</td><td><code>OK</code> and <code>Case processor assigned</code> on success.</td></tr>
<tr><td><code>TenantId, CaseId</code></td><td>string</td><td>The case that was changed.</td></tr>
<tr><td><code>ProcessorId</code></td><td>string</td><td>The new processor, or <code>null</code> when the processor was cleared.</td></tr>
</tbody></table>

**Sample response** (example from the Falcora Integration API documentation):

```json
{
    "Status": "OK",
    "Message": "Case processor assigned",
    "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
    "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
    "ProcessorId": "5c0b9e3a-2d4f-4e6a-8b1c-3f5d7e9a0b24"
}
```

**Action-specific errors:**

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>400</td><td>The value is unchanged, or the user is not an active user holding <code>Tenant.Cases.Write</code> directly on the tenant.</td></tr>
<tr><td>404</td><td>The case does not exist.</td></tr>
<tr><td>409</td><td>The case is completed.</td></tr>
</tbody></table>

### operation: Trigger Case Analysis
Re-runs the AI case analysis, for example after adding significant enrichment. Also reopens completed cases for analysis.

Falcora API: <code>POST /tenant/cases/{TenantId}/{CaseId}/actions/trigger-analysis</code>

Use this after adding significant enrichment, so the AI analysis takes it into account. The reason is stored on the case as a comment. On a completed case this reopens it for analysis.

#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Tenant ID</td><td>ID of the Falcora tenant. Leave empty to use the Tenant ID from the connector configuration.<br/><em>Optional</em></td></tr>
<tr><td>Case ID</td><td>ID (UUID) of the Falcora case.<br/><em>Required</em></td></tr>
<tr><td>Reason</td><td>Reason for the re-run, up to 1000 characters. Stored on the case as a comment.<br/><em>Required</em></td></tr>
</tbody></table>

#### Output
The output contains the following populated JSON schema:

```json
{
    "Status": "",
    "Message": "",
    "ProcessingStatus": ""
}
```

**Response fields:**

<table border=1><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody>
<tr><td><code>Status, Message</code></td><td>string</td><td><code>Accepted</code> (HTTP 202): the analysis was queued.</td></tr>
<tr><td><code>ProcessingStatus</code></td><td>int</td><td><code>30</code> (ready_for_analysis). Poll Get Case Details to follow the analysis.</td></tr>
</tbody></table>

**Sample response** (example from the Falcora Integration API documentation):

```json
{
    "Status": "Accepted",
    "Message": "…",
    "TenantId": "7d2c9f40-5b1e-4c7a-9a55-0f3e2d1b8c61",
    "CaseId": "4a1d7e2b-9c0f-4b6e-8a31-2e5f7c9d0b12",
    "ProcessingStatus": 30
}
```

**Action-specific errors:**

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>400</td><td>The reason is missing.</td></tr>
<tr><td>404</td><td>The case does not exist.</td></tr>
<tr><td>409</td><td>An analysis is already running (status 50).</td></tr>
</tbody></table>

## Value reference
Picklist parameters accept the label shown below or the raw API value.

### Alert ProcessingStatus
<table border=1><thead><tr><th>Code</th><th>String</th><th>Picklist label</th><th>Meaning</th></tr></thead><tbody>
<tr><td>10</td><td>open</td><td>Open</td><td>Received, waiting for triage.</td></tr>
<tr><td>30</td><td>triage_in_progress</td><td>Triage In Progress</td><td>AI triage running.</td></tr>
<tr><td>50</td><td>waiting_for_owner_input</td><td>Waiting For Owner Input</td><td>Triaged; waiting for the system owner's answers.</td></tr>
<tr><td>60</td><td>blocked_quota_exceeded</td><td>Blocked Quota Exceeded</td><td>Stored but held: the tenant's monthly allowance is used up.</td></tr>
<tr><td>70</td><td>completed</td><td>Completed</td><td>Triage (and owner feedback, if any) complete.</td></tr>
<tr><td>100</td><td>error</td><td>Error</td><td>Triage failed; see <code>ErrorMessage</code>.</td></tr>
</tbody></table>

### Case ProcessingStatus
<table border=1><thead><tr><th>Code</th><th>String</th><th>Picklist label</th><th>Meaning</th></tr></thead><tbody>
<tr><td>10</td><td>open</td><td>Open</td><td>Created; alerts still being processed.</td></tr>
<tr><td>15</td><td>waiting_for_owner</td><td>Waiting For Owner</td><td>At least one alert awaits owner feedback.</td></tr>
<tr><td>30</td><td>ready_for_analysis</td><td>Ready For Analysis</td><td>Queued for AI case analysis.</td></tr>
<tr><td>50</td><td>analysis_in_progress</td><td>Analysis In Progress</td><td>AI case analysis running.</td></tr>
<tr><td>70</td><td>ready_for_review</td><td>Ready For Review</td><td>Analysis done; waiting for the analyst's verdict.</td></tr>
<tr><td>90</td><td>completed</td><td>Completed</td><td>Verdict finalized; read-only.</td></tr>
<tr><td>100</td><td>error</td><td>Error</td><td>Analysis failed.</td></tr>
</tbody></table>

### Triage
<table border=1><thead><tr><th>Code</th><th>String</th><th>Picklist label</th></tr></thead><tbody>
<tr><td>1</td><td>false_positive</td><td>False Positive</td></tr>
<tr><td>2</td><td>true_positive</td><td>True Positive</td></tr>
</tbody></table>

### Verdicts and severity
<table border=1><thead><tr><th>Code</th><th>Verdict (AnalystFinalVerdict, LLMRecommendedVerdict)</th><th>Picklist label</th></tr></thead><tbody>
<tr><td>1</td><td>MALICIOUS_BEHAVIOUR</td><td>Malicious Behaviour</td></tr>
<tr><td>2</td><td>IMPROPER_OPERATION</td><td>Improper Operation</td></tr>
<tr><td>3</td><td>NOT_AN_ISSUE</td><td>Not An Issue</td></tr>
</tbody></table>

<table border=1><thead><tr><th>Code</th><th>Severity (AnalystSeverity, LLMAnalysisSeverity)</th><th>Picklist label</th></tr></thead><tbody>
<tr><td>10</td><td>LOW</td><td>Low</td></tr>
<tr><td>20</td><td>MEDIUM</td><td>Medium</td></tr>
<tr><td>30</td><td>HIGH</td><td>High</td></tr>
<tr><td>40</td><td>VERY_HIGH</td><td>Very High</td></tr>
</tbody></table>

Alerts carry no severity of their own; the source's priority is kept in <code>AlertData.PRIO</code>.

### Relative time range
<table border=1><thead><tr><th>Picklist label</th><th>API value</th></tr></thead><tbody>
<tr><td>Last Hour</td><td>LastHour</td></tr>
<tr><td>Last 24 Hours</td><td>Last24Hours</td></tr>
<tr><td>Last 3 Days</td><td>Last3Days</td></tr>
<tr><td>Last 7 Days</td><td>Last7Days</td></tr>
</tbody></table>

Start Time and End Time accept a FortiSOAR date/time, an ISO 8601 string or an epoch value (seconds or milliseconds) and are sent as ISO 8601 UTC. Start Time is inclusive, End Time exclusive. A relative range cannot be combined with Start Time or End Time.

## Error handling
Every failed request raises a connector error of the form <code>Falcora API error &lt;status&gt;: &lt;hint&gt; - &lt;Falcora message&gt;</code>.

<table border=1><thead><tr><th>HTTP status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>401 <code>Invalid credentials</code></td><td>Wrong username or password, or the Tenant ID is not the tenant the credential was created for. A credential is valid for exactly one tenant.</td></tr>
<tr><td>403 <code>Unable to identify user: missing OID claim</code></td><td>The credential is not permitted to call this endpoint. Check the roles listed under Minimum Permissions Required.</td></tr>
<tr><td>403 with an HTML body</td><td>The Falcora web application firewall rejected the request: body larger than 128 KB, or containing <code>${</code>.</td></tr>
<tr><td>404 with an HTML body</td><td>The API URL is missing the <code>/backend/api</code> path prefix.</td></tr>
<tr><td>429</td><td>Rate limited. GET requests are retried once when Falcora sends a <code>Retry-After</code> of up to 60 seconds.</td></tr>
</tbody></table>

## Included playbooks
The `Sample - Xiting Falcora - 1.0.0` playbook collection comes bundled with the Xiting Falcora connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR&trade; after importing the Xiting Falcora connector.

- `Get Alerts`
- `Get Alert Details`
- `Get Cases`
- `Get Case Details`
- `Get Case Alerts`
- `Add Case Comment`
- `Assign Case Processor`
- `Trigger Case Analysis`
- `> Xiting Falcora > Fetch`
- `> Xiting Falcora > Create Record`
- `Xiting Falcora > Ingest`
- `Xiting Falcora > Sync Alerts`
- `> Xiting Falcora > Update Record`

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection since the sample playbook collection gets deleted during connector upgrade and delete.

## Data Ingestion Support
Use the Data Ingestion Wizard to easily ingest Falcora alerts into FortiSOAR&trade; as alerts on a schedule. The ingestion follows the polling pattern Xiting recommends: it reads the alerts Falcora received in a time window, then remembers the end of the window for the next run.

### Configuring data ingestion
1. Open the <strong>Xiting Falcora</strong> connector, select the <strong>Configure Data Ingestion</strong> button and click <strong>Configure</strong>. You need a working connector configuration first.
2. On the <strong>Fetch Sample Data</strong> page, set the ingestion parameters below and click <strong>Fetch</strong>. The wizard runs the fetch playbook once to show sample alerts.
3. On the <strong>Field Mapping</strong> page, review how Falcora fields map to FortiSOAR alert fields (see the table below) and adjust them if required, then click <strong>Save Mapping &amp; Continue</strong>.
4. On the <strong>Scheduling</strong> page, enable the schedule and set the interval, for example every 5 minutes, then click <strong>Save Settings &amp; Continue</strong>.
5. On the <strong>Summary</strong> page, click <strong>Done</strong>. FortiSOAR now runs the <code>Xiting Falcora &gt; Ingest</code> playbook on the schedule.

### Ingestion parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody>
<tr><td>Pull Alerts Received in Past X Minutes</td><td>On the first run, pull the alerts received in the past X minutes. Later runs continue from the last pull time.<br/>Default: <code>60</code></td></tr>
<tr><td>Triage Delay (Minutes)</td><td>Only pull alerts received at least this many minutes ago, so Falcora has time to finish AI triage. Set to 0 to pull immediately.<br/>Default: <code>5</code></td></tr>
<tr><td>Overlap (Minutes)</td><td>Overlap consecutive pull windows by this many minutes. Alerts fetched twice are upserted on the Falcora alert ID (Source ID). Set to 0 if the unique constraint of the Alerts module (Source ID by default) was changed.<br/>Default: <code>1</code></td></tr>
<tr><td>Include Alert Details</td><td>Read each alert individually to include the raw event (AlertData), triage justification, SOP and owner feedback. Makes one extra request per alert.<br/>Default: <code>True</code></td></tr>
</tbody></table>

### How the ingestion works
<table border=1><thead><tr><th>Playbook</th><th>What it does</th></tr></thead><tbody>
<tr><td><code>Xiting Falcora &gt; Ingest</code></td><td>Entry point that the schedule runs. Calls the fetch playbook, then the create playbook once per returned alert.</td></tr>
<tr><td><code>&gt; Xiting Falcora &gt; Fetch</code></td><td>Reads the last pull time from the global variable <code>XitingFalcoraLastPullTime_&lt;playbook id&gt;</code> (created on the first run). Computes the window <code>[last pull time - Overlap, now - Triage Delay)</code>, or <code>[now - Triage Delay - X minutes, now - Triage Delay)</code> on the first run. Runs <strong>Get Alerts</strong> with that window, optionally with alert details, and stores the window end as the new last pull time.</td></tr>
<tr><td><code>&gt; Xiting Falcora &gt; Create Record</code></td><td>Creates one FortiSOAR alert per Falcora alert, with the Falcora <code>AlertId</code> as the alert Source ID. The step runs in <em>Overwrite</em> (upsert) mode, so an alert fetched twice because of the overlap updates the existing record, because the Alerts module is unique on <strong>Source ID</strong> by default. If that constraint was changed in the Module Editor, set <strong>Overlap</strong> to 0.</td></tr>
</tbody></table>

### Field mapping
<table border=1><thead><tr><th>FortiSOAR alert field</th><th>Value</th></tr></thead><tbody>
<tr><td>Name</td><td><code>PatternName</code> (fallback: <code>Xiting Falcora Alert</code>)</td></tr>
<tr><td>Description</td><td><code>AlertData.MESSAGE</code> (fallback: <code>AlertSemanticDescription</code>), followed by the Falcora triage verdict and false-positive score, processing status, SAP system, SAP users, Falcora case ID, triage flags and the AI triage justification</td></tr>
<tr><td>Severity</td><td>See the severity mapping below</td></tr>
<tr><td>Source</td><td><code>Xiting Falcora</code></td></tr>
<tr><td>Source ID</td><td><code>AlertId</code></td></tr>
<tr><td>Source Data</td><td>The complete Falcora alert as JSON</td></tr>
<tr><td>Type, State, Status</td><td>Defaults of the FortiSOAR alert module</td></tr>
</tbody></table>

### Severity mapping
Falcora alerts carry no severity of their own. The FortiSOAR severity is derived in this order; the first rule that matches wins:

<table border=1><thead><tr><th>Rule</th><th>FortiSOAR severity</th></tr></thead><tbody>
<tr><td><code>AlertData.PRIO</code> is <code>VERY HIGH</code>, <code>VERY_HIGH</code>, <code>CRITICAL</code> or <code>CRIT</code></td><td>Critical</td></tr>
<tr><td><code>AlertData.PRIO</code> is <code>HIGH</code></td><td>High</td></tr>
<tr><td><code>AlertData.PRIO</code> is <code>MEDIUM</code> or <code>MED</code></td><td>Medium</td></tr>
<tr><td><code>AlertData.PRIO</code> is <code>LOW</code></td><td>Low</td></tr>
<tr><td>Falcora triage is false positive (<code>LLMTriage</code> = 1)</td><td>Low</td></tr>
<tr><td>Falcora triage is true positive (<code>LLMTriage</code> = 2) and <code>LLMFalsePositiveScore</code> &le; 20</td><td>High</td></tr>
<tr><td>Anything else, including numeric <code>PRIO</code> values and alerts still in triage</td><td>Medium</td></tr>
</tbody></table>

<code>PRIO</code> is free text "as the source expresses it", and numeric values (for example SAP Security Audit Log severities) have no fixed scale, so they fall through to the triage-based rules. <code>PRIO</code> is only available when <strong>Include Alert Details</strong> is enabled.

### Keeping ingested alerts in sync
Falcora keeps working on an alert after FortiSOAR ingested it: triage finishes, the system owner answers, the AI answers questions, the alert moves to another case. Falcora has no change feed, so the <code>Xiting Falcora &gt; Sync Alerts</code> playbook polls for these changes and mirrors them into the FortiSOAR alerts.

<table border=1><thead><tr><th>Playbook</th><th>What it does</th></tr></thead><tbody>
<tr><td><code>Xiting Falcora &gt; Sync Alerts</code></td><td>Entry point to run on a schedule. Finds the FortiSOAR alerts with source <code>Xiting Falcora</code> that are not Closed and were created in the last <code>maxAgeDays</code> days, newest first and at most <code>batchSize</code>. Runs <strong>Get Alert Updates</strong> on them and calls the update playbook once per changed alert. The <em>Summary</em> step reports how many alerts were updated, unchanged, not found or failed.</td></tr>
<tr><td><code>&gt; Xiting Falcora &gt; Update Record</code></td><td>Updates one FortiSOAR alert: rebuilds the description, replaces the Source Data with the current Falcora alert and recalculates the severity (see below). When <code>addComment</code> is true it adds a comment to the alert listing what changed.</td></tr>
</tbody></table>

**What is updated and what is not:** Description, Source Data and Severity follow Falcora. The severity is only changed while it still equals the severity derived from the previously stored Falcora data; once an analyst sets a different severity, it is kept. State, Status, Assigned To and all other fields are never touched, so the analyst workflow in FortiSOAR stays in FortiSOAR.

**Setting it up:**

1. Clone <code>Xiting Falcora &gt; Sync Alerts</code> and <code>&gt; Xiting Falcora &gt; Update Record</code> into your own collection, and update the playbook reference in the <em>Update Changed Alerts</em> step to your clone of the update playbook.
2. Adjust the <em>Configuration</em> step if required: <code>maxAgeDays</code> (default 7), <code>batchSize</code> (default 100, at most 200) and <code>addComment</code> (default true).
3. Activate both playbooks, then go to <strong>Automation &gt; Schedules</strong> and create a schedule that runs <code>Xiting Falcora &gt; Sync Alerts</code>, for example every 15 minutes. Run it less often than the ingestion: each alert costs one Falcora request.

### Limitations
- Falcora has no change feed. Changes reach FortiSOAR only through the sync playbook, at its schedule interval, and only for open alerts younger than <code>maxAgeDays</code>.
- Each run checks at most <code>batchSize</code> alerts, newest first. If more open Falcora alerts exist, the oldest ones are not checked; raise <code>batchSize</code> or close alerts that need no further sync.
- Alerts that Falcora no longer returns are listed in the Summary step as not found and left unchanged in FortiSOAR.
- Falcora does not page the alert list. Keep the schedule interval short, so each run reads a small window.
- Alerts over the monthly Falcora allowance wait in status 60 (Blocked Quota Exceeded) and are ingested with that status.
