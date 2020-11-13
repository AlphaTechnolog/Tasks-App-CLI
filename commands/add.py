import sqlite3
from cli_app import Command
from lib.util import success, fatal

class Add(Command):
    """Add a task"""

    @staticmethod
    def register_arguments(parser):
        parser.add_argument('-d', '--description', required=True, help='The task description')
        parser.add_argument('-f', '--fulldescription', required=True, help='The task fulldescription')

    def check_if_exists_task(self):
        """
        Check if exists a task by description
        :param self: self instance
        :returns: void
        """
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT description FROM Tasks WHERE description = "{}"'.format(self.app.args.description))
        tasks = list(cur)
        conn.close()

        if len(tasks) == 0:
            return False
        else:
            return True

    def add_task(self):
        """
        Add a task with user flags
        :param self: self instance
        :returns: void
        """
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute('INSERT INTO Tasks (description, fulldescription, completed) VALUES (?, ?, ?)', (self.app.args.description, self.app.args.fulldescription, 0,))
        conn.commit()
        conn.close()
        
        success([
            'Task added successfully',
            'To check these process',
            'Use instead:',
            '$ tasks-app show --filter=description --value="{}"'.format(self.app.args.description),
        ])

    def run(self):
        """Main method"""
        exists = self.check_if_exists_task()
        if exists is False:
            self.add_task()
        else:
            fatal([
                'Invalid flag "description"',
                'The task with description = "{}" exists'.format(self.app.args.description),
                'to show the available tasks',
                'Use instead:',
                '$ tasks-app show',
            ])
