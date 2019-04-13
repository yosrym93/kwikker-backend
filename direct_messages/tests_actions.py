from . import actions
from database_manager import db_manager
import pytest
db_manager.initialize_connection('kwikker', 'postgres', '123456')
