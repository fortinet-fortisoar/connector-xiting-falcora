"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""
import re
import time
from datetime import datetime, timezone

import requests
from requests.auth import HTTPBasicAuth
from connectors.core.connector import get_logger, ConnectorError

from .constants import *

logger = get_logger(LOGGER_NAME)


class FalcoraClient(object):

    def __init__(self, config):
        self.config = config
        environment = config.get('environment') or ENV_TEST
        if environment == ENV_CUSTOM:
            self.api_url = (config.get('api_url') or '').strip().rstrip('/')
            if not self.api_url:
                raise ConnectorError('API URL is required for a custom environment')
        else:
            self.api_url = ENVIRONMENTS.get(environment)
            if not self.api_url:
                raise ConnectorError('Unknown environment: {0}'.format(environment))
        if not self.api_url.startswith('https://') and not self.api_url.startswith('http://'):
            self.api_url = 'https://' + self.api_url
        self.username = (config.get('username') or '').strip()
        self.password = config.get('password')
        if not self.username or not self.password:
            raise ConnectorError('Username and Password are required')
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.default_tenant_id = (config.get('tenant_id') or '').strip()
        self.verify_ssl = config.get('verify_ssl', True)

    # ---------- requests ----------

    def request(self, method, endpoint, params=None, body=None, allow_404=False):
        url = self.api_url + endpoint
        if params:
            params = {k: v for k, v in params.items() if v is not None and v != ''}
        if body is not None:
            body = sanitize_payload(body)
        response = self._send(method, url, params, body)
        if response.status_code == 429 and method.upper() == 'GET':
            wait = _retry_after(response)
            if wait is not None:
                time.sleep(wait)
                response = self._send(method, url, params, body)
        if allow_404 and response.status_code == 404:
            return None
        return self._handle_response(response)

    def _send(self, method, url, params, body):
        headers = {'Accept': 'application/json'}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        try:
            logger.debug('{0} {1} params={2}'.format(method, url, params))
            return requests.request(method, url, params=params, json=body, headers=headers, auth=self.auth,
                                    timeout=REQUEST_TIMEOUT, verify=self.verify_ssl)
        except requests.exceptions.SSLError as err:
            raise ConnectorError('SSL certificate validation failed: {0}'.format(err))
        except requests.exceptions.ConnectionError as err:
            raise ConnectorError('Unable to connect to Falcora at {0}: {1}'.format(self.api_url, err))
        except requests.exceptions.Timeout:
            raise ConnectorError('Request to Falcora timed out after {0} seconds'.format(REQUEST_TIMEOUT))

    def _handle_response(self, response):
        if response.ok:
            if response.status_code == 204 or not response.content:
                return {'Status': response.status_code}
            try:
                return response.json()
            except ValueError:
                return {'Status': response.status_code, 'Response': response.text}
        message = _error_message(response)
        logger.error('Falcora API error {0}: {1}'.format(response.status_code, message))
        raise ConnectorError('Falcora API error {0}: {1}'.format(response.status_code, message))

    # ---------- helpers ----------

    def tenant_id(self, params, required=True):
        tenant_id = (params.get('tenant_id') or self.default_tenant_id or '').strip()
        if required and not tenant_id:
            raise ConnectorError('Tenant ID is required. Set it on the action or in the connector configuration')
        return tenant_id or None


def _retry_after(response):
    value = response.headers.get('Retry-After')
    try:
        wait = int(value)
    except (TypeError, ValueError):
        return None
    return wait if 0 < wait <= 60 else None


def _error_message(response):
    content_type = response.headers.get('Content-Type', '')
    if 'html' in content_type.lower():
        if response.status_code == 403:
            return ('Request rejected by the web application firewall (body larger than 128 KB or '
                    'containing "${"). Response was HTML, not JSON.')
        if response.status_code == 404:
            return 'HTML 404 from the edge. Check the API URL contains the path prefix, e.g. /backend/api'
        return 'Unexpected HTML response'
    try:
        body = response.json()
    except ValueError:
        return response.text or response.reason
    if not isinstance(body, dict):
        return str(body)
    parts = []
    if response.status_code == 401:
        if body.get('errorCode') == 'UNAUTHENTICATED':
            parts.append('This endpoint does not accept Basic authentication with the connection credential')
        else:
            parts.append('Authentication failed. Check the Username and Password, and that the Tenant ID is '
                         'the tenant the connection credential was created for')
    elif response.status_code == 403 and 'OID claim' in str(body.get('Message', '')):
        parts.append('The connection credential is not permitted to call this endpoint. Check that it '
                     'belongs to this tenant and has the required role')
    for key in ('Message', 'message', 'errorMessage', 'Error', 'error', 'errorCode'):
        if body.get(key) and body.get(key) not in parts:
            parts.append(str(body.get(key)))
    errors = body.get('Errors')
    if errors:
        parts.append('; '.join(str(e) for e in errors) if isinstance(errors, list) else str(errors))
    for key in ('CurrentStatus', 'RetryAfterSeconds'):
        if key in body:
            parts.append('{0}: {1}'.format(key, body[key]))
    return ' - '.join(parts) if parts else str(body)


def sanitize_text(value):
    if isinstance(value, str):
        return value.replace(WAF_FORBIDDEN_SEQUENCE, WAF_REPLACEMENT_SEQUENCE)
    return value


def sanitize_payload(payload):
    if isinstance(payload, dict):
        return {k: sanitize_payload(v) for k, v in payload.items()}
    if isinstance(payload, list):
        return [sanitize_payload(v) for v in payload]
    return sanitize_text(payload)


_ISO_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?\s*(Z|[+-]\d{2}:?\d{2})?$')


def to_iso8601(value):
    """Convert a FortiSOAR datetime, ISO string or epoch value to an ISO 8601 UTC string with Z."""
    if value is None or value == '':
        return None
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.strip().isdigit()):
        number = float(value)
        if number > 1e11:
            number = number / 1000.0
        dt = datetime.fromtimestamp(number, tz=timezone.utc)
    else:
        text = str(value).strip()
        match = _ISO_RE.match(text)
        if not match:
            raise ConnectorError('Invalid date/time value: {0}'.format(value))
        year, month, day, hour, minute, second, fraction, offset = match.groups()
        micro = int((fraction or '0')[:6].ljust(6, '0'))
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second or 0), micro)
        if offset and offset != 'Z':
            sign = 1 if offset[0] == '+' else -1
            digits = offset[1:].replace(':', '')
            delta_minutes = sign * (int(digits[:2]) * 60 + int(digits[2:]))
            dt = datetime.fromtimestamp(dt.replace(tzinfo=timezone.utc).timestamp() - delta_minutes * 60,
                                        tz=timezone.utc)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.') + '{0:03d}Z'.format(dt.microsecond // 1000)


def map_value(value, mapping, name):
    """Map a picklist label to its API value. Raw API values are passed through."""
    if value is None or value == '':
        return None
    if value in mapping:
        return mapping[value]
    if value in mapping.values():
        return value
    if isinstance(value, str) and value.strip().lstrip('-').isdigit():
        number = int(value.strip())
        if number in mapping.values():
            return number
    raise ConnectorError('Invalid {0}: {1}. Valid values: {2}'.format(name, value, ', '.join(mapping.keys())))


def to_bool(value, default=False):
    if value is None or value == '':
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('true', '1', 'yes', 'y')


def split_text(text, max_length, prefix=''):
    """Split text into chunks of at most max_length characters, each starting with prefix."""
    size = max_length - len(prefix)
    if size <= 0:
        raise ConnectorError('Comment prefix is longer than {0} characters'.format(max_length))
    chunks = []
    remaining = text
    while remaining:
        if len(remaining) <= size:
            chunks.append(remaining)
            break
        cut = remaining.rfind('\n', 0, size)
        if cut < size // 2:
            cut = remaining.rfind(' ', 0, size)
        if cut < size // 2:
            cut = size
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    return [prefix + chunk for chunk in chunks]
