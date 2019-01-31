from .Database import Database
from pymongo import MongoClient
from os import mkdir
from json import dumps

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

  def analyze(self, targets, log_path):

    # Initialize logs
    #
    log_path = log_path + '/{server}'.format(server=self.name)
    mkdir(log_path)

    # Create connection to server
    #
    client = MongoClient(self.connection_string)

    # Call analyze in databases
    #
    target_databases = list(filter(
      lambda database: database.name in targets.keys()
    , self.databases))
    database_returns = list(map(
      lambda database: database.analyze(targets[database.name], client, log_path)
    , target_databases))

    # Count issues
    #
    issues_databases = 0
    try:
      issues_databases += len(database_returns)
    except:
      pass
    issues_collections = 0
    try:
      issues_collections += sum(list(map( lambda database: database['collections'], database_returns )))
    except:
      pass
    issues_documents = 0
    try:
      issues_documents += sum(list(map( lambda database: database['documents'], database_returns )))
    except:
      pass
    issues_properties = 0
    try:
      issues_properties += sum(list(map( lambda database: database['properties'], database_returns )))
    except:
      pass

    # Create server summary
    #
    with open(log_path+'/_{server}.log'.format(server=self.name), 'w') as log_file:
      log_file.write(dumps({
        'server': self.name,
        'databases': list(map(
          lambda database: {
            'database': database.name,
            'address': database.address
          }
        , self.databases)),
        'analysisTargets': list(targets.keys()),
        'issues': {
          'databases': issues_databases,
          'collections': issues_collections,
          'documents': issues_documents,
          'properties': issues_properties
        }
      }))
    
    return {
      'databases': issues_databases,
      'collections': issues_collections,
      'documents': issues_documents,
      'properties': issues_properties
    }

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
