# Libraries' Annual Statistics Helper Scripts

Some tools for summing data in our annual statistics reports. Basically, they do some of the tedious work of combining our administrative item types into types that are more understandable for others, which then lets us post informative tables of data onto [the Library Data page](https://libraries.cca.edu/about-us/about-us/library-data/).

The included JavaScript files all have to do with Koha reports and are meant to be run in your browser's JavaScript console; open it up with <kbd>CMD + Option + J</kbd> on a Mac using Chrome. Then copy-paste the code of the appropriate script into the console and hit <kbd>Return</kbd>. The output is usually copied to your keyboard in a tabular format but for some of the scripts it may be printed into the console, where you can manually transfer it to the appropriate spreadsheet.

## Teamwork Desk -> Reference Statistics

Rather than ask our Instructional Designer and their work study students to do double data entry in both Teamwork Desk, our ticketing system, and the Reference Statistics form, we convert exported Teamwork Desk tickets into a format consistent with our other data. Process:

- Visit Teamwork Desk at https://projects.cca.edu/desk/ then **Reports** > **Tickets**
- Set the date filter appropriately, e.g. the prior 12 months (assuming annual statistics)
- Use a (hopefully premade) filter to narrow down to tickets owned by the "Agents" on the instructional design team
- Click the anachronistic floppy disk icon to download the data as a CSV
- Run the python script included here to convert e.g. `./teamwork.py teamwork.csv`
- It'll output a file named "refstats.csv" which can be prepended to the "Data" tab of our Reference Statistics form responses spreadsheet (insert the Teamwork rows above the `ARRAYFORMULA()` rows that copy data from the "Form Responses" tab)

# LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
