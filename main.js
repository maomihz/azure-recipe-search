const AzureSearch = require('azure-search');
var client = AzureSearch({
    url: "https://cloudfoodies.search.windows.net",
    key: "CB7438AEBC34A349571CFD3A78424F92",
    version: "2017-11-11"
});

var schema = {
    name: 'index',
    fields:
        [
            {
                name: 'id',
                type: 'Edm.String',
                searchable: false,
                filterable: false,
                retrievable: true,
                sortable: false,
                facetable: false,
                key: true
            },

            {
                name: 'ingredients',
                type: 'Edm.String',
                searchable: true,
                filterable: true,
                retrievable: true,
                sortable: true,
                facetable: true,
                key: false
            },

            {
                name: 'instructions',
                type: 'Edm.String',
                searchable: false,
                filterable: false,
                retrievable: true,
                sortable: false,
                facetable: false,
                key: false
            }],
    scoringProfiles: [],
    defaultScoringProfile: null,
    corsOptions: { allowedOrigins: ["*"] }
};

client.createIndex(schema, function (err, schema) {
    console.log(schema);
    console.log(err.message);
});


var document = {
    id: "test-recipe",
    ingredients: "test ingredients",
    instructions: "test description"
};


client.addDocuments('index', [document], function (err, confirmation) {
    if (err) console.log(err.message);
    // document added
});