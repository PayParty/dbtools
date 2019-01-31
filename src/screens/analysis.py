from os import listdir
from os.path import isfile
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
        '({i}) {log_name}'.format(i=str(i).center(5, ' '), log_name=logs[i])
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
            return ('analysis_view_environment', '{logs}/{log}'.format(logs=logs_path, log=logs[int(user_input[1:])]), False)
          except:
            pass
      
      print('\nInvalid input\n\n')

  except:
    return (None, None, False)

def analysis_view_environment(logs_path):
  
  print()

  print(logs_path)

  return (None, None, False)

def analysis_view_server(logs_path):
  pass

def analysis_view_database(logs_path):
  pass

def analysis_view_collection(logs_path):
  pass

def analysis_view_collection_detailed(logs_path):
  pass
