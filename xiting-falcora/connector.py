"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""
from connectors.core.connector import Connector, get_logger, ConnectorError

from .constants import LOGGER_NAME
from .operations import operations, check_health

logger = get_logger(LOGGER_NAME)


class XitingFalcora(Connector):

    def execute(self, config, operation, params, *args, **kwargs):
        action = operations.get(operation)
        if not action:
            raise ConnectorError('Unsupported operation: {0}'.format(operation))
        try:
            logger.info('Executing operation {0}'.format(operation))
            return action(config, params)
        except ConnectorError:
            raise
        except Exception as err:
            logger.exception(err)
            raise ConnectorError(str(err))

    def check_health(self, config, *args, **kwargs):
        try:
            return check_health(config)
        except ConnectorError:
            raise
        except Exception as err:
            logger.exception(err)
            raise ConnectorError(str(err))
