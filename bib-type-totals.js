// Koha report: https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?reports=61&phase=Run%20this%20report
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
    'EBOOK': 'Books',
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
// printy/copy to clipboad in a nicer format
let out = ''
out += 'Type\tNumber of Titles\n'
for (let key in sum) {
    if (key !== 'undefined') out += `${key}\t${sum[key]}\n`
}
copy(out)
