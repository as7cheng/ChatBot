// import
var AWS = require("aws-sdk");

// Call bot
var lexruntime = new AWS.LexRuntime();

// Store bot's name alias and userID
var bot_name = "diningrobot";
var bot_alias = "beta";
var user_ID = "LF0";

// Handle user's input
exports.handler = (event, context, callback) => {
    
    // Get user's input
    var message = event.messages[0].unstructured.text;
    
    // Create test sending to bot
    var params = {
        botName: bot_name,
        botAlias: bot_alias,
        inputText: message,
        userId: user_ID,
        requestAttributes: {},
        sessionAttributes: {}
    };

    // Request bot and get reply
    lexruntime.postText(params, function(err, data) {
        // An error happens
        if (err) {
            console.log(err);
            callback(err);
        }
        // No error, create response sending to user
        else {
            // Construct the return vallue
            var response = {
                statusCode: 200,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                messages: [ 
                        {
                            type: 'unstructured', 
                            unstructured: 
                            {text: data.message} 
                        },
                    ],

            }
            // Since callback doesn't give the right format
            // return the callback value
            return callback(null, response);
        }
    });
};