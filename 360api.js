// ! This uses an UNPUBLISHED API — there is no guarantee the final product will work the same way.
// To get our complete list of subscribed databases:
// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/databaselist?apikey=
// To get information (and holdings) on a specific database:
// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/database/ADCGP?apikey=

let apiKey = process.env["360_API_KEY"]
// Three kinds of databases: paid subscriptions we count, special ones to ignore (e.g. LibGuides, CCA Print Holdings),
// & OA databases we do not count.
const subscribedDbs = ['AMZ', 'AAUAA', 'RDU', 'AUKZS', '~IF', 'AAGCL', 'AHLUM', 'DISTE', 'ILR', 'TAN', 'ACQHD', 'ELS', 'FTC', 'AAALR', 'AEFEZ', 'ABJKU', 'ADMOD', 'AAGNS', 'AIFPJ', 'AAGBT', 'ABVFA', 'AFSPT', 'AFHTS', 'AAVGA', 'AAOBU', 'RMI', 'MPCAJ', 'ENS', 'BWG', 'AALBR', 'DGR', 'X27', 'SJN', 'SBO', 'TFL', '1OC', 'PQBIZ', 'JST', 'M2O', 'AONYA', 'A.0', 'JLS' ]
const ignoredDbs = ['ARRKV', 'AUJGY', 'AADMN', 'AEPGA']

// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/export/page/1
// let root = "https://api-eu.hosted.exlibrisgroup.com" // ? will api-eu be our subdomain?
let root = "https://api-na.hosted.exlibrisgroup.com"
let service = "360"
let apiVersion = "v1"
let baseUrl = `${root}/${service}/${apiVersion}`

async function getDbList() {
    // how do we pass our library code?
    let response = await fetch(`${baseUrl}/library/databaselist?apikey=${apiKey}`)
    let data = await response.json()
    return data
}

async function getDb(dbCode) {
    let response = await fetch(`${baseUrl}/library/database/${dbCode}?apikey=${apiKey}`)
    let data = await response.json()
    return data
}

let totals = {"Databases": 0, "Open Access": 0, "Holdings": {} }

const dbList = await getDbList()
for (let db of dbList) {
    if (subscribedDbs.includes(db.databaseCode)) {
        let dbData = await getDb(db.databaseCode)
        // verify assumption: each response has only one provider providing only one database
        if (dbData.providers.length !== 1) {
            console.log(`Warning: ${db.databaseName} (${db.databaseCode}) has ${dbData.providers.length} providers`)
        }
        if (dbData.providers[0].databases.length !== 1) {
            console.log(`Warning: ${db.databaseName} (${db.databaseCode}) has ${dbData.providers[0].databases.length} databases`)
        }

        let holdings = dbData.providers[0].databases[0].holdings
        console.log(`${db.databaseName} (${db.databaseCode}) has ${holdings ? holdings.length : 0} holdings`)
        if (holdings) holdings.forEach(holding => {
            const type = holding.titleType
            if (!totals["Holdings"][type]) {
                totals["Holdings"][type] = 0
            }
            totals["Holdings"][type] += 1
        })

        // Strange logic here: if a database has ZERO holdings, we want to count it (e.g. LISTA, Kanopy)
        // but if a database has a small number of holdings (we somewhat arbitrarily say 5 or fewer), then it is probably
        // a journal package for which we only subscribe to a few titles (e.g. Duke U Press, Taylor & Francis)
        // and we do not want to count it as a database.
        if (!holdings || holdings.length > 5) {
            totals["Databases"] += 1
        }
    } else if (ignoredDbs.includes(db.databaseCode)) {
        console.log(`${db.databaseName} (${db.databaseCode}) is ignored`)
    } else {
        console.log(`${db.databaseName} (${db.databaseCode}) is considered Open Access`)
        totals["Open Access"] += 1
    }
}

console.log('\n======== Totals ========')
console.log(totals)
// We have yet to see a titleType other than Book, Journal, or Video but our code can handle one
console.log('\nGenerally, for data reporting purposes, Journal holdings are considered Digital/Electronic Serials, Books are considered Digital/Electronic Books, and Video are considered Digital/Electronic Media.')
