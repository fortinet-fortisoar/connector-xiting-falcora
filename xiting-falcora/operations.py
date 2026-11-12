"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""
import json
from urllib.parse import quote

from connectors.core.connector import get_logger, ConnectorError

from .constants import *
from .utils import FalcoraClient, map_value, to_iso8601, to_bool, split_text, sanitize_text

logger = get_logger(LOGGER_NAME)


def _path(*segments):
    return '/'.join(quote(str(s).strip(), safe='') for s in segments)


def _required(params, name, label):
    value = params.get(name)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ConnectorError('{0} is required'.format(label))
    return value.strip() if isinstance(value, str) else value


def _time_filters(params):
    relative = map_value(params.get('timestamp_relative'), TIMESTAMP_RELATIVE, 'Relative Time Range')
    timestamp_from = to_iso8601(params.get('timestamp_from'))
    timestamp_to = to_iso8601(params.get('timestamp_to'))
    if relative and (timestamp_from or timestamp_to):
        raise ConnectorError('Relative Time Range cannot be combined with Start Time or End Time')
    return {'TimestampRelative': relative, 'timestampFrom': timestamp_from, 'timestampTo': timestamp_to}


def _limit(records, params):
    limit = params.get('limit')
    if limit not in (None, '') and int(limit) > 0 and isinstance(records, list):
        return records[:int(limit)]
    return records


# ---------------- Alerts ----------------

def get_alerts(config, params):
    client = FalcoraClient(config)
    query = {
        'TenantId': client.tenant_id(params),
        'CaseId': params.get('case_id'),
        'SystemId': params.get('system_id'),
        'ProcessingStatus': map_value(params.get('processing_status'), ALERT_PROCESSING_STATUS, 'Processing Status'),
        'Triage': map_value(params.get('triage'), TRIAGE, 'Triage'),
        'SystemOwnerId': params.get('system_owner_id'),
        'AlertType': params.get('alert_type')
    }
    query.update(_time_filters(params))
    alerts = _limit(client.request('GET', '/tenant/alerts', params=query), params)
    if to_bool(params.get('include_details')) and isinstance(alerts, list):
        alerts = [_alert_details(client, alert) for alert in alerts]
    return alerts


def _alert_details(client, alert):
    details = client.request('GET', '/tenant/alerts/' + _path(alert.get('TenantId'), alert.get('AlertId')),
                             allow_404=True)
    return details if details else alert


def get_alert_details(config, params):
    client = FalcoraClient(config)
    alert_id = _required(params, 'alert_id', 'Alert ID')
    return client.request('GET', '/tenant/alerts/' + _path(client.tenant_id(params), alert_id))


def _parse_json(value, label):
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return json.loads(value)
        except ValueError:
            raise ConnectorError('{0} is not valid JSON'.format(label))
    return value


def _known_alert(item):
    """Accept a FortiSOAR alert record, its source data, or a plain Falcora alert ID."""
    if isinstance(item, str) and not item.strip().startswith(('{', '[')):
        return {}, {'AlertId': item.strip()}
    item = _parse_json(item, 'Alert')
    if not isinstance(item, dict):
        raise ConnectorError('Each entry in Alerts must be an alert record, alert object or alert ID')
    if 'sourcedata' in item or '@id' in item:
        previous = _parse_json(item.get('sourcedata'), 'Source Data') or {}
        if not previous.get('AlertId') and item.get('sourceId'):
            previous = dict(previous, AlertId=item.get('sourceId'))
        severity = item.get('severity')
        if isinstance(severity, dict):
            severity = severity.get('@id')
        return {'RecordIRI': item.get('@id'), 'RecordSeverity': severity}, previous
    return {}, item


def _display(value):
    if value is None or value == '' or value == []:
        return 'none'
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    if isinstance(value, dict):
        if 'SOPId' in value:
            return '{0} v{1}'.format(value.get('SOPId'), value.get('Version'))
        return json.dumps(value, sort_keys=True)
    return str(value)


def _alert_changes(previous, current):
    changes = []
    for field, label, mode in SYNC_TRACKED_FIELDS:
        old, new = previous.get(field), current.get(field)
        if mode == 'count':
            old, new = len(old or []), len(new or [])
        if old == new or (old in (None, '', []) and new in (None, '', [])):
            continue
        if mode == 'text':
            changes.append('{0} {1}'.format(label, 'added' if old in (None, '') else 'updated'))
        else:
            changes.append('{0}: {1} -> {2}'.format(label, _display(old), _display(new)))
    return changes


def get_alert_updates(config, params):
    client = FalcoraClient(config)
    known = _parse_json(params.get('alerts'), 'Alerts')
    if isinstance(known, (str, dict)):
        known = [known]
    if not known:
        raise ConnectorError('Alerts is required')
    if len(known) > MAX_SYNC_ALERTS:
        raise ConnectorError('At most {0} alerts can be checked per call'.format(MAX_SYNC_ALERTS))
    result = {'Updated': [], 'Unchanged': [], 'NotFound': [], 'Errors': []}
    for item in known:
        record, previous = _known_alert(item)
        ref = {'RecordIRI': record.get('RecordIRI'), 'AlertId': None}
        alert_id = (previous.get('AlertId') or '').strip()
        if not alert_id:
            result['Errors'].append(dict(ref, Error='No Falcora alert ID found'))
            continue
        ref['AlertId'] = alert_id
        tenant_id = previous.get('TenantId') or client.tenant_id(params)
        try:
            current = client.request('GET', '/tenant/alerts/' + _path(tenant_id, alert_id), allow_404=True)
        except ConnectorError as err:
            result['Errors'].append(dict(ref, Error=str(err)))
            continue
        if current is None:
            result['NotFound'].append(ref)
            continue
        changes = _alert_changes(previous, current)
        if changes:
            result['Updated'].append(dict(ref, RecordSeverity=record.get('RecordSeverity'), Changes=changes,
                                          PreviousAlert=previous, Alert=current))
        else:
            result['Unchanged'].append(ref)
    result['UpdatedCount'] = len(result['Updated'])
    return result


# ---------------- Cases ----------------

def get_cases(config, params):
    client = FalcoraClient(config)
    query = {
        'TenantId': client.tenant_id(params),
        'Top': params.get('top') or None,
        'ProcessingStatus': map_value(params.get('processing_status'), CASE_PROCESSING_STATUS, 'Processing Status'),
        'FinalVerdict': map_value(params.get('final_verdict'), VERDICT, 'Final Verdict'),
        'ProcessorId': params.get('processor_id'),
        'UserId': params.get('user_id'),
        'SystemId': params.get('system_id'),
        'ChangedBy': params.get('changed_by')
    }
    query.update(_time_filters(params))
    cases = client.request('GET', '/tenant/cases', params=query)
    # The API's Severity filter matches nothing today, so severity is filtered client-side
    severity = map_value(params.get('severity'), SEVERITY, 'Severity')
    if severity and isinstance(cases, list):
        cases = [c for c in cases if c.get('AnalystSeverity', c.get('LLMAnalysisSeverity')) == severity]
    return cases


def get_case_details(config, params):
    client = FalcoraClient(config)
    case_id = _required(params, 'case_id', 'Case ID')
    return client.request('GET', '/tenant/cases/' + _path(client.tenant_id(params), case_id))


def get_case_alerts(config, params):
    client = FalcoraClient(config)
    case_id = _required(params, 'case_id', 'Case ID')
    alerts = client.request('GET', '/tenant/alerts', params={'TenantId': client.tenant_id(params), 'CaseId': case_id})
    if to_bool(params.get('include_details')) and isinstance(alerts, list):
        alerts = [_alert_details(client, alert) for alert in alerts]
    return alerts


def add_case_comment(config, params):
    client = FalcoraClient(config)
    case_id = _required(params, 'case_id', 'Case ID')
    text = sanitize_text(_required(params, 'text', 'Comment'))
    prefix = params.get('prefix') or ''
    if prefix and not prefix.endswith(' '):
        prefix += ' '
    if to_bool(params.get('split_long_comments'), default=True):
        chunks = split_text(text, MAX_COMMENT_LENGTH, prefix)
    else:
        chunks = [prefix + text]
        if len(chunks[0]) > MAX_COMMENT_LENGTH:
            raise ConnectorError('Comment exceeds {0} characters. Enable "Split Long Comments" or shorten it'.format(
                MAX_COMMENT_LENGTH))
    endpoint = '/tenant/cases/{0}/comments'.format(_path(client.tenant_id(params), case_id))
    comments = [client.request('POST', endpoint, body={'Text': chunk}) for chunk in chunks]
    return {'CommentCount': len(comments), 'Comments': comments}


def assign_case_processor(config, params):
    client = FalcoraClient(config)
    case_id = _required(params, 'case_id', 'Case ID')
    assignee = params.get('assignee') or 'Specific User'
    if assignee == 'Clear Processor':
        processor_id = None
    else:
        processor_id = _required(params, 'processor_id', 'Processor ID')
    return client.request('POST', '/tenant/cases/{0}/actions/assign-processor'.format(
        _path(client.tenant_id(params), case_id)), body={'ProcessorId': processor_id})


def trigger_case_analysis(config, params):
    client = FalcoraClient(config)
    case_id = _required(params, 'case_id', 'Case ID')
    comment = _required(params, 'comment', 'Reason')
    if len(comment) > MAX_TEXT_LENGTH:
        raise ConnectorError('Reason exceeds {0} characters'.format(MAX_TEXT_LENGTH))
    return client.request('POST', '/tenant/cases/{0}/actions/trigger-analysis'.format(
        _path(client.tenant_id(params), case_id)), body={'Comment': comment})


def check_health(config):
    client = FalcoraClient(config)
    # The connection credential is scoped to one tenant and has no Falcora user identity, so /info/me is not
    # available. A narrow alert query verifies the credential and its access to the tenant.
    client.request('GET', '/tenant/alerts', params={'TenantId': client.tenant_id({}),
                                                     'TimestampRelative': TIMESTAMP_RELATIVE['Last Hour']})
    return True


operations = {
    'get_alerts': get_alerts,
    'get_alert_details': get_alert_details,
    'get_alert_updates': get_alert_updates,
    'get_cases': get_cases,
    'get_case_details': get_case_details,
    'get_case_alerts': get_case_alerts,
    'add_case_comment': add_case_comment,
    'assign_case_processor': assign_case_processor,
    'trigger_case_analysis': trigger_case_analysis
}
