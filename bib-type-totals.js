// Koha report: https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?reports=61&phase=Run%20this%20report&limit=50
const map = {
    '': 'Other',
    '2DAYRES': 'Reserves',
    '2HOURRES': 'Reserves',
    '3HOURRES': 'Reserves',
    'ARCHIVE': 'Archival Materials',
    'BK': 'Books',
    'BOOK': 'Books',
    'BOUNDPER': 'Periodicals',
    'DVD': 'Videos',
    'EBOOK': 'Digital/Electronic Books',
    'EQUIPMENT': 'Other',
    'LIBUSEBK': 'Books',
    'LIBUSEBOOK	': 'Books',
    'LIBUSEDVD': 'Videos',
    'LIBUSESUPP': 'Other',
    'LIBUSEVIDE': 'Videos',
    'MATSAMP': 'Material Samples',
    'MIXEDMEDIA': 'Other',
    'NEWPER': 'Periodicals',
    'REALIA': 'Other',
    'SUPPL': 'Other'
}
let sum = {}
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = 0
}
// loop over table & add each row to its matching sum entry
$('table tr').each((index, row) => {
    if ($(row).find('td').length === 2) {
        let type = $(row).find('td').first().text()
        let quantity = parseInt($(row).find('td').last().text())
        sum[map[type]] += quantity
    }
})
// sort categories alphabetically but put 'Other' at the end
let cats = Object.keys(sum).sort()
cats.splice(cats.indexOf('Other'), 1)
cats.push('Other')

// printy/copy to clipboad in a nicer format
let out = 'Type\tNumber of Titles\n'
cats.forEach(c => if (c !== 'undefined') out += `${c}\t${sum[c]}\n`)

console.log(out)
console.log("\n%c copied to your clipboard", "font-style: italic")
copy(out)
