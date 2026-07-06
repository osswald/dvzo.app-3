# Odoo 16 → 19 Migration Guide

This repository has been updated for **Odoo 19**. The database itself must still be upgraded through Odoo's official upgrade path.

## What changed in this repo

### Infrastructure

- Docker image: `odoo:16` → `odoo:19`
- PostgreSQL image: `15` → `16`
- Python dependency added for OFX import: `ofxparse`

### OCA modules (replaced with 19.0 branches)

| Module | Source |
|--------|--------|
| `helpdesk_mgmt`, `helpdesk_type` | [OCA/helpdesk](https://github.com/OCA/helpdesk) `19.0` |
| `partner_firstname` | [OCA/partner-contact](https://github.com/OCA/partner-contact) `19.0` |
| `account_statement_base` | [OCA/account-reconcile](https://github.com/OCA/account-reconcile) `19.0` |
| `account_statement_import_*` (except OFX) | [OCA/bank-statement-import](https://github.com/OCA/bank-statement-import) `19.0` |
| `auth_oidc` | [OCA/server-auth](https://github.com/OCA/server-auth) `19.0` |

`account_statement_import_ofx` is not yet available on OCA 19.0. This repo keeps a migrated copy based on the OCA 18.0 module.

Refresh OCA modules with:

```bash
./scripts/fetch_oca_modules.sh
```

### Custom DVZO modules

Custom modules were updated for Odoo 19 API and view changes:

- `<tree>` views → `<list>`
- `attrs` / `states` → `invisible`, `readonly`, `required` expressions
- `oe_chatter` → `<chatter/>`
- Removed deprecated `view_type`, `ir.cron.numbercall`, `ir.cron.doall`
- Replaced `name_search()` overrides with `_rec_names_search`
- Replaced `env.ref(...).read()[0]` with `env['ir.actions.act_window']._for_xml_id(...)`
- Migrated frontend assets to `@odoo-module` syntax
- Fixed security access rules in `member` and `training`

Re-apply XML migrations on custom modules with:

```bash
python3 scripts/migrate_modules_to_19.py
```

## Database upgrade (required)

Odoo does **not** support jumping directly from 16 to 19 at the database level. You must upgrade sequentially:

```
16 → 17 → 18 → 19
```

### Recommended approach

1. **Back up production**
   - Database dump
   - Filestore (`/var/lib/odoo/filestore`)
   - Docker volumes if applicable

2. **Test on staging first**
   - Restore the backup to a staging environment
   - Run the upgrade path on staging before touching production

3. **Upgrade options**
   - **Odoo Enterprise / Odoo.sh**: use the official upgrade service
   - **Odoo Community**: use [Odoo Upgrade Community Utilities (OCU)](https://github.com/OCA/OpenUpgrade) or a hosted migration service
   - Upgrade one major version at a time and validate after each step

4. **Deploy the new code**
   ```bash
   cp ./config/odoo.conf.example ./config/odoo.conf
   cp ./docker-compose.env.example ./docker-compose.env
   docker compose build
   docker compose up -d
   ```

5. **Update modules**
   ```bash
   docker compose exec web odoo -u all -d <your_database> --stop-after-init
   ```

6. **Validate**
   - Login and basic navigation
   - DVZO portal pages (`/my/shifts-needed/`, minimal hours)
   - OIDC authentication
   - Bank statement import (CAMT/OFX)
   - Helpdesk tickets
   - Training, train management, inventory, risk management workflows
   - Scheduled actions / crons

## Rollback plan

Keep the Odoo 16 database backup and Docker images until production has been stable on 19 for at least one full business cycle.

## Known follow-ups

- Watch [OCA/bank-statement-import](https://github.com/OCA/bank-statement-import) for an official `account_statement_import_ofx` 19.0 release
- Re-run `./scripts/fetch_oca_modules.sh` periodically to pick up OCA fixes
- Full regression testing of custom portal and report features is recommended before go-live
