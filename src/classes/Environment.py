from .Server import Server
from json import dumps, loads
from pprint import pprint
from datetime import datetime
from os import mkdir

class Environment:
# Environment
#
# Represents a configuration environment which may contain
# one or more servers. It is created by the dbtool CLI and
# can be saved and restored from .dbconfig files.
#

  def __init__(self, from_plain=None, **kwargs):
  # Constructor
  #
  # Properties
  #   __class: string with object class
  #   name: string with environment name
  #   servers: list of Server objects
  #   filepath: relative path to .dbconfig file associated to environment
  #

    if from_plain:
      self.__class = 'Environment',
      self.name = from_plain.get('name', '')
      self.servers = list(map(
        lambda server: Server(from_plain=server)
      , from_plain.get('servers', [])))
      self.filepath = from_plain.get('filepath', '')
      self.targets = loads(from_plain.get('targets', {}))
    else:
      self.__class = 'Environment'
      self.name = kwargs.get('name', '')
      self.__servers = []
      self.servers = kwargs.get('servers', [])
      self.filepath = kwargs.get('filepath', '')
      self.targets = kwargs.get('targets', {})

  def __repr__(self):

    return (
      'Environment object \'{name}\' containing {s_count} server(s)'.format(name=self.name, s_count=len(self.servers))
    )

  def analyze(self):
  # analyze
  #
  # Calls analysis functions in a nest recursion fashion
  # towards specified targets passing to them the write
  # function. As the target argument gets passed down, it
  # gets mutated so that calls to analyze with very specific
  # targets always provide the required context and data for
  # accessing the servers to the relevant objects.
  #

    # Initialize logs
    #
    log_path = self.filepath + str(datetime.now())
    mkdir(log_path)

    # Call analyze in servers
    #
    target_servers = list(filter(
      lambda server: server.name in self.targets.keys()
    , self.servers))
    server_returns = list(map(
      lambda server: server.analyze(targets=self.targets[server.name], log_path))
    , target_servers)

    # Count issues
    #
    issues_servers = 0
    try:
      issues_servers += len(list(server_returns.items()))
    except:
      pass
    issues_databases = 0
    try:
      issues_databases += sum(list(map( lambda server: server['collections'], server_returns )))
    except:
      pass
    issues_collections = 0
    try:
      issues_collections += sum(list(map( lambda server: server['databases'], server_returns )))
    except:
      pass
    issues_documents = 0
    try:
      issues_documents += sum(list(map( lambda server: server['documents'], server_returns )))
    except:
      pass
    issues_properties = 0
    try:
      issues_properties += sum(list(map( lambda server: server['properties'], server_returns )))
    except:
      pass

    # Create environment summary
    #
    with open(log_path+'/_{environment}.log'.format(environment=self.name), 'w') as log_file:
      log_file.write(dumps({
        'environment': self.name,
        'servers': list(map(
          lambda server: server.name
        , self.servers)),
        'analysisTargets': self.targets.keys(),
        'issues': {
          'servers': issues_servers,
          'databases': issues_databases,
          'collections': issues_collections,
          'documents': issues_documents,
          'properties': issues_properties
        }
      }))

    return {
      'path': log_path,
      'issues': {
        'servers': issues_servers,
        'databases': issues_databases,
        'collections': issues_collections,
        'documents': issues_documents,
        'properties': issues_properties
      }
    }
  
  def to_plain(self):
  # to_plain
  #
  # Returns a plain python object representing the Environment object
  #

    plain_servers = list(map(
      lambda server: server.to_plain()
    , self.servers))
    
    return {
      '__class': self.__class,
      'name': self.name,
      'servers': plain_servers,
      'filepath': self.filepath,
      'targets': dumps(self.targets)
    }
  
  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, new_name):
    if isinstance(new_name, str):
      self.__name = new_name

  @property
  def servers(self):
    return self.__servers
  @servers.setter
  def servers(self, new_servers):
    if isinstance(new_servers, list):
      self.__servers = new_servers
  
  def add_servers(self, new_servers):
    if isinstance(new_servers, list):
      self.__servers.extend(new_servers)
  
  def has_server(self, b):
    for server in self.servers:
      if server == b:
        return True
    return False
  
  @property
  def filepath(self):
    return self.__filepath
  @filepath.setter
  def filepath(self, new_filepath):
    if isinstance(new_filepath, str):
      self.__filepath = new_filepath
  
  @property
  def targets(self):
    return self.__targets
  @targets.setter
  def targets(self, new_targets):
    if isinstance(new_targets, dict):
      self.__targets = new_targets