from .Property import Property
from .ObjectProperty import ObjectProperty
from .ControlledObjectProperty import ControlledObjectProperty
from pymongo import MongoClient

def prop_from_plain(prop):
# prop_from_plain
#
# Auxiliary function that creates an object based on a
# plain python dictionary using its __class property as
# reference. Applied in from_plain construction of
# Collection as a mapping function.
#
  prop_class = prop.get('__class', '')
  if prop_class == 'Property':
    return Property(from_plain=prop)
  elif prop_class == 'ObjectProperty':
    return ObjectProperty(from_plain=prop)
  elif prop_class == 'ControlledObjectProperty':
    return ControlledObjectProperty(from_plain=prop)
  else:
    pass

class Collection:
# Collection
#
# Represents the model of a document in a collection,
# contained in a database. It contains, in turn, all
# properties associated with the document model.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with collection name
  #   properties: list of Property, ObjectProperty and ControlledObjectProperty objects
  #   address: string with collection address relative to server
  #

    if from_plain:
      self.__class = 'Collection'
      self.name = from_plain.get('name', '')
      self.properties = list(map(
        lambda prop: prop_from_plain(prop)
      , from_plain.get('properties', [])))
      self.address = from_plain.get('address', '')
    else:
      self.__class = 'Collection'
      self.name = kwargs.get('name', '')
      self.__properties = []
      self.properties = kwargs.get('properties', [])
      self.address = kwargs.get('address', '')

  def __repr__(self):

    return (
      'Collection object \'{name}\' containing {prop_count} properties.'.format(name=self.name, prop_count=len(self.properties))
    )

  def analyze(self, write, client):

    # Get cursor from client database
    #
    cursor = client[self.address].find({})

    # Open collection in log file
    #
    write('object_start')
    write('object_key', 'collection')
    write('object_value', self.name)
    write('object_key', 'documents')
    write('array_start', True)

    # Build documents
    #
    def analyze_document(document, write):

      # Open document in log file
      #
      write('object_start')

      # Write unexpected properties
      #
      def write_unexpected(prop_name, write):
        
        write('object_key', prop_name)
        write('object_value', 'unexpected property')

      _ = list(map(
        lambda prop: prop.analyze(document.get(prop.name, None), write)
      , self.properties))

      _ = list(map(
        lambda prop: write_unexpected(prop[0], write)
      , list(document.items())))

      # Close document in log file
      #
      write('object_end')

    # Iterate documents in collection
    #
    _ = list(map(
      lambda document: analyze_document(document, write)
    , cursor))

    # Close collection in log file
    #
    write('array_end')
    write('object_end')

  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the Collection object
  #

    plain_properties = list(map(
      lambda prop: prop.to_plain()
    , self.properties))
    
    return {
      '__class': self.__class,
      'name': self.name,
      'properties': plain_properties,
      'address': self.address
    }
  
  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, new_name):
    if isinstance(new_name, str):
      self.__name = new_name
  
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
  def address(self):
    return self.__address
  @address.setter
  def address(self, new_address):
    if isinstance(new_address, str):
      self.__address = new_address
