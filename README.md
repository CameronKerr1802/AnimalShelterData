<h1>Dallas Animal Shelter Data</h1>

Dallas Animal Shelter Data is a project to showcase my skills in ETL and dashboards by taking data from 2014-2024 Dallas Animal Shelters adn showing which dog breeds are most likely to
be taken by a shelter as well as how often a dog will be euthanised or adopted.

Link to Dashboard: https://public.tableau.com/app/profile/cameron.kerr3517/viz/DallasDogShelter_2014-2024/Dashboard1#1

<h2>How It's Made:</h2>
Tech used: Python, Pandas Framework, PgAdmin4, SQL, Tableau

I began by obtaining the raw data in CSV format from Dallas Open Data's website. Once I had the data, I then wrote a script to rename the CSV files and column names to be more readable so that working with it and interpreting it was simpler. I wrote script out unnecessary data, and changed data types so that it would remain consistent, and merged duplicate column values. Finally, I created a script that used SQL to bring the cleaned data into pgAdmin, where I created the needed tables and filled them with the cleaned data, preparing the dataset for analysis.
