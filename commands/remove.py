import sqlite3
from config.env import DATABASE
from lib.util import fatal, confirm, success
from cli_app import Command

class Remove(Command):
    """Remove a task"""

    @staticmethod
    def register_arguments(parser):
        """
        This define the app remove command arguments
        :param parser: The app parser
        :returns: void
        """
        parser.add_argument('-rb', '--removeby', required=False, help='Remove by custom date (description|fulldescription|completed)')
        parser.add_argument('-v', '--value', required=True, help='Task to remove, this is the posible value of removeby filter')

    def check_removeby_type(self):
        """
        Check if the removeby flag is description|fulldescription|completed
        :param self: self instance
        :returns: OK?
        """
        if self.app.args.removeby != 'description' and self.app.args.removeby != 'fulldescription' and self.app.args.removeby != 'completed':
            return False
        else:
            return True

    def check_correct_removeby_filter(self):
        """
        Check if the value of removeby filter is correct
        :returns: Are OK?
        """
        if self.app.args.removeby == 'completed':
            if self.app.args.value != 'True' and self.app.args.value != 'False':
                fatal([
                    'Invalid flag "value" for flag "removeby"',
                    'The flag "value" must be True|False to removeby',
                    'because the removeby flag is completed',
                    'Use instead:',
                    '$ tasks-app remove --removeby=completed --value=True|False',
                ])

        return True

    def check_removeby(self):
        """
        Check if to removeby filter
        :param self: self instance
        :returns: Is to remove by filter
        """
        if not self.app.args.removeby is None:
            ok = self.check_removeby_type()

            if not ok is True:
                fatal([
                    'Invalid flag "removeby"',
                    'The available types for these flag are',
                    'description|fulldescription|completed',
                    'Use instead:',
                    '$ tasks-app remove --removeby=description|fulldescription|completed --value={}'.format(self.app.args.value),
                ])
            
            return True
        else:
            return False

    @staticmethod
    def get_search_sql(filter, value):
        """
        Calc the sql with flags
        :param filter: the filter to search
        :param value: the value of filter
        :returns: the calqued sql string
        """

        if filter == 'completed':
            if value == 'False':
                value = 0
            else:
                value = 1

            sql = 'SELECT * FROM Tasks WHERE {} LIKE {}'.format(filter, value)
        else:
            sql = 'SELECT * FROM Tasks WHERE {} LIKE "{}%"'.format(filter, value)

        return sql

    @staticmethod
    def get_delete_sql(filter, value):
        """
        Get the sql to delete a task with filter
        :param filter: the filter
        :param value: the value
        :returns: the calqued sql string
        """
        if filter == 'completed':
            if value == 'False':
                value = 0
            else:
                value = 1

            sql = 'DELETE FROM Tasks WHERE {} LIKE {}'.format(filter, value)
        else:
            sql = 'DELETE FROM Tasks WHERE {} LIKE "{}%"'.format(filter, value)

        return sql

    def get_task(self, filter, value):
        """
        Get a task like value
        :param filter: the filter to search
        :param value: the value to search
        :returns: Task found
        """
        conn = sqlite3.connect(DATABASE['file'])
        cur = conn.cursor()
        sql = self.get_search_sql(filter, value)
        cur.execute(sql)
        task = list()

        if len(list(cur)) > 0:
            cur.execute(sql)
            for description, fulldescription, completed in cur:
                task.append((description, fulldescription, completed,))

        conn.close()
        return task

    def check_if_tasks_exists(self, filter, value):
        """
        Check if exists a task with value and filter
        :param filter: the filter to search
        :param value: the value of filter
        :returns: Exists?
        """
        conn = sqlite3.connect(DATABASE['file'])
        cur = conn.cursor()
        sql = self.get_search_sql(filter, value)

        cur.execute(sql)

        if len(list(cur)) == 0:
            exists = False
        else:
            exists = True

        conn.close()
        return exists

    def remove_task(self, filter, value):
        """
        Remove a task with filter
        :param filter: the filter
        :param value: the value
        :returns: OK?
        """
        conn = sqlite3.connect(DATABASE['file'])
        cur = conn.cursor()
        cur.execute(self.get_delete_sql(filter, value))
        conn.commit()
        conn.close()
        return True

    def removeby_completed_filter(self):
        """
        Remove all tasks with the completed status
        :param self: self instance
        :returns: void
        """
        if self.app.args.value == 'True':
            value = 1
        else:
            value = 0

        # Getting all task with completed status
        conn = sqlite3.connect(DATABASE['file'])
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tasks WHERE completed = {}'.format(value))
        tasks = list(cur)
        conn.close()

        # Checking the task len
        if len(tasks) == 0:
            fatal(['No tasks found with completed = {}'.format(self.app.args.value)])

        # Showing selected tasks
        print('Selected tasks:')

        for description, fulldescription, completed in tasks:
            if completed == 0:
                completed = 'Incompleted'
            else:
                completed = 'Completed'

            print('  > {} - {} ({})'.format(description, fulldescription, completed))

        print('NOTE: because the value {} i want selected the before list'.format(self.app.args.value))
        print('Do you want to continue?')
        cont = confirm('Remove?')

        if cont is True:
            for task in tasks:
                description = task[0] # Task description
                ok = self.remove_task('description', description)
                if ok is True:
                    success(['Removed {}'.format(description)])

    def removeby_another_filter(self):
        """
        Remove by another filter if not it is "completed"
        :param self: self instance
        :returns: void
        """
        exists = self.check_if_tasks_exists(self.app.args.removeby, self.app.args.value)

        if exists is False:
            fatal([
                'Invalid flag "value"',
                'The task with "{}" "{}" not found'.format(self.app.args.removeby, self.app.args.value),
                'To show the tasks use instead',
                '$ tasks-app show',
            ])

        (task,) = self.get_task(self.app.args.removeby, self.app.args.value)
        # Getting task data, struct = (description, fulldescription, completed (0 False, 1 True),)
        description = task[0]
        fulldescription = task[1]
        completed = task[2]

        if completed == 0:
            completed = 'Incompleted'
        else:
            completed = 'Completed'

        print('Selecting the task with description = "{}"'.format(description))
        print('NOTE: Your value "{}" of filter "{}" like with description "{}"'.format(self.app.args.value, self.app.args.removeby, description))
        print('NOTE: The complete task is:')
        print('NOTE: {} - {} ({})'.format(description, fulldescription, completed))
        print('Do you want to continue?')
        cont = confirm('Remove?')

        if cont is True:
            ok = self.remove_task(self.app.args.removeby, self.app.args.value)
            if ok is True:
                success([
                    'The task with {} description'.format(description),
                    'was deleted successfully',
                    'to verify these use instead:',
                    '$ tasks-app show --filter=description --value={}'.format(description),
                    'if the output is none results all are ok!',
                ])

    def remove_with_filter(self):
        """
        Remove a task with filter
        :param self: self instance
        :returns: void
        """
        # Checking if the filter removeby is completed
        if self.app.args.removeby == 'completed':
            self.removeby_completed_filter()
        else:
            self.removeby_another_filter()

    def remove_without_filter(self):
        """
        Remove a task without filter. default filter is: "description"
        :param self: self instance
        :returns: void
        """
        exists = self.check_if_tasks_exists('description', self.app.args.value)

        if exists is False:
            fatal([
                'Invalid flag "value"',
                'The task with "description" "{}" not found'.format(self.app.args.value),
                'To show the tasks use instead:',
                '$ tasks-app show',
            ])

        (task,) = self.get_task('description', self.app.args.value)
        description = task[0] # The task description, struct is: (description, fulldescription, completed,)

        print('Selecting the task with description = "{}"'.format(description))
        print('NOTE: Your value "{}" like with "{}"'.format(self.app.args.value, description))
        print('Do you want to continue?')
        cont = confirm('Remove?')

        if cont is True:
            ok = self.remove_task('description', self.app.args.value)
            if ok is True:
                success([
                    'The task with {} description'.format(description),
                    'was deleted successfully',
                    'to verify these use instead:',
                    '$ tasks-app show --filter=description --value={}'.format(description),
                    'if the output is none results all are ok!'
                ])

    def run(self):
        """
        Main function
        :param self: self instance
        :returns: void
        """
        remove_by_filter = self.check_removeby()

        if remove_by_filter is True:
            correct_removeby_filter = self.check_correct_removeby_filter()
            if correct_removeby_filter is True:
                self.remove_with_filter()
        else:
            self.remove_without_filter()
