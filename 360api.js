// ! This uses an UNPUBLISHED API — there is no guarantee the final product will work the same way.

let apiKey = process.env["360_API_KEY"]

// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/export/page/1
// let root = "https://api-eu.hosted.exlibrisgroup.com" // ? will api-eu be our subdomain?
let root = "https://api-na.hosted.exlibrisgroup.com"
let service = "360"
let apiVersion = "v1"
let baseUrl = `${root}/${service}/${apiVersion}`

async function main() {
    // how do we pass our library code?
    let response = await fetch(`${baseUrl}/databaselist?apikey=${apiKey}`)
    let data = await response.json()
    return data
}

console.log(main())

// this works:
// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/database/ADCGP?apikey=
// but that's because it's not library-specific...I can't see how to make the library specific routes work
// e.g.
// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/databaselist?library=CC9&apikey=
// returns an empty array and I tried library, libraryCode, code, LibraryCode
// replacing /library/ with /CC9/ causes the site to respond with a server error
// https://api-eu.hosted.exlibrisgroup.com/360/v1/library/export/page/1?library=CC9&apikey=
// returns {"status":404,"error":"Data not found","message":"Get library data not found"}
