// Serials Solutions Data Management page > Show All
// https://clientcenter.serialssolutions.com/CC/Library/DataManagement/Default.aspx?LibraryCode=CC9&ShowAll=1
const map = {
    "Art and Architecture Source": "Digital/Electronic Serials",
    "ARTstor": "Digital/Electronic Media",
    "Avery Index to Architectural Periodicals": "Digital/Electronic Serials",
    "Bloomsbury Design Library Core Collection": "Digital/Electronic Books",
    "Bloomsbury(Taylor & Francis):Full Collection:2015": "Digital/Electronic Serials",
    "California College of the Arts Libguides": "(ignored)",
    "California College of the Arts Library Catalog": "(ignored)",
    "CCA Library Catalog": "(ignored)",
    "CCA Print Holdings": "(ignored)",
    "Design & Applied Arts Index (DAAI)": "Digital/Electronic Serials",
    "Duke University Press": "Digital/Electronic Serials",
    "Encyclopedia Britannica Academic Edition": "Digital/Electronic Serials",
    "Gale Literature Resource Center": "Digital/Electronic Serials",
    "GreenFILE": "Digital/Electronic Serials",
    "JSTOR Archive Collection A-Z Listing": "Digital/Electronic Serials",
    "JSTOR Arts & Sciences III": "Digital/Electronic Serials",
    "Kanopy PDA - USA": "Digital/Electronic Media",
    "Library, Information Science & Technology Abstracts (LISTA)": "Digital/Electronic Serials",
    "Material ConneXion": "Digital/Electronic Media",
    "MIT Press Journals": "Digital/Electronic Serials",
    "MITPressDirect 2005 Archival Collection": "Digital/Electronic Books",
    "MITPressDirect 2006 to 2010 Archival Collection": "Digital/Electronic Books",
    "MITPressDirect 2011 to 2015 Archival Collection": "Digital/Electronic Books",
    "MITPressDirect 2016 Collection": "Digital/Electronic Books",
    "MITPressDirect 2017 Collection": "Digital/Electronic Books",
    "MITPressDirect 2018 Collection": "Digital/Electronic Books",
    "MITPressDirect 2019 Collection": "Digital/Electronic Books",
    "MITPressDirect 2020 Collection": "Digital/Electronic Books",
    "Newspaper Source": "Digital/Electronic Serials",
    "Oxford Art Online": "Digital/Electronic Books",
    "Oxford English Dictionary": "Digital/Electronic Books",
    "Research Library": "Digital/Electronic Serials",
    "Single Journals": "Digital/Electronic Serials",
    // the two titles we have from Springer are just OA books
    // "Springer Books": "Digital/Electronic Books",
    "Taylor & Francis Current Content Access": "Digital/Electronic Serials",
    "Underground and Independent Comics, Comix, and Graphic Novels: Volume 1": "Digital/Electronic Books",
    "University of California Press Journals": "Digital/Electronic Serials",
    "University of Chicago Press Journals (Current access)": "Digital/Electronic Serials",
    "VAULT": "(ignored)"
}

let sum = { "Databases": 0, "Open Access": 0}
// build the other categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = 0
}

$('#ctl00__lvph_DatabaseListGrid tr').each((idx, row) => {
    let tds = $(row).find('td')
    if (!$(row).hasClass('GridViewHeader')) {
        let name = tds.eq(1).text().trim()
        let quantity = parseInt(tds.eq(6).text().replace(/ of \d+/,''))
        if (map.hasOwnProperty(name)) {
            sum[map[name]] += quantity
            // track total of databases without including a) ebook collections
            // & b) single journals under publishers like Duke U Press
            if (!map[name].match('Books') && !tds.eq(6).text().match(/ of /)) sum.Databases++
        } else {
            console.log(`Assuming "${name}" is OA`)
            sum["Open Access"] += quantity
        }
    }
})

let out = 'Type\tNumber of Titles\n'
for (let key in sum) {
    if (key !== 'undefined') out += `${key}\t${sum[key]}\n`
}
console.log(out)
