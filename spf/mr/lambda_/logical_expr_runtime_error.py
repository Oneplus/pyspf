#!/usr/bin/env python


class LogicalExpressionRuntimeError(RuntimeError):
    def __init__(self, message):
        super(LogicalExpressionRuntimeError, self).__init__(message)
