#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ADDONS="$ROOT/addons"
TMP="$ROOT/.oca-tmp"

rm -rf "$TMP"
mkdir -p "$TMP"

clone_and_copy() {
  local repo="$1"
  local branch="$2"
  shift 2
  local modules=("$@")
  local dest="$TMP/$(basename "$repo")"

  git clone --depth 1 --branch "$branch" "https://github.com/$repo.git" "$dest"
  for module in "${modules[@]}"; do
    if [[ -d "$dest/$module" ]]; then
      rm -rf "$ADDONS/$module"
      cp -a "$dest/$module" "$ADDONS/$module"
      echo "installed $module from $repo@$branch"
    else
      echo "warning: $module not found in $repo@$branch" >&2
    fi
  done
}

clone_and_copy OCA/account-reconcile 19.0 account_statement_base
clone_and_copy OCA/helpdesk 19.0 helpdesk_mgmt helpdesk_type
clone_and_copy OCA/partner-contact 19.0 partner_firstname
clone_and_copy OCA/bank-statement-import 19.0 \
  account_statement_import_base \
  account_statement_import_file \
  account_statement_import_camt \
  account_statement_import_camt54
clone_and_copy OCA/server-auth 19.0 auth_oidc

# OFX import is not yet published on OCA 19.0; keep the migrated 18.0 module copy.

rm -rf "$TMP"
echo "OCA modules updated to 19.0"
