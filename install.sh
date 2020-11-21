#!/usr/bin/env bash

cd `dirname $0`
cd ../
sudo cp -r "./tasks-app" "/opt/tasks-app"
sudo chmod -R 777 "/opt/tasks-app/"
sudo ln -s "/opt/tasks-app/tasks-app" "/usr/bin/tasks-app"
cd $processed_pwd

/usr/bin/env python3 -c "
def success(msgs):
  if len(msgs) > 1:
    print('Info')
  else:
    print('Info: {}'.format(msgs[0]))

  if len(msgs) > 1:
    for msg in msgs:
      print('  > {}'.format(msg))

success([
  'Tasks app was installed successfully in your machine',
  'to test it use instead:',
  '$ tasks-app --help',
  'to get help!'
])
"
