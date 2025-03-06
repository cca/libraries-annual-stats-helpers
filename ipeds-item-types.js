// https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?id=172&op=run
const map = {
    '': 'Other',
    'ARCHIVE': 'Books',
    '2DAYRES': 'Books',
    '2HOURRES': 'Books',
    '3HOURRES': 'Books',
    'LIBUSEBK': 'Books',
    'BOOK': 'Books',

    'EBOOK': 'Digital/Electronic Books',

    'DVD': 'Media',
    'EQUIPMENT': 'Media',
    'LIBUSEDVD': 'Media',
    'LIBUSESUPP': 'Media',
    'LIBUSEVIDE': 'Media',
    'MATSAMP': 'Media',
    'MIXEDMEDIA': 'Media',
    'REALIA': 'Media',
    'SUPPL': 'Media',
    'VIDEOTAPE': 'Media',

    'BOUNDPER': 'Serials',
    'NEWPER': 'Serials',
}
let sum = {}
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = 0
}
// loop over table & add each row to its matching sum entry
$('table tr').each((index, row) => {
    if ($(row).find('td').length === 2) {
        let type = $(row).find('td').first().text().trim()
        let quantity = parseInt($(row).find('td').last().text().trim())
        console.log(type, quantity)
        sum[map[type]] += quantity
    }
})
// printy/copy to clipboad in a nicer format
let out = ''
out += 'Type\tNumber of Titles\n'
for (let key in sum) {
    if (key !== 'undefined') out += `${key}\t${sum[key]}\n`
}
console.log(out)
