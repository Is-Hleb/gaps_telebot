# gaps_telebot
<h2>To start</h2>
<p><b>python setup.py install <br> python main.py</b></p>
<h2>Commands</h2>
<p>
<ul>
<li>/admin - Allows you to enter the admin space<br>
    <p>Go to config to edit password, login and login command</p>
</li>

<br>
<li>/mark - Lets select and add absent<p>
    <b>Input format:</b><br>
    <b>h</b>(The number of hours that day) absent numbers - 1 2 3, <br> 
    if the reason for the absence is not valid, add * - 1*, 2*, 3*) <br>
    If the person missed a different collision of hours, dial <b>h(nums)</b> - 14*h8 15h2 <br>
    Example: <br>
    <b>h10 1 2 3 4h2 14*h8 20</b>
</p></li>
<li>/show_group - List the group as a message</li>
<li>/show_marked - Displays already marked</li>
<li>/remark - Differs from /mark in that it clears the base of gaps for the current date</li>
<li>/download - allows you to download a table with gaps in a specific month</li>
</ul>
</p>
<h2>Config.py</h2>
<p>Specify the token in the field of the same name.<br> In this file, you can edit the replicas to those or other commands</p>
<h2>Excel.py</h2>
<p>This file creates an exel file based on their database records</p>
<h2>PersonModel.py</h2>
<p>
File for working with the base. <br> The structure of the base is built on the concepts of a pass and a person, the file operates with the tables of the same name</p>
<h2>functions.py</h2>
<p>
The file contains two functions, one for sending a list with a message, the other for logging errors</p>
<h2>Main.py</h2>
<p>
The file describes the main logic of the application</p>
