var lrs;

try {
    lrs = new TinCan.LRS(
        {
            endpoint: "http://ec2-13-56-161-242.us-west-1.compute.amazonaws.com/data/xAPI",
            username: "a59b3e9175b985da787880ac853e1af57797dc5d",
            password: "b7e6913274742b1cc66b5a85d2fe95f8895744df",
            allowFail: false
        }
    );
}
catch (ex) {
    console.log("Failed to setup LRS object: ", ex);
    // TODO: do something with error, can't communicate with LRS
}


var statement = new TinCan.Statement(
{
    "timestamp": "2018-07-20T09:20:00-06:00",
    "version": "1.0.1",
    "actor": {
        "mbox": "mailto:Jacob@example.com",
        "name": "Jacob",
        "objectType": "Agent"
    },
    "verb": {
        "id": "http://adlnet.gov/expapi/verbs/attended",
        "display": {
            "en-US": "attended"
        }
    },
    "object": {
        "id": "https://alumnica-vle-dev.herokuapp.com/en/odas/14",
        "definition": {
            "name": {
                "en-US": "Evaluation"
            },
            "description": {
                "en-US": "Evaluation"
            }
        },
        "objectType": "Activity"
    }
}
);

$(document).ready(function(){
lrs.saveStatement(
    statement,
    {
        callback: function (err, xhr) {
            if (err !== null) {
                if (xhr !== null) {
                    console.log("Failed to save statement: " + xhr.responseText + " (" + xhr.status + ")");
                    // TODO: do something with error, didn't save statement
                    return;
                }

                console.log("Failed to save statement: " + err);
                // TODO: do something with error, didn't save statement
                return;
            }

            console.log("Statement saved");
            // TOOO: do something with success (possibly ignore)
        }
    }
);

})
