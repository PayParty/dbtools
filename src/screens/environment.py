from .. import Environment
from json import loads, dumps

def environment_select(a=None):
  
  print (
    '\n\n\n  dbtool for MongoDB\n\n\n'
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

def environment_open(a=None):

  print()

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
      '(N) New server   | (O#) Open server by index   | (R) Run analysis\n'+
      '(S) Save environment                           | (Q) Close environment without saving\n'
    )
    if user_input in ['N', 'n']:
      user_input_valid = True
      return ('server_new', environment, True)
    elif user_input in ['S', 's']:
      user_input_valid = True
      return ('environment_save', environment, True)
    elif user_input in ['R', 'r']:
      user_input_valid = True
      environment.analyze()
      return (None, None, True)
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
