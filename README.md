# bot-printer
This is a simple query bot that gives you the status of the printers upon request.

## How to use
This bot should run on a computer that is connected to the printers and have access to the printer. The bot will query the printers and return the status of the printers. The bot will run in the background and can be queried at any time.

Its suggested to create a single executable file that can be run on the computer. This can be done by creating an executable with pyinstaller. Then schedule the executable to run when the computer starts up.

### Create an executable
Using pyinstaller, create an executable file that can be run on the computer. This will create a single file that can be run on the computer. By running the following command, an executable will be created in the `dist` folder.

```pyinstaller BotStampante.spec```

The .spec file contains the configuration for the executable. It is included in the repository.

### Commands
- `/get` - Returns the status of the printers.

These below are typical examples of responses from the telegram bot

![image](https://github.com/user-attachments/assets/d1ae2292-2335-4f9a-bb35-b95c1a703be7)
![image](https://github.com/user-attachments/assets/9a8c8304-1695-4170-ac6d-d2a6ce7e6c17)


# Widget printer
This is a simple widget that displays the status of the printers. The widget will display the status of the printers and will update every 30 minutes.

## How to use
This widget should run on a computer that is connected to the printers and have access to the printer. The widget will show the printers and display the status of the printers. The widget will run in the background and can be queried at any time.


![image](https://github.com/user-attachments/assets/151d3d6d-fee0-4495-acef-7613ba567141)
