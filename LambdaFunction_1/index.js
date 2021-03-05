'use strict';
// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

// Close dialog with the customer, reporting fulfillmentState of Failed or Fulfilled ("Thanks, your pizza will arrive in 20 minutes")
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
 
// --------------- Events -----------------------
 
function dispatch(intentRequest, callback) {
    console.log(`request received for userId=${intentRequest.userId}, intentName=${intentRequest.currentIntent.name}`);
    const sessionAttributes = intentRequest.sessionAttributes;
    const slots = intentRequest.currentIntent.slots;
    const location = slots.location;
    const cuisine = slots.cuisine;
    const numberOfPeople = slots.numberOfPeople;
    const date = slots.date;
    const time = slots.time;
    const Email_address = slots.email;
    
    var params = {
       // Remove DelaySeconds parameter and value for FIFO queues
    DelaySeconds: 3,
     
      MessageBody: 'Location:'+location+'Cuisine:'+cuisine+
      'Numberofpeople:'+numberOfPeople+'Date:'+date+'Time:'+time
      +'Email_address:'+Email_address,
      
      QueueUrl: "https://sqs.us-east-1.amazonaws.com/213660796932/Q1"
    };

    sqs.sendMessage(params, function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
        console.log("Success", data.MessageId);
      }
    });
    callback(close(sessionAttributes, 'Fulfilled',
    {'contentType': 'PlainText', 'content': `You’re all set. Expect my suggestions shortly! Have a good day.`}));
    
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
        callback(err);
    }
};