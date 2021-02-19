
'use strict';



    var AWS = require("aws-sdk");
    AWS.config.update({region: 'us-east-1'});
    var sqs = new AWS.SQS();
    var sqs_URL = "https://sqs.us-east-1.amazonaws.com/452853680688/user-info";

     
// Close dialog
function close(sessionAttributes, fulfillmentState, message) {
    return {
        sessionAttributes,
        dialogAction: {
            type: 'Close',
            fulfillmentState,
            message,
        },
    };
}

// Function for duspatching message for each intent of Amazon lEX
function dispatch(intentRequest, callback) {
    const intentName = intentRequest.currentIntent.name;
    const sessionAttributes = intentRequest.sessionAttributes;
    
    if (intentName == "GreetingIntent") {
        callback(close(sessionAttributes, 'Fulfilled',
        {'contentType': 'PlainText', 'content': `Hi there, how can I help you?`}));
    } else if (intentName == "ThankYouIntent") {
        callback(close(sessionAttributes, 'Fulfilled',
        {'contentType': 'PlainText', 'content': `Your're welcome!`}));
    } else if (intentName == "DiningSuggestionsIntent") {
        
        var params = {
            MessageBody: messageGenerator(intentRequest),
            QueueUrl: sqs_URL,
        };
        
        sqs.sendMessage(params, function(err, data) {
            if (err) {
                console.log("Error", err);
            } else {
                console.log("Success", data.MessageId);
                callback(close(sessionAttributes, 'Fulfilled',
                {'contentType': 'PlainText', 'content': `You’re all set. Expect my suggestions shortly! Have a good day.`}));
            }
        });
    }
    
}

function messageGenerator(event) {
    var message = {
        Location: event.currentIntent.slots.location.toLowerCase(),
        Cuisine: event.currentIntent.slots.cuisine.toLowerCase(),
        Amount: event.currentIntent.slots.amount.toLowerCase(),
        Date: event.currentIntent.slots.date,
        Time: event.currentIntent.slots.time,
        PhoneNumber: event.currentIntent.slots.cell
    };
    return JSON.stringify(message);
}
 
// --------------- Main handler -----------------------
 
// Route the incoming request based on intent.
// The JSON body of the request is provided in the event slot.
exports.handler = (event, context, callback) => {
    try {
        dispatch(event,
            (response) => {
                callback(null, response);
            });
            
    } catch (err) {
        var message = "Sorry, we are unable to provide any recommendation."
        callback(null, message);
    }
};

                
        
     