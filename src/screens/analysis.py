def analysis_success(log_return):

  print()

  print(
    '\n  Analysis successful\n  Full logs saved in {log_path}\n  Issues found:'.format(log_path=log_return['path'])+
    '\n    {prop} properties in {coll} collections in {daba} databases in {serv} servers'.format(prop=log_return['issues']['properties'], coll=log_return['issues']['collections'], daba=log_return['issues']['databases'], serv=log_return['issues']['servers'])
  )

  return (None, None, False)
