from .. import Database

def database_new(server):

  print ()

  # Name
  #
  user_input_valid = False
  while not user_input_valid:
    name_input = input(
      'Database name: '
    )
    if isinstance(name_input, str) and len(name_input) > 0:
      user_input_valid = True
      name = name_input
      del name_input
    else:
      print(
        '\nInvalid name entered\n\n'
      )
  
  # Address
  #
  user_input_valid = False
  while not user_input_valid:
    address_input = input(
      'Address: '
    )
    if isinstance(address_input, str) and len(address_input) > 0:
      user_input_valid = True
      address = address_input
      del address_input
    else:
      print(
        '\nInvalid address entered\n\n'
      )

  new_database = (Database(name=name, address=address))
  server.add_databases([new_database])
  
  return ('database_view', new_database, False)

def database_view(database):

  print()

  # Show database data
  #
  print(
    '\n  Database {name}\n  On: {address}\n'.format(name=database.name, address=database.address)
  )

  # Show collections
  #
  print(
    '  Collections:\n'
  )
  for i in range(0, len(database.collections)):
    print(
      '    ({i}) {name}'.format(i=str(i).center(5, ' '), name=database.collections[i].name)
    )
  if len(database.collections) == 0:
    print(
      '    No collections in database'
    )
  print('\n')

  # User
  #
  user_input_valid = False
  while not user_input_valid:
    user_input = input(
      '(N) New collection   | (O#) Open collection by index   | (X) Back\n'
    )
    if user_input in ['N', 'n']:
      user_input_valid = True
      return ('collection_new', database, True)
    elif user_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('collection_view', database.collections[int(user_input[1:])], True)
        except:
          pass

    print('\nInvalid input\n\n')
