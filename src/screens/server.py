from .. import Server

def server_new(environment):

  print()

  # Name
  #
  user_input_valid = False
  while not user_input_valid:
    name_input = input(
      'Server name: '
    )
    if isinstance(name_input, str) and len(name_input) > 0:
      user_input_valid = True
      name = name_input
      del name_input
    else:
      print(
        '\nInvalid name entered\n\n'
      )
  
  # Connection string
  #
  user_input_valid = False
  while not user_input_valid:
    connection_string_input = input(
      'Connection string: '
    )
    if isinstance(connection_string_input, str) and len(connection_string_input) > 0:
      user_input_valid = True
      connection_string = connection_string_input
      del connection_string_input
    else:
      print(
        '\nInvalid connection string entered\n\n'
      )

  new_server = (Server(name=name, connection_string=connection_string))
  environment.add_servers([new_server])
  
  return (None, None, False)

def server_view(server):

  print()

  # Show server data
  #
  print(
    '\n  Server {name}\n  On: {connection_string}\n'.format(name=server.name, connection_string=server.connection_string)
  )

  # Show databases
  #
  print(
    '  Databases:\n'
  )
  for i in range(0, len(server.databases)):
    print(
      '    ({i}) {name}'.format(i=str(i).center(5, ' '), name=server.databases[i].name)
    )
  if len(server.databases) == 0:
    print(
      '    No databases in server'
    )
  print('\n')

  # User
  #
  user_input_valid = False
  while not user_input_valid:
    user_input = input(
      '(N) New database   | (O#) Open database by index   | (X) Back\n'
    )
    if user_input in ['N', 'n']:
      user_input_valid = True
      return ('database_new', server, True)
    elif user_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('database_view', server.databases[int(user_input[1:])], True)
        except:
          pass

    print('\nInvalid input\n\n')
