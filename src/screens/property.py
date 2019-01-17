from .. import Property, ObjectProperty, ControlledObjectProperty

def property_new(collection):

  print ()

  # Name
  #
  user_input_valid = False
  while not user_input_valid:
    name_input = input(
      'Property name: '
    )
    if isinstance(name_input, str) and len(name_input) > 0:
      user_input_valid = True
      name = name_input
      del name_input
    else:
      print(
        '\nInvalid name entered\n\n'
      )
  
  # Type
  #
  user_input_valid = False
  while not user_input_valid:
    type_input = input(
      'Select a property type:\n'+
      '(I) Object ID   | (S) String   | (N) Number   | (B) Boolean\n'+
      '(A) Any         | (O) Object   | (C) Controlled Object\n'
    )
    if type_input in ['O', 'o']:
      user_input_valid = True
      prop_type = 'ObjectProperty'
      del type_input
    elif type_input in ['C', 'c']:
      user_input_valid = True
      prop_type = 'ControlledObjectProperty'
      del type_input
    elif type_input in ['S', 's']:
      user_input_valid = True
      prop_type = 'String'
      del type_input
    elif type_input in ['B', 'b']:
      user_input_valid = True
      prop_type = 'Boolean'
      del type_input
    elif type_input in ['N', 'n']:
      user_input_valid = True
      prop_type = 'Number'
      del type_input
    elif type_input in ['I', 'i']:
      user_input_valid = True
      prop_type = 'ObjectID'
      del type_input
    elif type_input in ['A', 'a']:
      user_input_valid = True
      prop_type = 'Any'
      del type_input
    else:
      print(
        '\nInvalid property type selected\n\n'
      )
  
  # Optional
  #
  user_input_valid = False
  while not user_input_valid:
    optional_input = input(
      'Optional property? (Y/N): '
    )
    if optional_input in ['Y', 'y']:
      user_input_valid = True
      optional = True
      del optional_input
    elif optional_input in ['N', 'n']:
      user_input_valid = True
      optional = False
      del optional_input
    else:
      print(
        '\nInvalid option selected\n\n'
      )

  # ObjectProperty
  #
  if prop_type == 'ObjectProperty':
    new_property = ObjectProperty(name=name, optional=optional)

  # ControlledObjectProperty
  #
  elif prop_type == 'ControlledObjectProperty':

    # Controller name
    #
    user_input_valid = False
    while not user_input_valid:
      controller_input = input(
        'Controller property name: '
      )
      if isinstance(controller_input, str) and len(controller_input) > 0:
        user_input_valid = True
        controller = controller_input
        del controller_input
      else:
        print(
          '\nInvalid controller name entered\n\n'
        )
    
    new_property = ControlledObjectProperty(name=name, controller=Property(name=controller, type='Boolean'), optional=optional)
  
  # Other types
  #
  else:
    new_property = Property(name=name, type=prop_type, optional=optional)
  
  collection.add_properties([new_property])

  return (None, None, False)

def property_view(prop):
  
  # Delegate to specific function depending on property type
  #
  if prop.type == 'ObjectProperty':
    return property_view_object_property(prop)
  elif prop.type == 'ControlledObjectProperty':
    return property_view_controlled_object_property(prop)
  else:
    return property_view_property(prop)

def property_view_property(prop):
  
  print()

  # Show property data
  #
  if prop.optional:
    optional = 'Yes'
  else:
    optional = 'No'
  print(
    '\n  Property {name}\n  Type: {type}\n  Optional: {optional}\n'.format(name=prop.name, type=prop.type, optional=optional)
  )

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

def property_view_object_property(prop):
  
  print()

  # Show property data
  #
  if prop.optional:
    optional = 'Yes'
  else:
    optional = 'No'
  print(
    '\n  Property {name}\n  Type: {type}\n  Optional: {optional}\n'.format(name=prop.name, type=prop.type, optional=optional)
  )

  # Show properties
  #
  print(
    '  Properties:\n'
  )
  for i in range(0, len(prop.properties)):
    if prop.properties[i].optional:
      optional = '*'
    else:
      optional = ''
    print(
      '    ({i}) {name} ({type}){optional}'.format(i=str(i).center(5, ' '), name=prop.properties[i].name, type=prop.properties[i].type, optional=optional)
    )
  if len(prop.properties) == 0:
    print(
      '    No properties'
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
      return ('property_new', prop, True)
    elif user_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('property_view', prop.properties[int(user_input[1:])], True)
        except:
          pass
    
    print('\nInvalid input\n\n')

def property_view_controlled_object_property(prop):

  print()
  
  # Show property data
  #
  if prop.optional:
    optional = True
  else:
    optional = False
  print(
    '\n  Property {name}\n  Type: {type}\n  Optional: {optional}\n'.format(name=prop.name, type=prop.type, optional=optional)
  )

  # Show controller
  #
  print(
    '  Controller:\n\n    {name} ({type})\n'.format(name=prop.controller.name, type=prop.controller.type)
  )

  # Show properties
  #
  print(
    '  Properties:\n'
  )
  for i in range(0, len(prop.properties)):
    if prop.properties[i].optional:
      optional = '*'
    else:
      optional = ''
    print(
      '    ({i}) {name} ({type}){optional}'.format(i=str(i).center(5, ' '), name=prop.properties[i].name, type=prop.properties[i].type, optional=optional)
    )
  if len(prop.properties) == 0:
    print(
      '    No properties'
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
      return ('property_new', prop, True)
    elif user_input in ['X', 'x']:
      user_input_valid = True
      return (None, None, False)
    elif len(user_input) > 1:
      if user_input[0] in ['O', 'o'] and user_input[1:].isdigit():
        try:
          return ('property_view', prop.properties[int(user_input[1:])], True)
        except:
          pass

    print('\nInvalid input\n\n')
