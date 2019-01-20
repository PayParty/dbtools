from .Collection import Collection
from pymongo import MongoClient

class Database:
# Database
#
# Represents a database contained in a server and may
# contain one or more collections.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with database name
  #   collections: list of Collection objects
  #   address: string with database address relative to server root
  #

    if from_plain:
      self.__class = 'Database'
      self.name = from_plain.get('name', '')
      self.collections = list(map(
        lambda collection: Collection(from_plain=collection)
      , from_plain.get('collections', [])))
      self.address = from_plain.get('address', '')
    else:
      self.__class = 'Database'
      self.name = kwargs.get('name', '')
      self.__collections = []
      self.collections = kwargs.get('collections', [])
      self.address = kwargs.get('address', '')

  def __repr__(self):

    return (
      'Database object \'{name}\' containing {col_count} collection(s).'.format(name=self.name, col_count=len(self.collections))
    )
  
  def analyze(self, targets, write, client):

    # Get database from client
    #
    client_database = client[self.address]

    # Open database in log file
    #
    write('object_start')
    write('object_key', 'database')
    write('object_value', self.name)
    write('object_key', 'collections')
    write('array_start', True)

    # Call analyze in collections
    target_collections = list(filter(
      lambda collection: collection.name in targets
    , self.collections))
    _ = list(map(
      lambda collection: collection.analyze(write=write, client=client_database)
    , target_collections))

    # Close database in log file
    #
    write('array_end')
    write('object_end')

  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the Database object
  #

    plain_collections = list(map(
      lambda collection: collection.to_plain()
    , self.collections))
    
    return {
      '__class': self.__class,
      'name': self.name,
      'collections': plain_collections,
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
  def collections(self):
    return self.__collections
  @collections.setter
  def collections(self, new_collections):
    if isinstance(new_collections, list):
      self.__collections = new_collections
  
  def add_collections(self, new_collections):
    if isinstance(new_collections, list):
      self.__collections.extend(new_collections)
  
  def has_collection(self, b):
    for collection in self.collections:
      if collection == b:
        return True
    return False
  
  @property
  def address(self):
    return self.__address
  @address.setter
  def address(self, new_address):
    if isinstance(new_address, str):
      self.__address = new_address
