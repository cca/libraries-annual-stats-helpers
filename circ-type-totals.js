// Koha report: https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?op=run&id=231
const map = {
    '': 'Other materials',
    'ARCHIVE': 'Other materials',
    '2DAYRES': 'Books',
    '2HOURRES': 'Books',
    '3HOURRES': 'Books',
    'BK': 'Books',
    'BOOK': 'Books',
    'BOUNDPER': 'Periodicals',
    'DVD': 'Videos',
    'EQUIPMENT': 'Equipment',
    'LIBUSEBK': 'Books',
    'LIBUSEBOOK	': 'Books',
    'LIBUSEDVD': 'Videos',
    'LIBUSESUPP': 'Other materials',
    'LIBUSEVIDE': 'Videos',
    'MATSAMP': 'Materials Samples',
    'MIXEDMEDIA': 'Other materials',
    'NEWPER': 'Periodicals',
    'REALIA': 'Other materials',
    'SUPPL': 'Other materials',
    'VIDEOTAPE': 'Videos'
}
let sum = {}
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = 0
}
// loop over table & add each row to its matching sum entry
$('#report_results tr').each((index, row) => {
    if (index != 0) {
        let type = $(row).find('td').eq(0).text().trim()
        let quantity = parseInt($(row).find('td').eq(1).text().trim())
        console.log(type, quantity)

        if (sum.hasOwnProperty(map[type])) {
            sum[map[type]] += quantity
        }
    }
})
// printy/copy to clipboad in a nicer format
let out = 'Type\tTotal\n'
for (let key of Object.keys(sum).sort()) {
    out += `${key}\t${sum[key]}\n`
}
console.log(out + '\n')
