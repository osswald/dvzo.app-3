FROM odoo:16

USER root

RUN pip3 install setuptools wheel
RUN pip3 install python-jose requests

USER odoo
