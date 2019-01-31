from os import listdir
from os.path import isfile, isdir
from json import loads

def analysis_success(log_return):

  print()

  print(
    '\n  Analysis successful\n  Full logs saved in {log_path}'.format(log_path=log_return['path']) +
    '\n  Close environment to view logs\n  Issues found:'+
    '\n    {issues_properties} propert{properties_plural}'.format(issues_properties=log_return['issues']['properties'], properties_plural='y' if log_return['issues']['properties'] == 1 else 'ies') +
    '\n    {issues_documents} document{documents_plural}'.format(issues_documents=log_return['issues']['documents'], documents_plural='' if log_return['issues']['documents'] == 1 else 's') +
    '\n    {issues_collections} collection{collections_plural}'.format(issues_collections=log_return['issues']['collections'], collections_plural='' if log_return['issues']['collections'] == 1 else 's') +
    '\n    {issues_databases} database{databases_plural}'.format(issues_databases=log_return['issues']['databases'], databases_plural='' if log_return['issues']['databases'] == 1 else 's') +
    '\n    {issues_servers} server{servers_plural}\n'.format(issues_servers=log_return['issues']['servers'], servers_plural='' if log_return['issues']['servers'] == 1 else 's')
  )

  return (None, None, False)

def analysis_view(logs_path):
  
  print()

  # Show available logs
  #
  try:
    logs = listdir(logs_path)

    print(
      '\n  Select a log:\n'
    )

    for i in range(0,len(logs)):
      print(
        '    ({i}) {log_name}'.format(i=str(i).center(5, ' '), log_name=logs[i])
      )
    print('\n')
    
    # User
    #
    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(O#) Open log by index   | (X) Back\n'
      )

      if user_input in ['X', 'x']:
        user_input_valid = True
        return (None, None, False)

      elif len(user_input) > 1:
        if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
          try:
            return ('analysis_view_environment', '{logs}/{log}'.format(logs=logs_path, log=logs[int(user_input[1:])]), True)
          except:
            pass
      
      print('\nInvalid input\n\n')

  except:
    return (None, None, False)

def analysis_view_environment(logs_path):
  
  print()

  dir_contents = listdir(logs_path)
  dir_environment = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=logs_path, r_path=path)) and path.endswith('.log')
  , dir_contents))
  dir_servers = list(filter(
    lambda path: isdir('{logs}/{r_path}'.format(logs=logs_path, r_path=path))
  , dir_contents))
  del dir_contents

  try:

    path_environment = '{logs}/{r_path}'.format(logs=logs_path, r_path=dir_environment[0]) 
    del dir_environment

    with open(path_environment, 'r') as file_environment:
      data_environment = loads(file_environment.read())
    del path_environment

    print(
      '  Environment {name}:\n'.format(name=data_environment['environment']) +
      '    {count} issues\n\n'.format(count=data_environment['issues']['properties']) +
      '  Servers:'
    )

    for i in range(0, len(dir_servers)):
      print(
        '    ({i}) {server}'.format(i=str(i).center(5, ' '), server=dir_servers[i])
      )
    print('\n')

    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(O#) Open server by index   | (X) Back\n'
      )

      if user_input in ['X', 'x']:
        user_input_valid = True
        return (None, None, False)
      elif len(user_input) > 1:
        if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
          try:
            return ('analysis_view_server', '{logs}/{log}'.format(logs=logs_path, log=dir_servers[int(user_input[1:])]), True)
          except:
            pass
      
      print('\nInvalid input\n\n')

    return (None, None, False)

  except:
    return (None, None, False)

def analysis_view_server(logs_path):
  
  print()

  dir_contents = listdir(logs_path)
  dir_server = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=logs_path, r_path=path)) and path.endswith('.log')
  , dir_contents))
  dir_databases = list(filter(
    lambda path: isdir('{logs}/{r_path}'.format(logs=logs_path, r_path=path))
  , dir_contents))
  del dir_contents

  try:
    
    path_server = '{logs}/{r_path}'.format(logs=logs_path, r_path=dir_server[0])
    del dir_server

    with open(path_server, 'r') as file_server:
      data_server = loads(file_server.read())
    del path_server

    print(
      '  Server {name}:\n'.format(name=data_server['server']) +
      '    {count} issues\n\n'.format(count=data_server['issues']['properties']) +
      '  Databases:'
    )

    for i in range(0, len(dir_databases)):
      print(
        '    ({i}) {database}'.format(i=str(i).center(5, ' '), database=dir_databases[i])
      )
    print('\n')

    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(O#) Open database by index   | (X) Back\n'
      )

      if user_input in ['X', 'x']:
        return (None, None, False)
      elif len(user_input) > 1:
        if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
          try:
            return ('analysis_view_database', '{logs}/{log}'.format(logs=logs_path, log=dir_databases[int(user_input[1:])]), True)
          except:
            pass

      print('\nInvalid input\n\n')
      
    return (None, None, False)
  
  except:
    return (None, None, False)

def analysis_view_database(logs_path):
  pass

def analysis_view_collection(logs_path):
  pass

def analysis_view_collection_detailed(logs_path):
  pass
