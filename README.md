# A JIRA exported csv to 12 month roadmap utility

Create a JIRA issue report containing the issues you care about, in my case these are Epics tagged with the label 'Roadmap'.

``project in (RR, ROT) AND resolution = Unresolved AND status != "Closed - DONE" AND status != "No Personal Data Changes" AND type = epic AND labels = Roadmap ORDER BY priority, summary DESC``

Export the report in CSV format to a file named \<Project code>Roadmap.csv

The project code has to be supplied on the command line followed by the current Quarter. 

    $ python jira-csv-roadmap.py PROJ Q4 > proj_2019_q4.html

The program assumes you have completed the Target Start Date and Target End Date for every epic. 
To use other fields you would need to change the code.

To get this to work you will need to modify the variable ``jira_url_prefix`` to match your JIRA installation.