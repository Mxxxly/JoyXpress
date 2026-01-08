from flask import Blueprint
paymentobj = Blueprint('bppayment',__name__,template_folder='templates',static_folder='static',url_prefix='/payment')

# to make the local routes available

from pkg.payments import routes #from. import routes 