from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@login_required
@views.route('/')
def home():
    return render_template("base.html", user=current_user)

