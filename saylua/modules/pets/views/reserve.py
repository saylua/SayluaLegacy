from flask import render_template, g, redirect, request, flash
from saylua import db
from saylua.wrappers import login_required
from ..models.db import Pet
from saylua.utils import corpus, add_article

import datetime
import random


def pet_reserve():
    new_adoptee = Pet.query.filter(Pet.guardian_id == None).order_by(db.func.random()).first() # noqa
    if new_adoptee is None:
        return render_template("reserve_empty.html")
    cute_texts = (["This {} really likes you!".format(random.choice(corpus.little_pet)),
            "This {} looks like it likes you!".format(new_adoptee.species.name.capitalize()),
            "Have you ever considered adopting {}?".format(add_article(new_adoptee.species.name.capitalize()))])
    cute_text = random.choice(cute_texts)
    return render_template("reserve.html", adoptee=new_adoptee, cute_text=cute_text)


@login_required(redirect='pets.reserve', error='You need to be logged in to adopt a companion!')
def pet_reserve_post():
    adopter = g.user
    soul_name = request.form.get('soul_name')
    adoptee = db.session.query(Pet).filter(Pet.soul_name == soul_name).one_or_none()
    youngest = (Pet.query.filter(Pet.guardian_id == g.user.id)
            .order_by(Pet.date_bonded.desc()).first())
    if youngest and (datetime.datetime.now() - youngest.date_bonded).days < 1:
        flash(("I'm afraid I can't let you adopt adopt a new companion today, " +
            "you should focus on making sure {} is settling into their new home.")
            .format(youngest.name))
    elif adoptee is None:
        flash("Sorry, I couldn't find a pet with that soul name.")
    elif adoptee.guardian_id is not None:
        flash("I'm afraid {} already has a companion.".format(adoptee.name))
    else:
        adoptee.guardian_id = adopter.id
        adoptee.date_bonded = db.func.now()
        db.session.add(adoptee)
        if adopter.companion is None:
            adopter.companion = adoptee
            db.session.add(adopter)
        db.session.commit()
        flash("You have adopted {}!".format(adoptee.name))
        return redirect(adoptee.url(), code=302)
    return redirect('/reserve/', code=302)
