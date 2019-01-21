from .. import Collection

def collection_new(database):

  print ()

  # Name
  #
  user_input_valid = False
  while not user_input_valid:
    name_input = input(
      'Collection name: '
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

  new_collection = (Collection(name=name, address=address))
  database.add_collections([new_collection])
  
  return ('collection_view', new_collection, False)

def collection_view(collection):

  print()

  # Show collection data
  #
  print(
    '\n  Collection {name}\n  On: {address}\n'.format(name=collection.name, address=collection.address)
  )

  # Show properties
  #
  print(
    '  Properties:\n'
  )
  for i in range(0, len(collection.properties)):

    if collection.properties[i].optional:
      optional = '*'
    else:
      optional = ''

    if collection.properties[i].type == 'ObjectProperty':
      type_string = 'Object'
    elif collection.properties[i].type == 'ControlledObjectProperty':
      type_string = 'Controlled Object'
    elif collection.properties[i].type == 'ArrayProperty':
      type_string = '<{elt_type}>'.format(elt_type=collection.properties[i].property_type)
    else:
      type_string = collection.properties[i].type

    print(
      '    ({i}) {name} ({type}){optional}'.format(i=str(i).center(5, ' '), name=collection.properties[i].name, type=type_string, optional=optional)
    )
  if len(collection.properties) == 0:
    print(
      '    No properties in collection'
    )
  print('\n')

  # User
  #
  user_input_valid = False
  while not user_input_valid:
    user_input = input(
      '(N) New property   | (O#) Open property by index   | (X) Back\n'
    )
    if user_input in ['N', 'n']:
      user_input_valid = True
      return ('property_new', collection, True)
    elif user_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('property_view', collection.properties[int(user_input[1:])], True)
        except:
          pass

    print('\nInvalid input\n\n')
