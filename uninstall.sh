#!/bin/bash

route=`dirname $0`

error() {
  echo "Fatal: $1"
  exit 1
}

confirm() {
  control="Y/n: "

  if test "$2" -eq 1; then
    control="y/N: "
  fi

  printf "$1 $control"
  read res

  while [[ $res != 'y' && $res != 'Y' && $res != 'n' && $res != 'N' && $res != '' ]]; do
    printf "Invalid response $control"
    read res
  done

  if [[ $res == 'y' || $res == 'Y' ]]; then
    return 0
  elif [[ $res == 'n' || $res == 'N' ]]; then
    return 1
  else
    return $2
  fi
}

print_final_log() {
  echo "Info:"
  echo "  > Tasks app was uninstalled successfully"
  echo "  > If you resigned use:"
  echo "  > $route/install.sh"
  echo "  > Please delete the alias added in your BASHrc"
}

tasks_app="/opt/tasks-app/tasks-app"

if ! test -f "$tasks_app"; then
  error "Tasks app was not found in your machine"
fi

# Uninstalling...

echo "Info: "
echo "  > This script is to remove tasks app of your machine"
echo "  > Use instead:"
echo "  > $ $route/install.sh"
echo "  > you must to reinstall"
confirm "Do you want to uninstall tasks-app?" 1

case $? in
  0)
    sudo rm "/usr/bin/tasks-app"
    sudo rm -rf "/opt/tasks-app"
    print_final_log
  ;;
esac
