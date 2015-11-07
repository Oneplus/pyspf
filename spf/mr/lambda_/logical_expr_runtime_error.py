#!/usr/bin/env python

class LogicalExpressionRuntimeError(RuntimeError):
  def __init__(self_, message):
    super(LogicalExpressionRuntimeError, self_).__init__(message)
