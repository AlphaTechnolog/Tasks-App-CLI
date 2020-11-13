import sqlite3
from lib.util import fatal
from cli_app import Command

class Show(Command):
    """Display your tasks"""

    @staticmethod
    def register_arguments(parser):
        parser.add_argument('-f', '--filter', type=str, required=False, help='Define the value of filter (description|fulldescription|completed)')
        parser.add_argument('-v', '--value', type=str, required=False, help='Define the value of filter flag')

    def validate_value_flag(self):
        """Check the value flag"""
        if not self.app.args.value is None or self.app.args.value == '':
            return True
        else:
            return False

    def is_to_filter(self):
        """Check if is to filter"""
        if not self.app.args.filter is None:
            # Check the flag value to evite problem in search process
            ok = self.validate_value_flag()

            if ok is False:
                fatal([
                    'Invalid value for "value" flag',
                    'The value flag is required to filter',
                    'Use instead:',
                    '$ tasks-app show --filter/-f={} --value/-v=VALUE'.format(self.app.args.filter),
                ])
            else:
                return True
        else:
            return False

    @staticmethod
    def fetchall():
        """This method fetch all tasks and show in terminal"""
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tasks')

        if len(list(cur)) > 0:
            print('Tasks found')

        cur.execute('SELECT * FROM Tasks')

        for description, fulldescription, completed in cur:
            if completed == 0:
                completed = 'Incompleted'
            else:
                completed = 'Completed'

            print('  > {} - {} ({})'.format(description, fulldescription, completed))

        cur.execute('SELECT * FROM Tasks')

        if len(list(cur)) == 0:
            print('No tasks found')

        conn.close()

    @staticmethod
    def validate_filterval(filterval):
        """
        Validate the filter val. Valid options description|fulldescription|completed
        :param filterval: The value to filter
        :returns: OK?
        """
        if filterval != 'description' and filterval != 'fulldescription' and filterval != 'completed':
            return False
        else:
            return True

    def filterby(self, filterval, valueoffilter):
        """
        Filter by a name
        :param filterval: The value to filter
        :param valueoffilter: The value of filter camp
        """
        if valueoffilter == '':
            fatal([
                'Invalid flag "value"',
                'value is required to flag "filter"'
            ])

        ok = self.validate_filterval(filterval)

        if ok is False:
            fatal([
                'Invalid flag "filter"',
                'The available filter values are:',
                'description (name)|fulldescription (description)|completed',
                'Use instead:',
                '$ tasks-app show --filter=description|fulldescription|completed --value={}'.format(valueoffilter)
            ])

        if filterval == 'completed':
            if valueoffilter != 'True' and valueoffilter != 'False':
                fatal([
                    'Invalid flag "value"',
                    'the available values for completed filter flag are:',
                    'True|False',
                    'Use instead:',
                    '$ tasks-app show --filter={filterval} --value=True|False',
                ])

        if filterval == 'completed':
            if valueoffilter == 'True':
                valueoffilter = 1
            elif valueoffilter == 'False':
                valueoffilter = 0

        if not filterval == 'completed':
            sql = 'SELECT * FROM Tasks WHERE {} LIKE "{}%"'.format(filterval, valueoffilter)
        else:
            sql = 'SELECT * FROM Tasks WHERE {} LIKE "{}"'.format(filterval, valueoffilter)

        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute(sql)

        if not len(list(cur)) == 0:
            print('Tasks found')

        cur.execute(sql)

        for description, fulldescription, completed in cur:
            if completed == 0:
                completed = 'Incompleted'
            else:
                completed = 'Completed'

            print('  > {} - {} ({})'.format(description, fulldescription, completed))

        cur.execute(sql)

        if len(list(cur)) == 0:
            print('No tasks found with search {}={}'.format(filterval, valueoffilter))

        conn.close()

    def run(self):
        to_filter = self.is_to_filter()

        if to_filter is True:
            self.filterby(self.app.args.filter, self.app.args.value)
        else:
            self.fetchall()
