from .Property import Property

class ControlledObjectProperty:
# ControlledObjectProperty
#
# Represents a property of a model which is an object
# and contains a boolean property which controls whether
# or not the other properties within it are expected.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with property name
  #   type: string with property type
  #   controller: Property object with type 'bool' which acts as the control
  #   properties: list of Property objects
  #   optional: whether or not the property is optional (bool)
  #

    if from_plain:
      self.__class = 'ControlledObjectProperty'
      self.name = from_plain.get('name', '')
      self.type = 'ControlledObjectProperty'
      self.controller = Property(from_plain=from_plain.get('controller', {'name':'yes', 'type':'bool'}))
      self.properties = list(map(
        lambda prop: Property(from_plain=prop)
      , from_plain.get('properties', [])))
      self.optional = from_plain.get('optiona', False)
    else:
      self.__class = 'ControlledObjectProperty'
      self.name = kwargs.get('name', '')
      self.type = 'ControlledObjectProperty'
      self.controller = kwargs.get('controller', Property(name='yes', type='Boolean'))
      self.__properties = []
      self.properties = kwargs.get('properties', [])
      self.optional = kwargs.get('optional', False)
    
  def __repr__(self):

    controller_count = 0
    if self.controller:
      controller_count = 1

    return (
      'ControlledObjectProperty object \'{name}\' containing {cont}+{prop_count} properties.'.format(name=self.name, cont=controller_count, prop_count=len(self.properties))
    )

  def analyze(self, document_property):

    if document_property == None:
      
      if self.optional:
        return None
      else:
        return 'missing property'

    else:

      if not document_property.get(self.controller.name, False):
        return 'missing controller'
      else:
        if not isinstance(document_property.get(self.controller.name, False), bool):
          return 'incorrect controller type'

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
            return 'issues in {count} propertties'.format(count=sum(list(map( lambda prop: 0 if prop == None else 1, property_results ))))
          else:
            return None

  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the ControlledObjectProperty object
  #

    plain_properties = list(map(
      lambda prop: prop.to_plain()
    , self.properties))
    
    return {
      '__class': self.__class,
      'name': self.name,
      'controller': self.controller.to_plain(),
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
  def controller(self):
    return self.__controller
  @controller.setter
  def controller(self, new_controller):
    if isinstance(new_controller, Property):
      if new_controller.type == 'Boolean':
        self.__controller = new_controller
  
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
  
  @property
  def optional(self):
    return self.__optional
  @optional.setter
  def optional(self, new_optional):
    if isinstance(new_optional, bool):
      self.__optional = new_optional
