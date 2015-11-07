#!/usr/bin/env python

class Type(object):
  ''' The basic abstract object for type '''
  def __init__(self_, name):
    self_.name_ = name

  def __eq__(self_, other):
    return self_ == other

  def __neq__(self_, other):
    return not self_.__eq__(other)

  def get_name(self_):
    return self_.name_

  def hash_code(self_):
    return self_.hash_code_cache

  def is_array(self_):
    raise NotImplementedError('is_array not implemented')

  def is_complex(self_):
    raise NotImplementedError('is_complex not implemented')

  def is_extending(self_):
    raise NotImplementedError('is_extending not implemented')

  def is_extending_or_extended_by(self_, other):
    ''' For hierachical type ontology '''
    raise NotImplementedError('is_extending_or_extended_by not implemented')

  def __str__(self_):
    return ''

  def __hash__(self_):
    return hash(self_.name_)

  #def read_resolve(self_):
  #  ''' querying the type repository and get the equivalent class '''
  #  return LogicalLanguageServices.get_type_repository().get_type_create_if_needed(self_.name_)
