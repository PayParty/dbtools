from os import listdir
from os.path import isfile, isdir
from json import loads

def analysis_success(log_return):

  print()

  # Show success message, path to logs output folder
  # and summary of found issues in environment
  #
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

  # Get paths of environment log file and server log directories
  #
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

    # Try to open environment log file
    #
    with open(path_environment, 'r') as file_environment:
      data_environment = loads(file_environment.read())
    del path_environment

    # Print environment summary
    #
    print(
      '  Environment {name}:\n'.format(name=data_environment['environment']) +
      '    {count} issues\n\n'.format(count=data_environment['issues']['properties']) +
      '  Servers:'
    )

    # Print servers
    #
    for i in range(0, len(dir_servers)):
      print(
        '    ({i}) {server}'.format(i=str(i).center(5, ' '), server=dir_servers[i])
      )
    print('\n')

    # User
    #
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
  
  # Same logic as analysis_view_environment, see above
  #
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
  
  print()

  dir_contents = listdir(logs_path)
  dir_database = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=logs_path, r_path=path)) and path.endswith('.log')
  , dir_contents))
  dir_collections = list(filter(
    lambda path: isdir('{logs}/{r_path}'.format(logs=logs_path, r_path=path))
  , dir_contents))
  del dir_contents

  try:
    
    path_database = '{logs}/{r_path}'.format(logs=logs_path, r_path=dir_database[0])
    del dir_database

    with open(path_database, 'r') as file_database:
      data_database = loads(file_database.read())
    del path_database

    print(
      '  Database {name}:\n'.format(name=data_database['database']) +
      '    {count} issues\n\n'.format(count=data_database['issues']['properties']) +
      '  Collections:'
    )

    for i in range(0, len(dir_collections)):
      print(
        '    ({i}) {collection}'.format(i=str(i).center(5, ' '), collection=dir_collections[i])
      )
    print('\n')

    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(O#) Open collection by index   | (X) Back\n'
      )

      if user_input in ['X', 'x']:
        return (None, None, False)
      elif len(user_input) > 1:
        if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
          try:
            return ('analysis_view_collection', '{logs}/{log}'.format(logs=logs_path, log=dir_collections[int(user_input[1:])]), True)
          except:
            pass

      print('\nInvalid input\n\n')
      
    return (None, None, False)
  
  except:
    return (None, None, False)

def analysis_view_collection(logs_path):
  
  print()

  dir_contents = listdir(logs_path)
  dir_collection = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=logs_path, r_path=path)) and path.endswith('.log')
  , dir_contents))
  del dir_contents

  try:

    path_collection = '{logs}/{r_path}'.format(logs=logs_path, r_path=dir_collection[0])
    del dir_collection

    with open(path_collection, 'r') as file_collection:
      data_collection = loads(file_collection.read())
    del path_collection

    print(
      '  Collection {collection}:\n'.format(collection=data_collection['collection']) +
      '    {count} issues\n'.format(count=data_collection['issues']['properties'])
    )

    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(D) Load detailed analysis   | (X) Back\n'
      )

      if user_input in ['X', 'x']:
        user_input_valid = True
        return (None, None, False)
      elif user_input in ['D', 'd']:
        user_input_valid = True
        return ('analysis_view_collection_detailed', logs_path, False)

      print('\nInvalid input\n\n')

    return (None, None, False)

  except:
    return (None, None, False)

def analysis_view_collection_detailed(logs_path):

  print ()

  # Get collection log
  #
  dir_contents = listdir(logs_path)
  dir_collection = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=logs_path, r_path=path)) and path.endswith('.log')
  , dir_contents))
  del dir_contents
  try:
    path_collection = '{logs}/{r_path}'.format(logs=logs_path, r_path=dir_collection[0])
    del dir_collection
    with open(path_collection, 'r') as file_collection:
      data_collection = loads(file_collection.read())
    del path_collection
  except:
    return (None, None, False)

  path_documents = '{logs}/Documents'.format(logs=logs_path)

  # Get paths of document logs
  #
  dir_contents = listdir(path_documents)
  dir_documents = list(filter(
    lambda path: isfile('{logs}/{r_path}'.format(logs=path_documents, r_path=path)) and path.endswith('.log')
  , dir_contents))
  del dir_contents

  try:
    
    # Initialize issues dict
    #
    issues = dict()

    # Iterate documents with json.loads and build issues dict
    # 
    for document in dir_documents:
      with open('{logs}/{document}'.format(logs=path_documents, document=document), 'r') as file_document:
        data_document = loads(file_document.read())
        for key in data_document.keys():
          if not data_document[key] == None:
            issues.setdefault(key, dict())
            issues[key].setdefault(data_document[key], 0)
            issues[key][data_document[key]] += 1

    # Re-print collection summary
    #
    print(
       '  Collection {collection}:\n'.format(collection=data_collection['collection']) +
       '    {count} issues\n\n'.format(count=data_collection['issues']['properties']) +
       '  Properties:'
    )

    # Print issues
    #
    for prop in issues.keys():
      print(
        '    {prop_name} ({count} issues):'.format(prop_name=prop, count=sum(issues[prop].values()))
      )
      for issue in issues[prop].keys():
        print(
          '    | {issue_text} ({count} occurences)'.format(issue_text=issue, count=issues[prop][issue])
        )
    print('\n')
    
    # User
    #
    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(X) Back\n'
      )
      if user_input in ['X', 'x']:
        user_input_valid = True
        return (None, None, False)
      
      print('\nInvalid input\n\n')

    return (None, None, False)

  except:
    return (None, None, False)
