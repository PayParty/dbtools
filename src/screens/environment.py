from .. import Environment
from json import loads, dumps

def environment_select(args=None):

  if args:
    environment = environment_open(args)
    return ('environment_view', environment, False)
  
  print (
    '\n\n\n  dbtools for MongoDB\n\n\n'
  )
  user_input_valid = False
  while not user_input_valid:
    environment_input = input(
      '(N) Create new environment   | (O) Open environment from file   | (X) Exit\n'
    )

    if environment_input in ['N', 'n']:
      user_input_valid = True
      environment = environment_create()
      if environment:
        return ('environment_view', environment, True)

    elif environment_input in ['O', 'o']:
      user_input_valid = True
      environment = environment_open()
      if environment:
        return ('environment_view', environment, True)

    elif environment_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)

    print('\nInvalid option selected.\n\n')

def environment_create(a=None):

  print()

  # Name
  #
  user_input_valid = False
  while not user_input_valid:
    name_input = input(
      'Environment name: '
    )
    if isinstance(name_input, str) and len(name_input) > 0:
      user_input_valid = True
      name = name_input
      del name_input
    else:
      print(
        '\nInvalid name entered\n\n'
      )
  
  # Filepath
  #
  user_input_valid = False
  while not user_input_valid:
    filepath_input = input(
      'File name: '
    )
    if isinstance(filepath_input, str) and len(filepath_input) > 0:
      user_input_valid = True
      filepath = '{input}.dbconf'.format(input=filepath_input)
      del filepath_input
    else:
      print(
        '\nInvalid file name entered\n\n'
      )

  return Environment(name=name, filepath=filepath)

def environment_open(args=None):

  print()

  if args:
    try:
      file_input = open(args, 'r')
      file_contents = file_input.read()
      file_input.close()
      return Environment(from_plain=loads(file_contents))
    except:
      raise Exception()

  # Get filepath
  #
  user_input_valid = False
  while not user_input_valid:
    filepath_input = input(
      'File name (relative): '
    )
    if isinstance(filepath_input, str) and len(filepath_input) > 0:
      if not filepath_input.endswith('.dbconf'):
        filepath_input += '.dbconf'
      try:
        file_input = open(filepath_input, 'r')
        file_contents = file_input.read()
        file_input.close()
        user_input_valid = True
      except:
        print(
          '\nFile not found.\n\n'
        )
    elif isinstance(filepath_input, str) and len(filepath_input) == 0:
      return None

  return Environment(from_plain=loads(file_contents))

def environment_view(environment):

  print()

  # Show environment data
  #
  print(
    '\n  Environment {name}\n  On file: {filepath}\n'.format(name=environment.name, filepath=environment.filepath)
  )

  # Show servers
  #
  print(
    '  Servers:\n'
  )
  for i in range(0, len(environment.servers)):
    print(
      '    ({i}) {name}'.format(i=str(i).center(5, ' '), name=environment.servers[i].name)
    )
  if len(environment.servers) == 0:
    print(
      '    No servers in environment'
    )
  print('\n')
  
  # User
  #
  user_input_valid = False
  while not user_input_valid:
    user_input = input(
      '(N) New server         | (O#) Open server by index   | (R) Run analysis\n'+
      '(S) Save environment   | (Q) Close environment without saving\n'
    )
    if user_input in ['N', 'n']:
      user_input_valid = True
      return ('server_new', environment, True)
    elif user_input in ['S', 's']:
      user_input_valid = True
      return ('environment_save', environment, True)
    elif user_input in ['R', 'r']:
      user_input_valid = True
      return ('environment_analyze', environment, True)
    elif user_input in ['Q', 'q']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('server_view', environment.servers[int(user_input[1:])], True)
        except:
          pass

    print('\nInvalid input\n\n')

def environment_save(environment):

  print()

  # Inform
  #
  print(
    '\nSaving environment {name} to {filepath}\n'.format(name=environment.name, filepath=environment.filepath)
  )
  try:
    file_out = open(environment.filepath, 'w')
    file_out.write(dumps(environment.to_plain()))
    file_out.close()
    print(
      '\nSaved\n\n'
    )
    return (None, None, False)
  except:
    print(environment.to_plain())
    print(
      '\nCould not save file\n\n'
    )
    return (None, None, False)

def environment_analyze(environment):
# environment_analyze
#
# Allows the user to select analysis targets,
# calls the analysis, and returns the analysis
# viewer screen call

  print ()

  targets = environment.targets

  # Selection loop
  #
  user_done = False
  while not user_done:

    # Show current selection
    #
    print(
      '  Analysis\n\n  Current selection:\n'
    )
    for server in environment.servers:
      print(
        '    ({selected}) {name}'.format(selected='S' if server.name in list(targets.keys()) else ' ', name=server.name)
      )
      if len(server.databases) > 0:
        print('    | ')
      for database in server.databases:
        print(
          '    |-({selected}) {name}'.format(selected='S' if server.name in list(targets.keys()) and database.name in list(targets[server.name].keys()) else ' ', name=database.name)
        )
        for collection in database.collections:
          print(
            '    | |-({selected}) {name}'.format(selected='S' if server.name in list(targets.keys()) and database.name in list(targets[server.name].keys()) and collection.name in list(targets[server.name][database.name]) else ' ', name=collection.name)
          )
        print('    | ')
    print('\n')

    # User
    #
    user_input_valid = False
    while not user_input_valid:
      user_input = input(
        '(S path) Select element by path   | (D path) Deselect element by path\n'+
        '(R) Run analysis   | (X) Back     | (path: server[.database[.collection]])\n'+
        '\n'
      )
      if user_input in ['X', 'x']:
        user_input_valid = True
        user_done = True
        environment.targets = targets
        return (None, None, False)
      elif user_input in ['R', 'r'] and len(targets.keys()) > 0:
        user_input_valid = True
        user_done = True
        environment.targets = targets
        log_filepath = environment.analyze()
        return ('analysis_view', log_filepath, False)

      # Select
      #
      elif user_input.split(' ', 1)[0] in ['S', 's']:

        print('\n')

        try:
          path = user_input.split(' ', 1)[1].split('.')

          # Server
          #
          if len(path) > 0 and path[0]:
            found_server = list(filter(
              lambda server: server.name == path[0]
            , environment.servers)).pop()
            if targets.get(found_server.name, None) == None:
              targets[found_server.name] = {}
            if len(path) == 1:
              targets[found_server.name] = dict(map(
                lambda database: (database.name, list(map(lambda collection: collection.name, database.collections)))
              , found_server.databases))
            
            # Database
            #
            if len(path) > 1 and path[1]:
              found_database = list(filter(
                lambda database: database.name == path[1]
              , found_server.databases)).pop()
              if targets[found_server.name].get(found_database.name, None) == None:
                targets[found_server.name][found_database.name] = []
              if len(path) == 2:
                targets[found_server.name][found_database.name] = list(map(
                  lambda collection: collection.name
                , found_database.collections))

              # Collection
              #
              if len(path) > 2 and path[2]:
                found_collection = list(filter(
                  lambda collection: collection.name == path[2]
                , found_database.collections)).pop()
                if not path[2] in targets[found_server.name][found_database.name]:
                  targets[found_server.name][found_database.name].append(found_collection.name)
                  raise GeneratorExit('collection')
              
              else:
                raise GeneratorExit('database')
            else:
              raise GeneratorExit('server')
          else:
            raise GeneratorExit('none')

        except GeneratorExit as exit_value:

          if str(exit_value) == 'none':
            print('\nNothing selected\n\n')
          elif str(exit_value) == 'server':
            print('\nServer selected\n\n')
          elif str(exit_value) == 'database':
            print('\nDatabase selected\n\n')
          elif str(exit_value) == 'collection':
            print('\nCollection selected\n\n')
          
          user_input_valid = True
          continue

        except Exception as error:
          print('\nSyntax error. Selection may have occurred incorrectly\n\n')
          user_input_valid = True
          continue

      # Deselect
      #
      elif user_input.split(' ', 1)[0] in ['D', 'd']:

        print('\n')
        
        try:
          path = user_input.split(' ', 1)[1].split('.')

          if len(path) == 3:
            user_input_valid = True
            targets[path[0]][path[1]].remove(path[2])
            if targets[path[0]][path[1]] == []:
              del targets[path[0]][path[1]]
              if targets[path[0]] == {}:
                del targets[path[0]]
            continue
          elif len(path) == 2:
            user_input_valid = True
            del targets[path[0]][path[1]]
            if targets[path[0]] == {}:
              del targets[path[0]]
            continue
          elif len(path) == 1:
            user_input_valid = True
            del targets[path[0]]
            continue
          else:
            raise Exception()
        
        except Exception as error:
          print('\nSyntax error\n\n')
          user_input_valid = True
          continue

      print('\nInvalid input\n\n')
