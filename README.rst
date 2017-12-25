=========================================
 Push7-Cmd
=========================================

This command provides a push7 command.   
Using this command, you can send a push notification from your terminal to your browser using push7.jp_.


Installation
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

  pip install push7-cmd
..

Setup
~~~~~~~~~~~~~~~~~~~~~~
First, you should add a push7 application into push7-cmd.

.. code-block:: sh

  push7 applications add 'your_appno' 'your_apikey'
  push7 applications list 
  push7 applications use 'your_appno'
..

Usage
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

  # Send a push from stdin
  push7 < a.txt
  
  # Send a push from stdin
  echo 'notification' | push7

  a-time-consuming-command | push7
  
  # Send a push with given title
  echo 'notification with given title' | push7 -t 'test push'

  # Send a push without stdin
  push7 --title 'poe' --body 'poe'

  a-command-will-cause-output-like-a-flood | push7 --body 'finish the command'

  # Add new application
  push7 applications add 'your_appno' 'your_apikey'

  # List registed applications
  push7 applications list

  # Delete the application
  push7 applications delete 'your_appno'

  # Change default applicatios
  # Default applications means : An application which this command will use when you sent a push.
  push7 applications use 'your_appno'
  
  # Help
  push7 --help


..

All Commands
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

  push7 applications list
  push7 applications delete <appno>
  push7 applications add <appno> <apikey>
  push7 applications use <appno>
  push7 --title title --body body
..

.. _push7.jp: https://push7.jp/

