"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""
LOGGER_NAME = 'xiting-falcora'
REQUEST_TIMEOUT = 120

ENV_TEST = 'Test'
ENV_PRODUCTION = 'Production'
ENV_CUSTOM = 'Custom'

ENVIRONMENTS = {
    ENV_TEST: 'https://api.falcora-test.xiting.com/backend/api',
    ENV_PRODUCTION: 'https://api.falcora.xiting.com/backend/api'
}

# The API host sits behind a WAF that rejects bodies above ~128 KB and bodies containing "${"
WAF_FORBIDDEN_SEQUENCE = '${'
WAF_REPLACEMENT_SEQUENCE = '$ {'
MAX_COMMENT_LENGTH = 1000
MAX_TEXT_LENGTH = 1000
MAX_SYNC_ALERTS = 200

# Alert fields compared by Get Alert Updates: (field, label, mode). Mode "value" reports old -> new,
# "count" compares list lengths, "text" only reports that a long text was added or updated.
SYNC_TRACKED_FIELDS = [
    ('ProcessingStatusString', 'Processing status', 'value'),
    ('LLMTriageString', 'Triage', 'value'),
    ('LLMFalsePositiveScore', 'False-positive score', 'value'),
    ('CaseId', 'Falcora case', 'value'),
    ('TriageFlags', 'Triage flags', 'value'),
    ('SystemOwnerIds', 'System owners', 'value'),
    ('SystemOwnerClassification', 'Owner classification', 'value'),
    ('SystemOwnerFeedback', 'Owner feedback', 'text'),
    ('SystemOwnerAnswers', 'Owner answers', 'count'),
    ('AIAnsweredQuestions', 'Questions answered by AI', 'count'),
    ('AutoResolvedByAI', 'Auto-resolved by AI', 'value'),
    ('AIAnswerOverridden', 'AI answer overridden', 'value'),
    ('LLMTriageJustification', 'Triage justification', 'text'),
    ('SOP', 'SOP', 'value'),
    ('ErrorMessage', 'Error', 'text'),
    ('RetryCount', 'Retry count', 'value'),
]

ALERT_PROCESSING_STATUS = {
    'Open': 10,
    'Triage In Progress': 30,
    'Waiting For Owner Input': 50,
    'Blocked Quota Exceeded': 60,
    'Completed': 70,
    'Error': 100
}

CASE_PROCESSING_STATUS = {
    'Open': 10,
    'Waiting For Owner': 15,
    'Ready For Analysis': 30,
    'Analysis In Progress': 50,
    'Ready For Review': 70,
    'Completed': 90,
    'Error': 100
}

TRIAGE = {
    'False Positive': 1,
    'True Positive': 2
}

VERDICT = {
    'Malicious Behaviour': 1,
    'Improper Operation': 2,
    'Not An Issue': 3
}

SEVERITY = {
    'Low': 10,
    'Medium': 20,
    'High': 30,
    'Very High': 40
}

TIMESTAMP_RELATIVE = {
    'Last Hour': 'LastHour',
    'Last 24 Hours': 'Last24Hours',
    'Last 3 Days': 'Last3Days',
    'Last 7 Days': 'Last7Days'
}
