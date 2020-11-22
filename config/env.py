"""Define the app envs."""

import sys
import os

class Service:
    """Validate os."""
    def getSystem(self):
        """System."""
        return os.name

    def getPlatform(self):
        """Platform."""
        return sys.platform

service = Service()

def get_database_data():
    if service.getPlatform() == 'win32' or service.getPlatform() == 'win64' and service.getSystem() == 'nt':
        return { 'file': 'C:\\ProgramData\\TasksAppCLI\\db\\tasksapp.sqlite3', 'dirname': 'C:\\ProgramData\\TasksAppCLI\\db' }
    elif service.getPlatform() == 'linux' and service.getSystem() == 'posix':
        return { 'file': '/opt/tasksapp/tasksapp.sqlite3', 'dirname': '/opt/tasksapp' }
    else:
        return { 'file': '/opt/tasksapp/tasksapp.sqlite3', 'dirname': '/opt/tasksapp' }

DATABASE = get_database_data()