from .Property import Property

class ObjectProperty:
# ObjectProperty
#
# Represents a property of a model which is an object,
# itself containing other properties.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with property name
  #   type: string with property type
  #   properties: list of Property objects
  #   optional: whether or not the property is optional (bool)
  #

    if from_plain:
      self.__class = 'ObjectProperty'
      self.name = from_plain.get('name', '')
      self.type = 'ObjectProperty'
      self.properties = list(map(
        lambda prop: Property(from_plain=prop)
      , from_plain.get('properties', [])))
      self.optional = from_plain.get('optional', False)
    else:
      self.__class = 'ObjectProperty'
      self.name = kwargs.get('name', '')
      self.type = 'ObjectProperty'
      self.__properties = []
      self.properties = kwargs.get('properties', [])
      self.optional = kwargs.get('optional', False)
  
  def __repr__(self):

    return (
      'ObjectProperty object \'{name}\' containing {prop_count} properties.'.format(name=self.name, prop_count=len(self.properties))
    )
  
  def analyze(self, document_property):

    if document_property == None:
      
      if self.optional:
        return None
      else:
        return 'missing property'

    else:

      property_results = {}

      def add_result(output, name, value):
        if value:
          output[name] = value
      
      _ = list(map(
        lambda prop: add_result(property_results, prop.name, prop.analyze(document_property.pop(prop.name, None)))
      , self.properties))

      _ = list(map(
        lambda prop: add_result(property_results, prop[0], 'unexpected property')
      , document_property))

      if any(list(property_results.values())):
        return 'issues in {count} properties'.format(count=sum(list(map( lambda prop: 0 if prop == None else 1, property_results ))))
      else:
        return None

  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the ObjectProperty object
  #

    plain_properties = list(map(
      lambda prop: prop.to_plain()
    , self.properties))
    
    return {
      '__class': self.__class,
      'name': self.name,
      'type': self.type,
      'optional': self.optional,
      'properties': plain_properties
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
  def properties(self):
    return self.__properties
  @properties.setter
  def properties(self, new_properties):
    if isinstance(new_properties, list):
      self.__properties = new_properties
  
  def add_properties(self, new_properties):
    if isinstance(new_properties, list):
      self.__properties.extend(new_properties)
  
  def has_property(self, b):
    for prop in self.properties:
      if prop == b:
        return True
    return False

  @property
  def optional(self):
    return self.__optional
  @optional.setter
  def optional(self, new_optional):
    if isinstance(new_optional, bool):
      self.__optional = new_optional
