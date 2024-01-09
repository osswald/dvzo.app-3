 odoo.define('train_management.shift_offer', function (require) {
        "use strict";
        var ajax = require('web.ajax');
        function sendValueToBackend(offer_id, shift_id, choice, comment) {
           ajax.jsonRpc('/my/shifs-needed/set_shift_offer/', 'call', 
               {
                'offer_id': offer_id,
                'shift_id': shift_id,
                'choice': choice,
                'comment': comment,
               }
             );
        };
        odoo.shift_offer_sendValueToBackend = sendValueToBackend;
});
