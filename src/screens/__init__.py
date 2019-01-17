from .environment import *
from .server import *
from .database import *
from .collection import *
from .property import *

screens = {
  'environment_select': environment_select,
  'environment_view': environment_view,
  'environment_save': environment_save,

  'server_new': server_new,
  'server_view': server_view,

  'database_new': database_new,
  'database_view': database_view,

  'collection_new': collection_new,
  'collection_view':  collection_view,

  'property_new': property_new,
  'property_view': property_view
}