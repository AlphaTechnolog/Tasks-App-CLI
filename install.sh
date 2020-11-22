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

/usr/bin/env python3 -c "
def confirm():
  response = input('Do you want to create an alias to more easy use without \`sudo\` (recomended) Y/n: ')

  while response != '' and response != 'y' and response != 'Y' and response != 'n' and response != 'N':
    response = input('Invalid response Y/n: ')

  if response == '':
    return True
  elif response == 'y' or response == 'Y':
    return True
  else:
    return False

confirmation = confirm()

if confirmation is True:
  exit(1)
else:
  exit(0)
"

case $? in
  1)
    if [[ $SHELL == `which bash` ]]; then
      echo 'alias tasks-app=sudo\ tasks-app' >> "$HOME/.bashrc"
    elif [[ $SHELL == `which zsh` ]]; then
      echo 'alias tasks-app=sudo\ tasks-app' >> "$HOME/.zshrc"
    else
      echo "Please add it to your BASHrc"
      echo 'alias tasks-app=sudo\ tasks-app >> "$HOME/BASHrc"'
    fi
  ;;
esac
