/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        const titleService = useService("title");
        titleService.setParts({ zopenerp: document.title });
    },
});
