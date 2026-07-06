/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

async function sendValueToBackend(shift_id, choice, comment) {
    await rpc("/my/shifs-needed/set_shift_offer", {
        shift_id,
        choice,
        comment,
    });
}

window.odoo = window.odoo || {};
window.odoo.shift_offer_sendValueToBackend = sendValueToBackend;
