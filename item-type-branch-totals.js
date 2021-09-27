// Koha report: https://library-staff.cca.edu/cgi-bin/koha/reports/guided_reports.pl?phase=Run+this+report&reports=228&limit=40
const map = {
    '': 'Other',
    '2DAYRES': 'Reserves',
    '2HOURRES': 'Reserves',
    '3HOURRES': 'Reserves',
    'BK': 'Books',
    'BOOK': 'Books',
    'BOUNDPER': 'Periodicals',
    'DVD': 'Videos',
    'EQUIPMENT': 'Other',
    'LIBUSEBK': 'Books',
    'LIBUSEBOOK	': 'Books',
    'LIBUSEDVD': 'Videos',
    'LIBUSESUPP': 'Other',
    'LIBUSEVIDE': 'Videos',
    'MIXEDMEDIA': 'Other',
    'NEWPER': 'Periodicals',
    'REALIA': 'Other',
    'SUPPL': 'Other'
}
let sum = {}
// build the categories from the map
for (let key in map) {
    if (!sum[map[key]]) sum[map[key]] = {'OAK': 0, 'SF': 0}
}
// loop over table & add each row to its matching sum entry
$('table tr').each((index, row) => {
    if ($(row).find('td').length === 3) {
        let type = $(row).find('td').eq(0).text()
        let branch = $(row).find('td').eq(1).text()
        let quantity = parseInt($(row).find('td').eq(2).text())

        if (sum.hasOwnProperty(map[type])) {
            sum[map[type]][branch] += quantity
        }
    }
})
// print/copy to clipboad in a nicer format
let out = 'Type\tMeyer\tSimpson\n'
for (let key in sum) {
    out += `${key}\t${sum[key].OAK}\t${sum[key].SF}\n`
}

console.log(out)
console.log("\n%c copied to your clipboard", "font-style: italic")
copy(out)
