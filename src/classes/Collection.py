from .Property import Property
from .ObjectProperty import ObjectProperty
from .ControlledObjectProperty import ControlledObjectProperty
from .ArrayProperty import ArrayProperty
from pymongo import MongoClient
from os import mkdir
from json import dumps

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
  elif prop_class == 'ArrayProperty':
    return ArrayProperty(from_plain=prop)
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

  def analyze(self, client, log_path):

    # Initialize logs
    #
    log_path = log_path + '/{collection}'.format(collection=self.address)
    mkdir(log_path)

    # Get cursor from client database
    #
    cursor = client[self.address].find({})

    # Document analysis
    #
    def analyze_document(document, log_path):

      document_results = {}
      document_id = document.get('_id', 'no_id')

      def add_result(output, name, value):
        if value:
          output[name] = value

      _ = list(map(
        lambda prop: add_result(document_results, prop.name, prop.analyze(document.pop(prop.name, None)))
      , self.properties))

      _ = list(map(
        lambda prop: add_result(document_results, prop[0], 'unexpected property')
      , list(document.items())))

      if any(list(document_results.values())):
        with open(log_path+'/'+str(document_id)+'.log', 'w') as log_file:
          log_file.write(dumps(document_results))
        
      issues = 0
      try:
        issues += len(list(document_results.items()))
      except:
        pass
      return {
        'properties': issues
      } 

    # Iterate documents in collection
    #
    document_returns = list(map(
      lambda document: analyze_document(document, log_path)
    , cursor))

    # Count issues
    #
    issues_documents = 0
    try:
      issues_documents += len(document_returns)
    except:
      pass
    issues_properties = 0
    try:
      issues_properties += sum(list(map( lambda document: document['properties'], document_returns )))
    except:
      pass

    # Create collection summary
    #
    with open(log_path+'/_{collection}.log'.format(collection=self.address), 'w') as log_file:
      log_file.write(dumps({
        'collection': self.name,
        'address': self.address,
        'issues': {
          'documents': issues_documents,
          'properties': issues_properties
        }
      })) 

    return {
      'documents': issues_documents,
      'properties': issues_properties
    }

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
