from .Server import Server

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
    else:
      self.__class = 'Environment'
      self.name = kwargs.get('name', '')
      self.__servers = []
      self.servers = kwargs.get('servers', [])
      self.filepath = kwargs.get('filepath', '')

  def __repr__(self):

    return (
      'Environment object \'{name}\' containing {s_count} server(s)'.format(name=self.name, s_count=len(self.servers))
    )
  
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
      'filepath': self.filepath
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