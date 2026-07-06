FROM odoo:19

USER root

RUN pip3 install setuptools wheel
RUN pip3 install python-jose requests ofxparse
RUN pip3 install phonenumbers

USER odoo
