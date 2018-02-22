from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

from alarm import Jobs

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Sublimey')

class AlarmForm(FlaskForm):
    name = StringField('Alarm Name:', validators=[DataRequired()])
    hour = IntegerField('Hour:' , validators=[NumberRange(min=1, max=12, message='Valid hours are 1 thru 12')])
    minute = IntegerField('Minute:', validators=[NumberRange(min=0, max=59, message='Valid minutes 0 thru 59')])


class DaysForm(AlarmForm):
    SUN = BooleanField('Sunday', default=True )
    MON = BooleanField('Monday', default=True )
    TUE = BooleanField('Tuesday', default=True )
    WED = BooleanField('Wednesday', default=True )
    THU = BooleanField('Thursday', default=True )
    FRI = BooleanField('Friday', default=True )
    SAT = BooleanField('Saturday', default=True )
    submit = SubmitField('Set Alarm')



app = Flask(__name__)
app.config['SECRET_KEY'] = 'a sailor went 2 CCC to C what he/she could CCC'
app.jinja_env.auto_reload = True
bootstrap = Bootstrap(app)
moment = Moment(app)
jobs = Jobs("mtaylor","alarm.sh")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', 
                            current_time=datetime.utcnow(), alarms=jobs)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/alarm/<idx>', methods=['GET','POST'])
def alarm(idx):
    form = DaysForm()
    the_alarm = jobs.get_job(int(idx))
    form.hour.data = int(str(the_alarm.hour))
    form.minute.data = int(str(the_alarm.minute))
    for day in the_alarm.days:
        checked = the_alarm.get_day(day)
        form[day].data = checked
    if form.validate_on_submit():
        flash('Alarm saved')
        session['alarm']=form.hour.data
        the_alarm.dow.clear()
        for day in the_alarm.days:
            if form[day].data == True:
                the_alarm.dow.on(day)
        print the_alarm

        return redirect(url_for('index'))
    return render_template('set.html', form=form, alarm=the_alarm)
    


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
     app.run()

