const AzureSearch = require('azure-search');
var client = AzureSearch({
    url: "https://cloudfoodies-basic.search.windows.net",
    key: "17E8CC73BADFC27595E85B7C4F047F2C",
    version: "2017-11-11"
});



module.exports.search = function(query, cb) {
    var opt = {
        search: query,
        top: 10
    };
    client.search('documentdb-index', opt, cb);
};

