from .Database import Database
from pymongo import MongoClient

class Server:
# Server
#
# Represents a server contained in an environment and may
# contain one or more databases.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with server name
  #   databases: list of Database objects
  #   connection_string: string with server's connection string
  #

    if from_plain:
      self.__class = 'Server'
      self.name = from_plain.get('name', '')
      self.databases = list(map(
        lambda database: Database(from_plain=database)
      , from_plain.get('databases', [])))
      self.connection_string = from_plain.get('connection_string', '')
    else:
      self.__class = 'Server'
      self.name = kwargs.get('name', '')
      self.__databases = []
      self.databases = kwargs.get('databases', [])
      self.connection_string = kwargs.get('connection_string', '')

  def __repr__(self):

    return (
      'Server object \'{name}\' containing {db_count} database(s).'.format(name=self.name, db_count=len(self.databases))
    )

  def analyze(self):

    client = MongoClient(self.connection_string)

    return list(map(
      lambda database: database.analyze(client[database.address])
    , self.databases))
  
  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the Server object
  #

    plain_databases = list(map(
      lambda database: database.to_plain()
    , self.databases))

    return {
      '__class': self.__class,
      'name': self.name,
      'databases': plain_databases,
      'connection_string': self.connection_string
    }
  
  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, new_name):
    if isinstance(new_name, str):
      self.__name = new_name
  
  @property
  def databases(self):
    return self.__databases
  @databases.setter
  def databases(self, new_databases):
    if isinstance(new_databases, list):
      self.__databases = new_databases
  
  def add_databases(self, new_databases):
    if isinstance(new_databases, list):
      self.__databases.extend(new_databases)
  
  def has_database(self, b):
    for database in self.databases:
      if database == b:
        return True
    return False
  
  @property
  def connection_string(self):
    return self.__connection_string
  @connection_string.setter
  def connection_string(self, new_connection_string):
    if isinstance(new_connection_string, str):
      self.__connection_string = new_connection_string
