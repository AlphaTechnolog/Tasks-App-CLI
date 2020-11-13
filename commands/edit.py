import sqlite3
from lib.util import fatal, success, confirm
from cli_app import Command

class Edit(Command):
    """Edit a task"""

    @staticmethod
    def register_arguments(parser):
        """
        Register an arguments of edit command
        :param parser: the parser
        :returns: void
        """
        parser.add_argument('-d', '--description', required=True, help='The task description')
        parser.add_argument('-nd', '--newdescription', required=True, help='The new task description')
        parser.add_argument('-nfd', '--newfulldescription', required=True, help='The new task fulldescription')
        parser.add_argument('-nc', '--newcompleted', required=True, help='The new task fulldescription')

    def validate_newcompleted(self):
        """
        This validate if the newcompleted arg is correctly
        :param self: self instance
        :returns: is valid?
        """
        if self.app.args.newcompleted != 'True' and self.app.args.newcompleted != 'False':
            return False
        else:
            return True

    def process_new_completed_arg(self):
        """
        This function process the new completed arg, if self.app.args.newcompleted == 'True' then return 1 else return 0
        :param self: self instance
        :returns: processed_task 1|0
        """
        if self.app.args.newcompleted == 'True':
            return 1
        else:
            return 0

    def check_if_exists_task(self):
        """
        This method check if exists a task with description = newdescription
        :param self: self instance
        :returns: exists?
        """
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT description FROM Tasks WHERE description = ?', (self.app.args.newdescription,))
        result = list(cur)
        conn.close()

        # Checking the result variable
        if len(result) == 0:
            return False
        else:
            return True

    def get_selected_task(self):
        """
        This method request the selected task sending the description attribute
        :param self: self instance
        :returns: The found task, if not found returns None
        """
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tasks WHERE description LIKE "{}%"'.format(self.app.args.description))
        task = list(cur)
        conn.close()

        if len(task) == 0:
            return None
        else:
            return task[0]

    def update(self):
        """
        This method update the task with new data
        :param self: self instance
        :returns: void
        """
        sql = 'UPDATE Tasks SET description = "{}", fulldescription = "{}", completed = {} WHERE description LIKE "{}%"'.format(self.app.args.newdescription, self.app.args.newfulldescription, self.app.args.newcompleted, self.app.args.description)
        conn = sqlite3.connect('db/tasksapp.sqlite3')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True

    def run(self):
        """
        Main method
        :param self: self instance
        :returns: void
        """
        ok = self.validate_newcompleted()

        if ok is False:
            fatal([
                'Invalid flag "newcompleted"',
                'the available values for newcompleted are True|False',
                'Use instead:',
                '$ tasks-app edit --description="{}" --newdescription="{}" --newfulldescription="{}" --newcompleted=True|False'.format(self.app.args.description, self.app.args.newdescription, self.app.args.newfulldescription)
            ])

        self.app.args.newcompleted = self.process_new_completed_arg()

        exists = self.check_if_exists_task()

        if exists is True:
            fatal([
                'The task with description "{}" was exists'.format(self.app.args.newdescription),
                'to get all tasks. Use instead:',
                '$ tasks-app show',
            ])

        selected_task = self.get_selected_task()

        if selected_task is None:
            fatal([
                'Invalid task to search with "description" LIKE "{}"'.format(self.app.args.description),
                'The task with description like to "{}" doesn\'t exists'.format(self.app.args.description),
                'To show all tasks use instead:',
                '$ tasks-app show',
            ])

        # Getting the selected task data, struct = (description, fulldescription, completed 0|1)
        description = selected_task[0]
        fulldescription = selected_task[1]
        completed = selected_task[2]

        if completed == 0:
            completed = 'Incompleted'
        else:
            completed = 'Completed'
        
        print('NOTE: Selected the task with description = "{}"'.format(description))
        print('NOTE: Your description "{}" like with description "{}"'.format(self.app.args.description, description))
        print('NOTE: The complete task format is:')
        print('NOTE: {} - {} ({})'.format(description, fulldescription, completed))
        print('Do you want to update to:')

        description = self.app.args.newdescription
        fulldescription = self.app.args.newfulldescription
        completed = self.app.args.newcompleted

        if completed == 0:
            completed = 'Incompleted'
        else:
            completed = 'Completed'

        print('{} - {} ({})'.format(description, fulldescription, completed))
        cont = confirm('Update?')

        if cont is True:
            ok = self.update()
            if ok is True:
                success([
                    'The task with description = "{}"'.format(selected_task[0]),
                    'was update successfully to verify these',
                    'Use instead:',
                    '$ tasks-app show --filter=description --value="{}"'.format(self.app.args.newdescription)
                ])
