from bson import ObjectId

class Property:
# Property
#
# Represents a simple property contained in a model.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   _class: string with object class
  #   name: string with property name
  #   type: string with property type
  #   optional: whether or not the property is optional (bool)
  #

    if from_plain:
      self.__class = 'Property'
      self.name = from_plain.get('name', '')
      self.type = from_plain.get('type', 'None')
      self.optional = from_plain.get('optional', False)
    else:
      self.__class = 'Property'
      self.name = kwargs.get('name', '')
      self.type = kwargs.get('type', 'None')
      self.optional = kwargs.get('optional', False)

  def __repr__(self):

    return (
      'Property object \'{name}\' of type {type}.'.format(name=self.name, type=self.type)
    )
  
  def analyze(self, document_property, write):
    
    # Open property in log file
    #
    write('object_key', self.name)

    if document_property:

      if self.type == 'ObjectID':
        if isinstance(document_property, ObjectId):
          write('object_value', None)
        else:
          write('object_value', 'invalid type')

      elif self.type == 'String':
        if isinstance(document_property, str):
          write('object_value', None)
        else:
          write('object_value', 'invalid type')
      
      elif self.type == 'Number':
        if isinstance(document_property, int) or isinstance(document_property, float):
          write('object_value', None)
        else:
          write('object_value', 'invalid type')
      
      elif self.type == 'Boolean':
        if isinstance(document_property, bool):
          write('object_value', None)
        else:
          write('object_value', 'invalid type')
      
      elif self.type == 'Any':
        write('object_value', None)

    else:

      if self.optional:
        write('object_value', None)
      else:
        write('object_value', 'missing property')
  
  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the Property object
  #

    return {
      '__class': self.__class,
      'name': self.name,
      'type': self.type,
      'optional': self.optional
    }

  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, new_name):
    if isinstance(new_name, str):
      self.__name = new_name
  
  @property
  def type(self):
    return self.__type
  @type.setter
  def type(self, new_type):
    if isinstance(new_type, str):
      self.__type = new_type
  
  @property
  def optional(self):
    return self.__optional
  @optional.setter
  def optional(self, new_optional):
    if isinstance(new_optional, bool):
      self.__optional = new_optional
