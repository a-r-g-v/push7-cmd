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

  push7 applications add --appno 'your_appno' --apikey 'your_apikey'
  push7 applications list 
  push7 applications use 'your_appno'
..

Usage
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh


  push7 < a.txt
  
  echo 'notification' | push7
  
  echo 'notification with given title' | push7 -t 'test push'

  a-time-consuming-command | push7
  
..

All Commands
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

  push7 applications list
  push7 applications delete
  push7 applications add
  push7 applications use
  push7
..

.. _push7.jp: https://push7.jp/

