#!/usr/bin/env python3
"""Apply Odoo 16 -> 19 compatibility changes to custom addon XML files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

CUSTOM_MODULES = [
    "dvzo",
    "training",
    "train_management",
    "member",
    "emergency_contact",
    "key_management",
    "minimal_hours",
    "risk_management",
    "inventory",
    "uniform",
    "web_window_title",
]

ADDONS_ROOT = Path(__file__).resolve().parents[1] / "addons"

ATTRS_REPLACEMENTS = [
    (
        r'''attrs="\{'invisible': \[\('has_locomotive', '=', False\)\]\}"''',
        'invisible="not has_locomotive"',
    ),
    (
        r'''attrs="\{'invisible': \[\('approximate_times', '=', False\)\]\}"''',
        'invisible="not approximate_times"',
    ),
    (
        r'''attrs="\{'invisible': \[\('state', '!=', 'draft'\)\]\}"''',
        'invisible="state != \'draft\'"',
    ),
    (
        r'''attrs="\{'invisible': \[\('state', '!=', 'executed'\)\]\}"''',
        'invisible="state != \'executed\'"',
    ),
    (
        r'''attrs="\{'invisible': \[\('state', '!=', 'canceled'\)\]\}"''',
        'invisible="state != \'canceled\'"',
    ),
    (
        r'''attrs="\{'readonly': \[\('is_record_saved','=',True\)\]\}"''',
        'readonly="is_record_saved"',
    ),
    (
        r'''attrs="\{'readonly': \[\('is_record_saved', '=', True\)\]\}"''',
        'readonly="is_record_saved"',
    ),
    (
        r'''attrs="\{'invisible': \[\('not_monitored', '=', True\)\]\}"''',
        'invisible="not_monitored"',
    ),
    (
        r'''attrs="\{'invisible': \[\('is_vendor', '=', False\)\]\}"''',
        'invisible="not is_vendor"',
    ),
    (
        r'''attrs="\{'invisible': \[\('risk_assessment', '=', False\)\]\}"''',
        'invisible="not risk_assessment"',
    ),
]

STATES_REPLACEMENTS = [
    (
        r'states="running"',
        'invisible="state != \'running\'"',
    ),
    (
        r'states="planned"',
        'invisible="state != \'planned\'"',
    ),
    (
        r'states="planned,running"',
        'invisible="state not in (\'planned\', \'running\')"',
    ),
    (
        r'states="draft"',
        'invisible="state != \'draft\'"',
    ),
    (
        r'states="confirmed"',
        'invisible="state != \'confirmed\'"',
    ),
]


def migrate_xml(content: str) -> str:
    content = content.replace("<tree", "<list")
    content = content.replace("</tree>", "</list>")
    content = content.replace('view_mode">tree', 'view_mode">list')
    content = content.replace('view_mode">tree,form', 'view_mode">list,form')
    content = content.replace('view_mode">tree,kanban', 'view_mode">list,kanban')
    content = content.replace('view_mode">kanban,tree', 'view_mode">kanban,list')
    content = content.replace('view_mode">tree,form,kanban', 'view_mode">list,form,kanban')
    content = re.sub(
        r'<field name="numbercall">-?\d+</field>\s*',
        "",
        content,
    )
    content = re.sub(
        r'<field name="doall" eval="(?:True|False)"/>\s*',
        "",
        content,
    )
    content = re.sub(
        r'<div class="oe_chatter">.*?</div>',
        "<chatter/>",
        content,
        flags=re.DOTALL,
    )
    content = content.replace('t-name="kanban-box"', 't-name="card"')
    content = content.replace("t-field-options=", "t-options=")
    for pattern, replacement in ATTRS_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    for pattern, replacement in STATES_REPLACEMENTS:
        content = content.replace(pattern, replacement)
    return content


def migrate_module(module_name: str) -> int:
    module_path = ADDONS_ROOT / module_name
    if not module_path.exists():
        print(f"skip missing module: {module_name}")
        return 0

    changed_files = 0
    for xml_file in module_path.rglob("*.xml"):
        original = xml_file.read_text(encoding="utf-8")
        migrated = migrate_xml(original)
        if migrated != original:
            xml_file.write_text(migrated, encoding="utf-8")
            changed_files += 1
            print(f"updated {xml_file.relative_to(ADDONS_ROOT.parent)}")
    return changed_files


def main() -> int:
    total = 0
    for module in CUSTOM_MODULES:
        total += migrate_module(module)
    print(f"migrated {total} XML files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
