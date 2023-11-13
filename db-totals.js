// Serials Solutions Data Management page > Show All
// https://clientcenter.serialssolutions.com/CC/Library/DataManagement/Default.aspx?LibraryCode=CC9&ShowAll=1
const map = {
    "Art & Architecture Source": "Digital/Electronic Serials",
    "ARTbibliographies Modern": "Digital/Electronic Serials",
    "ARTstor": "Digital/Electronic Media",
    "Avery Index to Architectural Periodicals": "Digital/Electronic Serials",
    "Bloomsbury Design Library Core Collection": "Digital/Electronic Books",
    "Bloomsbury.*Full Collection\:2015": "Digital/Electronic Serials",
    "California College of the Arts Libguides": "(ignored)",
    "California College of the Arts Library Catalog": "(ignored)",
    "CCA Library Catalog": "(ignored)",
    "CCA Print Holdings": "(ignored)",
    "Design & Applied Arts Index": "Digital/Electronic Serials",
    "Duke University Press": "Digital/Electronic Serials",
    "Ebook Central - Business Ebook Subscription": "Digital/Electronic Books",
    "e-Duke Books Scholarly Collection .*": "Digital/Electronic Books",
    "Encyclopedia Britannica Academic Edition": "Digital/Electronic Serials",
    "Gale Literature Resource Center": "Digital/Electronic Serials",
    "GreenFILE": "Digital/Electronic Serials",
    "JSTOR Archive Collection A-Z Listing": "Digital/Electronic Serials",
    "JSTOR Arts & Sciences III": "Digital/Electronic Serials",
    "Kanopy PDA - USA": "Digital/Electronic Media",
    "Library, Information Science & Technology Abstracts": "Digital/Electronic Serials",
    "Material ConneXion": "Digital/Electronic Media",
    "MIT Press Journals": "Digital/Electronic Serials",
    "MIT Press Direct .* Collection": "Digital/Electronic Books",
    "MITPressDirect .* Collection": "Digital/Electronic Books",
    "Newspaper Source": "Digital/Electronic Serials",
    "Oxford Art Online": "Digital/Electronic Books",
    "Oxford Clinical Psychology All Titles": "Digital/Electronic Books",
    "Oxford English Dictionary": "Digital/Electronic Books",
    "Oxford Reference Library": "Digital/Electronic Books",
    "ProQuest One Business": "(ignored)",   // see logged note at the end
    "^Research Library$": "Digital/Electronic Serials", // need ^$ otherwise this matches "Open Research Library (Open Access)" too
    "Single Journals": "Digital/Electronic Serials",
    // the two titles we have from Springer are just OA books
    // "Springer Books": "Digital/Electronic Books",
    "Taylor & Francis Current Content Access": "Digital/Electronic Serials",
    "Underground and Independent Comics, Comix, and Graphic Novels: Volume 1": "Digital/Electronic Books",
    "University of California Press Journals": "Digital/Electronic Serials",
    "University of Chicago Press Journals": "Digital/Electronic Serials",
    "VAULT": "(ignored)",
    "Wiley Online Library All Journals": "Digital/Electronic Serials"
}

let sum = { "Databases": 0, "Open Access": 0}
// build the other categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = 0
}

let keys = Object.keys(map)
let patterns = keys.map(key => new RegExp(key))
const ofregex = / of \d+/
function addDBtoTotal(name, titles) {
    let matched = false
    for (let i = 0; i < keys.length; i++) {
        if (name.match(patterns[i])) {
            matched = true
            if (!titles.match(ofregex)) sum["Databases"]++ // don't count 1 title out of many as a full db
            let type = map[keys[i]]
            console.log(`${name} is categorized as "${type}"`)
            console.log('count', parseInt(titles.replace(ofregex, '')))
            sum[type] += parseInt(titles.replace(ofregex, ''))
            break
        }
    }
    if (!matched) {
        console.log(`Assuming ${name} is OA`)
        sum["Open Access"] += parseInt(titles.replace(/ of \d+/, ''))
    }
}

$('#ctl00__lvph_DatabaseListGrid tr').each((idx, row) => {
    let tds = $(row).find('td')
    if (!$(row).hasClass('GridViewHeader')) {
        let name = tds.eq(1).text().trim()
        let titles = tds.eq(6).text().trim()
        addDBtoTotal(name, titles)
    }
})

let out = 'Type\tNumber of Titles\n'
Object.keys(sum).forEach(key => {
    if (key) out += `${key}\t${sum[key]}\n`
})
console.log(out)
copy(out)
console.log("\n%c copied to your clipboard", "font-style: italic")
console.log("NOTES\n1. ProQuest One Business contains both ebooks and journals and so is not included in these totals. Visit the database detail page then add its titles to the above.\n2. Comics Plus is not included in the ebook totals here since records are loaded directly into Koha.")
