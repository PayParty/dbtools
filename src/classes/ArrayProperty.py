from .Property import Property
from bson import ObjectId

class ArrayProperty:
# ArrayProperty
#
# Represents a property of a model which is na array,
# containing values of a specific type.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with property name
  #   type: string with property name
  #   property_type: string with type of array elements
  #   optional: whether or not the property is optional (bool)
  #

    if from_plain:
      self.__class = 'ArrayProperty'
      self.name = from_plain.get('name', '')
      self.type = 'ArrayProperty'
      self.property_type = from_plain.get('property_type', 'Any')
      self.optional = from_plain.get('optional', False)
    else:
      self.__class = 'ArrayProperty'
      self.name = kwargs.get('name', '')
      self.type = 'ArrayProperty'
      self.property_type = kwargs.get('property_type', 'Any')
      self.optional = kwargs.get('optional', False)

  def __repr__(self):

    return (
      'ArrayProperty object \'{name}\' of type {type}'.format(name=self.name, type=self.property_type)
    )

  def analyze(self, document_property, write):
    
    # Create key in log file
    #
    write('object_key', self.name)

    if document_property and isinstance(document_property, list):

      # Open array in log file
      #
      write('array_start', True)

      # Analyze and write elements
      #
      def write_element(element, write):

        if self.property_type == 'Any':
          write('array_element', None)
        
        elif self.property_type == 'ObjectID':
          if isinstance(element, ObjectId):
            write('array_element', None)
          else:
            write('array_element', 'invalid type')
        
        elif self.property_type == 'String':
          if isinstance(element, str):
            write('array_element', None)
          else:
            write('array_element', 'invalid type')
        
        elif self.property_type == 'Number':
          if isinstance(element, int) or isinstance(element, float):
            write('array_element', None)
          else:
            write('array_element', 'invalid type')
        
        elif self.property_type == 'Boolean':
          if isinstance(element, bool):
            write('array_element', None)
          else:
            write('array_element', 'invalid type')

      # Analyze elements
      #
      _ = list(map(
        lambda element: write_element(element, write)
      , document_property))

    else:

      if self.optional:
        write('object_value', None)
      else:
        write('object_value', 'missing property')

  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the ArrayProperty object
  #

    return {
      '__class': self.__class,
      'name': self.name,
      'type': self.type,
      'property_type': self.property_type,
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
  def property_type(self):
    return self.__property_type
  @property_type.setter
  def property_type(self,new_property_type):
    if isinstance(new_property_type, str):
      self.__property_type = new_property_type
  
  @property
  def optional(self):
    return self.__optional
  @optional.setter
  def optional(self, new_optional):
    if isinstance(new_optional, bool):
      self.__optional = new_optional
