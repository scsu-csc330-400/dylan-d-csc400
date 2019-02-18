# Abstract
To provide teachers/researchers with a platform that takes data from students and generates graphs to find which study strategies have an impact on grades. This data will be used in a study at Yale and will allow teachers at collect and analyze this data quickly without having to do it by hand. This is a huge benefit, so teachers can focus on teaching without having to input and calculate the results by hand.

# Design
The system will be comprised of three main components. First, the system will require input from students in the form of a survey. The second part of the system is a persistent database to store all of the data collected from the surveys. The last component will be a web interface where teachers can upload de-identified grades, view and edit data for their classes and generate graphs for their classes.

# Back-end
Written in Python and using the Flask Framework and its libraries, the system takes input from a Google Form and stores it in an SQL database running on a VM in Google Cloud. The app uses matpltlib for generating graphs, openpyxl to read grades from an Excal file.

# Getting Started
Review all pages in the Wiki before you start using this app.
<p>Currently, the ip address for this project is http://104.154.246.246/</p>
The Google Form used by students to input data is <p>https://drive.google.com/open?id=1nfRt2jut6acoOiAWyJH1szMopT8RQlPAHTgLgkVcDFM</p>
