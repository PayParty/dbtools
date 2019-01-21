from .Server import Server
from json import dumps, loads
from pprint import pprint
from datetime import datetime

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

    # Initialize log file
    #
    logfile_path = self.filepath + str(datetime.now()) + '.log'
    logfile = open(logfile_path, 'w')
    logfile.write('')
    logfile.close()

    # This auxiliary function writes to the log file based on a
    # set of actions, and makes use of external variables to
    # keep track of the indentation level (and yes, I understand
    # the negative consequences of this).
    #
    global indent
    indent = 0
    global first_element
    first_element = True
    def write_to_logs(filepath, action, data=None):

      logfile = open(filepath, 'a')
      global indent
      global first_element

      # 'object_start' represents an action to open a pair of
      # curly braces, representing, in JSON, an object. The data
      # argument of a call with this action represents the
      # boolean value of whether this object is a value in a
      # key-value pair
      #
      if action == 'object_start':
        if not data and not first_element:
          logfile.write(',')
        logfile.write('{')
        indent += 1
        first_element = True

      elif action == 'object_key':
        if first_element:
          first_element = False
        else:
          logfile.write(',')
        logfile.write('\n{indent}\'{key}\': '.format(indent='  '*indent, key=str(data)))

      elif action == 'object_value':
        if isinstance(data, str):
          logfile.write('\'{value}\''.format(value=data))
        elif isinstance(data, int) or isinstance(data, float):
          logfile.write('{value}'.format(value=str(data)))
        elif isinstance(data, bool):
          logfile.write('{value}'.format(value='true' if data else 'false'))
        elif isinstance(data, type(None)):
          logfile.write('null')
        else:
          try:
            logfile.write('{value}'.format(value=str(data)))
          except:
            pass

      elif action == 'object_end':
        first_element = False
        indent -= 1
        logfile.write('\n{indent}}}'.format(indent='  '*indent))

      # 'array_start' represents an action to open a pair of
      # square brackets, representing, in JSON, an array. The data
      # argument of a call with this action represents the boolean
      # value of whether this array is a value in a key-value pair
      #
      elif action == 'array_start':
        if not data and not first_element:
          logfile.write(',')
        logfile.write('[')
        indent += 1
        first_element = True

      elif action == 'array_element':
        if first_element:
          first_element = False
        else:
          logfile.write(',')
        logfile.write('\n{indent}'.format(indent='  '*indent))
        if isinstance(data, str):
          logfile.write('\'{value}\''.format(value=data))
        elif isinstance(data, int) or isinstance(data, float):
          logfile.write('{value}'.format(value=str(data)))
        elif isinstance(data, bool):
          logfile.write('{value}'.format(value='true' if data else 'false'))
        elif isinstance(data, type(None)):
          logfile.write('null')
        else:
          try:
            logfile.write('{value}'.format(value=str(data)))
          except:
            pass

      elif action == 'array_end':
        first_element = False
        indent -= 1
        logfile.write('\n{indent}]'.format(indent='  '*indent))

      logfile.close()

    # Open environment in log file
    #
    write_to_logs(logfile_path, 'object_start')
    write_to_logs(logfile_path, 'object_key', 'environment')
    write_to_logs(logfile_path, 'object_value', self.name)
    write_to_logs(logfile_path, 'object_key', 'servers')   
    write_to_logs(logfile_path, 'array_start', True)

    # Call analyze in servers
    #
    target_servers = list(filter(
      lambda server: server.name in self.targets.keys()
    , self.servers))
    _ = list(map(
      lambda server: server.analyze(targets=self.targets[server.name], write=lambda action, data=None: write_to_logs(logfile_path, action, data))
    , target_servers))
    
    # Close environment in log file
    #
    write_to_logs(logfile_path, 'array_end')
    write_to_logs(logfile_path, 'object_end')

    return logfile_path
  
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