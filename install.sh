#!/usr/bin/env bash

processed_pwd=$(/usr/bin/env python3 -c "
pwd='$PWD'
pwd = pwd.split('/')
pwd = pwd[-1]
print(pwd)
")

if [[ $processed_pwd != 'tasks-app' ]]; then
  /usr/bin/env python3 -c "
def fatal(msgs):
  if len(msgs) > 1:
    print('Fatal')
  else:
    print('Fatal {}'.format(msgs[0]))

  if len(msgs) > 1:
    for msg in msgs:
      print('  > {}'.format(msg))

  exit(1)

fatal([
  'Uncaught error',
  'Please execute the bash install.sh in the folder',
  'Use instead:',
  '$ cd /path/to/tasks-app',
  '$ cd ./install.sh',
  'if the folder is not called \"tasks-app\", please rename it'
])
  "
  exit 1
fi

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
