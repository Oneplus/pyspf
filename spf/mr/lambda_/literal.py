#!/usr/bin/env python

from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType, Option
from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
import logging

class Literal(LogicalExpression):
  LOG = logging.getLogger(__name__)
  PREFIX = LogicalExpression.PARENTHESIS_OPEN

  def __init__(self_, predicate_, arguments_, *args):
    super(Literal, self).__init__()
    self_.predicate_ = predicate_
    self_.arguments_ = arguments_

    if len(args) == 0:
      from spf.mr.lambda_.logic_language_services import LogicLanguageServices
      type_comparator = _.LogicLanguageServices.get_type_comparator()
      type_repository = _.LogicLanguageServices.get_type_repository()
    elif len(args) == 2:
      type_comparator = args[0]
      type_repository = args[1]

    if not predicate_.get_type().is_complex():
      raise LogicalExpressionRuntimeError(
          'Predicate must have a complex type, not %s' % predicate_.get_type())
      literal_typing = self_.compute_literal_typing(
          self_.predicate_.get_type(),
          [arg.get_type() for arg in self_.arguments_],
          type_comparator,
          type_repository)

  def compute_literal_typing(predicate_type, arg_types, type_comparator, type_repository):
    ''' Input the predicate type, a list of argument types. Dealing with the <e,<e,t>> '''
    current_domain = None
    current_range = predicate_type
    current_num_args = 0
    implied_signature_types = []

    for i, arg_type in enumerate(arg_types):
      if not current_range.is_complex():
        break
      current_domain = current_range.get_domain()
      current_range = current_range.get_range()

      if (not type_comparator.verify_arg_type(current_domain, arg_type) and
          isinstance(current_range, RecursiveComplexType) and
          current_range.get_final_range().is_complex()):
        if current_num_args < current_range.get_min_args():
          LOG.debug(
              'Recursive type %s requires a minimum of %d arguments,'
              ' %d were provided.' % (current_range.get_min_args(), current_num_args)
              )
          return None
        current_domain = current_range.get_final_range().get_domain()
        current_range = current_range.get_final_range().get_range()
        current_num_args = 0

        if not type_comparator.verify_arg_type(current_domain, arg_type):
          LOG.debug('Invalid argument type (%s) for signature type (%s)' % (
            arg_type, current_domain))
          return None

        implied_signature_types.append(current_domain)
        current_num_args += 1

        if i+1 < len(arg_type) and not current_range.is_complex():
          LOG.debug('Too many arguments for predicate of type %s: %s' % (
            predicate_type, arg_type))

          if isinstance(current_range, RecursiveComplexType):
            recursive_predicate_type = current_range
            if current_num_args >= recursive_predicate_type.get_min_args():
                return (recursive_predicate_type.get_final_range(), implied_signature_types)
            else:
                return (type_repository.get_type_create_if_needed(
                    recursive_predicate_type.get_domain(),
                    recursive_predicate_type.get_final_range(),
                    Option(
                        recursive_predicate_type.is_order_sensitive(),
                        recursive_predicate_type.get_min_args() - current_num_args)),
                    implied_signature_types)
        else:
            return (current_range, implied_signature_types)
