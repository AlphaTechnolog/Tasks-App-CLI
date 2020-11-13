# Tasks App CLI

This is an app to manage your tasks with command line interface (CLI).

## Instalation

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
