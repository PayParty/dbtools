from .screens import screens

def app(args):
# CLI loop
#
  try:

    screen_stack = [('environment_select', None, False)]
    if len(args) > 1:
      screen_stack.append(('environment_select', args[1], False))

    while len(screen_stack) > 0:

      current_screen = screen_stack.pop()
      next_screen = screens[current_screen[0]](current_screen[1])
      if next_screen[2]:
        screen_stack.append(current_screen)
      if next_screen[0]:
        screen_stack.append(next_screen)
        print('\n\n')

    print('\n\n')
  
  except Exception as error:
    print('\n\n')
