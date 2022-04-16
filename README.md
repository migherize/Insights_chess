# ClickUper

Prototype a state machine to use the Format with Clickup microservice.

## Install

1. Clone the project.
2. ```docker network create kukun-net```
3. ```docker-compose up -d```
4. Ready to use

## Structure:

#### - Cron

Cron is a Scheduling utility that can schedule scripts to be executed regularly. 
Cron uses a specific syntax to define schedules. It consists of five fields, which are separated by blank spaces. The fields are:

```bash
Minute Hour Day Month Day_of_the_Week
```

The fields can have the following values:

```bash
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23) 
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
│ │ │ │ │                                       7 is also Sunday on some systems)
│ │ │ │ │
│ │ │ │ │
* * * * *  command to execute
```

Example to use: * * * * * ptyhon my_script_python.py

Every minute of every hour of every day of the month for every month for every day of the week.

#### - Output
For state machine the data is output to data/output into the container using environment variable
state_machine_OUTPUT_DATA.

    Output:
        - test.txt: compile time log.
        - maquina_estado.txt : registro de compilación maquina de estado. 


#### - Status ClickUp
Different states that can be handled in the ClickUp list.

1. TO DO: state initial for anything list.
2. STARTED: task startup
3. DONE-INVALID: task done with error.
4. DONE-VALID: task done successful.
5. INCOMPLETE: failed task with a status other than 200.
6. COMPLETED: task finished and ready to go to origin.

#### - Status Formatter

Different states that can be handled in the formatter microservice.

1. No: Initial state for any project to go through for formatter.
2. Running: Build status for any project in the formatter.
3. Stop: Finished status for any project in the formatter.

## To use:

State machine

```bash
$ docker exec -it state_machine_id /bin/sh
$ cd project
$ python maquina_estado.py
or (to use the cron)
$ vi root.py
add your setting cron
$ * * * * * ptyhon /code/project/maquina_estado.py
```
![Screenshot](state_machine_formater.png)
![alt text](automata.gif)
