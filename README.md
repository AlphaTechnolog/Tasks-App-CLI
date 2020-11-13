# Tasks App CLI

This is an app to manage your tasks with command line interface (CLI).

## Installation

Important!!! Rename the folder to "tasks-app"

### Automatic (Recomended)

Open your terminal (Ctrl+Alt+T) and execute these commands:

```sh
cd /path/to/tasks-app
./install.sh # To uninstall ./uninstall.sh
```

These script install the tasks app in your machine.

### Manual

Open your terminal (Ctrl+Alt+T) and execute these commands:

```sh
cd /path/to/tasks-app
cd ../
sudo cp -r ./tasks-app /opt/tasks-app
sudo chmod -R 777 /opt/tasks-app
sudo ln -s /opt/tasks-app/tasks-app /usr/bin/tasks-app
# To uninstall
sudo rm -rf /opt/tasks-app
sudo rm /usr/bin/tasks-app
```

## Usage

To show help use:

```sh
tasks-app --help # or
tasks-app -h
```

To show tasks use:

```sh
tasks-app show
# ...
```

To filter use:

```sh
tasks-app show --filter='description|fullname|completed' --value='{Value to search}' # or
tasks-app show -f='description|fullname|completed' -v='{Value to search}'
# ...
```

To add task

```sh
tasks-app add --description='description' --fulldescription='fulldescription' # or
tasks-app add -d='description' -f='fulldescription'
# ...
```

To remove task

```sh
tasks-app remove --value='Search value' # this is to remove by description, or
tasks-app remove -v='Search value' # to remove with filter use:
tasks-app remove --removeby='description|fulldescription|completed' --value='Search value' # or
tasks-app remove -rb='description|fulldescription|completed' -v='Search value'
# ...
```

To edit task

```sh
tasks-app edit --description='Description of task to edit' --newdescription='New description' --newfulldescription='New fulldescription' --newcompleted='True|False' # or
tasks-app edit -d='Description of task to edit' -nd='New description' -nfd='New fulldescription' -nc='True|False'
# ...
```
