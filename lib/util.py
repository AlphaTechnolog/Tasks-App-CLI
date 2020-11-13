"""
Define the utils functions to more
easy develop!!!
"""

def fatal(msgs):
    """
    This function show a fatal error msg and exit
    This function validate the len of msgs and show
    various messages depending of length of msgs.
    """
    if len(msgs) > 1:
        print('Fatal')
    else:
        print('Fatal: {}'.format(msgs[0]))

    if len(msgs) > 1:
        for msg in msgs:
            print('  >', msg)

    exit(1)

def success(msgs):
    """
    This function show a advanced success msg
    This function validate the len of msgs and show
    various messages depending of length of msgs.
    """
    if len(msgs) > 1:
        print('Info')
    else:
        print('Info: {}'.format(msgs[0]))

    if len(msgs) > 1:
        for msg in msgs:
            print('  > {}'.format(msg))

def confirm(msg, default_val=True):
    """
    This function show a normal confirm to terminal
    This function realize the validations of default
    values and user response
    :param msg: The msg to show
    :param default_val (default True): The default value (in boolean format)
    :returns (True|False): The user response (in boolean format)
    """
    if default_val is True:
        ask = 'Y/n: '
    else:
        ask = 'y/N: '

    response = input('{} {}'.format(msg, ask))

    while response != '' and response != 'y' and response != 'n' and response != 'Y' and response != 'N':
        response = input('Invalid response. {} {}'.format(msg, ask))

    if response == '':
        return default_val
    elif response == 'y' or response == 'Y':
        return True
    else:
        return False
