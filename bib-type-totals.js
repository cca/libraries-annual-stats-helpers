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
    'DIGITAL': 'Other',
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
    'SUPPL': 'Other',
    'VIDEOTAPE': 'Videos',
}
let sum = {}
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = {Titles: 0, Items: 0}
}
// loop over table & add each row to its matching sum entry
$('table tr').each((index, row) => {
    if ($(row).find('td').length === 3) {
        let type = $(row).find('td').eq(0).text().trim()
        // skip ILL item, not part of our collection
        if (type === 'ILL') return
        let titles = parseInt($(row).find('td').eq(1).text().trim())
        let items = parseInt($(row).find('td').eq(2).text().trim())
        sum[map[type]].Titles += titles
        sum[map[type]].Items += items
    }
})
// sort categories alphabetically but put 'Other' at the end
let cats = Object.keys(sum).sort()
cats.splice(cats.indexOf('Other'), 1)
cats.push('Other')

// printy/copy to clipboad in a nicer format
let out = 'Type\tNumber of Titles\tNumber of Items\n'
cats.forEach(c => {
    // handle edge case (true for Digital/Electronic) where we have more items
    // than titles, which doesn't really make sense (it's because of item-less
    // bib records that are just links to websites)
    let items = sum[c].Items
    let titles = sum[c].Titles
    if (items < titles) items = titles
    if (c !== 'undefined') out += `${c}\t${titles}\t${items}\n`
})

console.log(out)
console.log("\n%c copied to your clipboard", "font-style: italic")
copy(out)
