// Koha report: https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?phase=Run+this+report&reports=231
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
    // NOTE: this is for when material samples are checked out of non-MATLIB
    // locations (e.g. Simpson). Matlib transactions are totalled separately.
    'MATSAMP': 'Other materials',
    'MIXEDMEDIA': 'Other materials',
    'NEWPER': 'Periodicals',
    'REALIA': 'Other materials',
    'SUPPL': 'Other materials',
    'VIDEOTAPE': 'Videos'
}
let sum = {}
let matlib = 0
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = {'OAK': 0, 'SF': 0}
}
// loop over table & add each row to its matching sum entry
$('table tr').each((index, row) => {
    if (index != 0) {
        let type = $(row).find('td').eq(0).text().trim()
        let branch = $(row).find('td').eq(1).text().trim()
        let quantity = parseInt($(row).find('td').eq(2).text().trim())

        if (branch === 'MATLIB') {
            matlib += quantity
        } else if (sum.hasOwnProperty(map[type])) {
            sum[map[type]][branch] += quantity
        }
    }
})
// printy/copy to clipboad in a nicer format
let out = 'Type\tMeyer Total\n'
for (let key in sum) {
    out += `${key}\t${sum[key].OAK}\n`
}
console.log(out + '\n')
out = 'Type\tSimpson Total\n'
for (let key in sum) {
    out += `${key}\t${sum[key].SF}\n`
}
console.log(out + '\n')
console.log(`Materials Library\t${matlib}`)
