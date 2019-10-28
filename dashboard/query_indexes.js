var faunadb = require('faunadb'),
q = faunadb.query;

DATABASE_URL = '54.245.218.63'

console.log('Node.js code is now running!')
var client = new faunadb.Client({ secret: 'secret', domain: DATABASE_URL, scheme: 'http', port: '8443'});

// Create index for duration of matches
client.query(
    q.CreateIndex(
        {
            name: 'matches_raw_duration', 
            source: q.Collection('matches_raw'), 
            terms: [], 
            values: [{ field: ['data', 'result', 'duration'] }]
        }
    )
).then(
    (ret) => console.log(ret)
)

// Create index for provenance of api_call_type
client.query(
    q.CreateIndex(
        {
            name: 'matches_raw_prov_api_duration', 
            source: q.Collection('matches_raw'), 
            terms: [], 
            values: [{ field: ['data', 'provenance', 'dataFetchStage', 'apiCallDuration'] }]
        }
    )
).then(
    (ret) => console.log(ret),
    (err) => console.log(err)
)

// Create index for average first blood
client.query(
    q.CreateIndex(
        {
            name: 'matches_raw_fb_time', 
            source: q.Collection('matches_raw'), 
            terms: [], 
            values: [{ field: ['data', 'results', 'first_blood_time'] }]
        }
    )
).then(
    (ret) => console.log(ret),
    (err) => console.log(err)
)

// Raw Data Count index
client.query(
    q.CreateIndex({
        name: 'all_raw_matches',
        source: q.Collection('matches_raw')
    })
).then(
    (ret) => console.log(ret),
    (err) => console.log(err)
)