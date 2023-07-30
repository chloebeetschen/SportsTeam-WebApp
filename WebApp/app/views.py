from flask import render_template, flash, request, redirect, session, url_for, g
from app import app, db
from .models import Member, Fixture, FixtureInfo
from .forms import LoginForm, ResetPass, MemberForm, ContactUsForm, FixtureForm
import datetime
import hashlib

logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    members = Member.query.all()
    if form.validate_on_submit():
        for m in members:
            if m.email == form.email.data:
                if str((hashlib.md5((form.password_hash.data).encode()).hexdigest())) == m.password_hash:
                    app.logger.info('%s logged in successfully',form.email.data)
                    flash("You have logged in succesfully!")
                    session['logged_in'] = True

                    return redirect('/')

        app.logger.info('%s failed to log in successfully',form.email.data)
        flash("Email or Password incorrect, please try again")

    return render_template('login.html',
                           title='Login',
                           form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPass()
    members = Member.query.all()
    if form.validate_on_submit():
        
        for m in members:
            if m.email == form.email.data and m.fname == form.fname.data and m.lname == form.lname.data:
                if form.password_hash.data == form.conf_password_hash.data:
                    
                    m.password_hash = str(hashlib.md5((form.password_hash.data).encode()).hexdigest())                    
                    db.session.commit()

                    app.logger.info('%s changed their password successfully',form.email.data)
                    flash("You have changed your password succesfully!")
                    return redirect('/login')
                else:
                    flash("Passwords didnt match please try again")
                    app.logger.info('%s failed to change their password successfully',form.email.data)

        app.logger.info('%s failed to change their password successfully',form.email.data)
        flash("User details not recognised")


    return render_template('forgot_password.html',
                           title='Reset Password',
                           form=form)



#add member form page
@app.route('/join', methods=['GET', 'POST'])
def join():
    form  = MemberForm()
    if form.validate_on_submit():
        app.logger.info('%s joined the team successfully',form.email.data)
        flash("You have joined succesfully!")
        m = Member(fname=form.fname.data, lname=form.lname.data, email=form.email.data, password_hash=str((hashlib.md5((form.password_hash.data).encode()).hexdigest())), position=form.position.data)
        db.session.add(m)
        db.session.commit()

        session['logged_in'] = True

        return redirect('/')


    return render_template('join.html',
                           title='Join',
                           form=form)
    
#contact form page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if session.get('logged_in'):
        form  = ContactUsForm()
        if form.validate_on_submit():
            app.logger.info('contact form  submitted')
            flash("Your query has been sent succesfully!")
        return render_template('contact.html',
                            title='Contact',
                            form=form)
    else:
        form  = ContactUsForm()
        if form.validate_on_submit():
            app.logger.info('contact form  submitted')
            flash("Your query has been sent succesfully!")
        return render_template('contact2.html',
                            title='Contact',
                            form=form)

#add fixture form                            
@app.route('/add_fixture', methods=['GET', 'POST'])
def add_fixture():
    form  = FixtureForm()
    if form.validate_on_submit():
        app.logger.info('fixture added successfully')
        flash("Fixture added succesfully!")
        f1 = Fixture(team=form.team.data, home_away=form.home_away.data, date=form.date.data)
        f2 = FixtureInfo(location=form.location.data, meet_loc=form.meet_loc.data, time=form.time.data, meet_time=form.meet_time.data)
        for membid in form.members.data:
            member = Member.query.get(membid)
            f1.members.append(member)
        db.session.add(f1)
        db.session.add(f2)
        db.session.commit()
        
        return redirect('/fixtures')

    return render_template('add_fixture.html',      
                            title='AddFixture',
                            form=form)

@app.route('/fixtures', methods=['GET'])
def fixtures():
    fixtures = Fixture.query.all()
    return render_template('fixtures.html',
                            title='Fixtures',
                            fixtures=fixtures)

@app.route('/fixture_info_lineup/<id>', methods=['GET'])
def fixturesInforLineup(id):
    f = Fixture.query.filter_by(fixtureId=id).first()
    f2 = FixtureInfo.query.filter_by(id=id).all()

    return render_template('fixture_info_lineup.html',
                            title='Fixture Info for ' + str(f),
                            info=f2,
                            lineup=f.members)

@app.route('/fixtures_played/<id>', methods=['GET'])
def fixturesPlayed(id):
    m = Member.query.filter_by(memberId=id).first()
    f = Fixture.query.filter_by(fixtureId=id).first()

    return render_template('fixtures_played.html',
                            title='Fixture Played by ' + str(m),
                            fixtures=m.fixtures)

@app.route('/team', methods=['GET'])
def team():
    members = Member.query.all()
    return render_template('team.html',
                            title='Team',
                            members=members)

@app.route('/delete_player/<id>', methods=['GET'])
def delete_player(id):
    app.logger.info('member deleted successfully')
    player = Member.query.get(id)
    db.session.delete(player)
    db.session.commit()
    return redirect('/team')

@app.route('/delete_fixture/<id>', methods=['GET'])
def delete_fixture(id):
    app.logger.info('fixture deleted successfully')
    fixture = Fixture.query.get(id)
    db.session.delete(fixture)
    db.session.commit()
    return redirect('/fixtures')

@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('home.html',
                                title='Home')
    else:
        return render_template('home2.html',
                                title='Home')

