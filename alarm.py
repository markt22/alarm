from crontab import CronTab, CronItem

Days = ["Su", "M", "Tu", "W", "Th", "F", "Sa", "Su"]

def get_description(self):
    """
    Get_description is a Monkey Patch for CronItem

    Provides a description string for the alarm applicatiom
    """
    days = str(self.dow)
    if days == '*':
        day = 'Everyday'
    else:
        day = ''
        for aday in days.split(","):
            day += Days[int(aday)] + " "
    enabled = 'Enabled' if self.enabled else 'Disabled'
    desc = "Alarm set for {0} at {1}:{2} ({3})".format(
            day, self.hour, self.minute, enabled)
    return desc

CronItem.get_description = get_description

class Jobs():
    """
    A list of jobs extracted from crontab file.
    
    This class is used to interact with the crontab file and 
    manipulate the command entries.

    Parameters
    ----------
    user : String, required
        user of the crontab file used
    cmd : String, required
        command string that cron will execute 
    """

    def __init__(self, user, cmd):
        self.cron = CronTab(user="mtaylor")
        self.jobs = list(self.cron.find_command(cmd))
        self.cmd = cmd

    def __iter__(self):
        return JobIterator(self.jobs)

    def NumberAlarms(self):
        return len(self.jobs)
    
    def test(self):
        print "We are testing"
        for job in self.jobs:
            print job

    def command(self):
        return self.cmd

    def daysTime(self):
        return JobDayTimeStringIterator(self.jobs)

    def get(self, idx):
        return self.jobs[idx]

    def CreateJob(self, min="*", hour="*", dom="*", mon="*", dow="*"):
        try:
            time = "{} {} {} {} {}".format(
                min,
                hour,
                dom,
                mon,
                dow)
        except TypeError as e:
            print "Invalid parameters"
            pass
        print time

class JobDayTimeStringIterator:
    """
    Iterator interface for the jobs class 
    that returns a easy readable format
    """
    def __init__(self, jobs):
        self.jobs = jobs
        self.index = 0
    
    def next(self):
        try:
            job = self.jobs[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        
        return job.get_description()

    def __iter__(self):
        return self 

class JobIterator:
    """
    Iterator interface for the Jobs class

    """
    def __init__(self, jobs):
        self.jobs = jobs
        self.index = 0
    
    def next(self):
        try:
            job = self.jobs[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return (self.index-1, job)

    def __iter__(self):
        return self 


if __name__ == "__main__":
    jobs = Jobs("mtaylor","alarm.sh")
    print jobs.NumberAlarms()
    for job in jobs:
        print job[1].get_description()
        print job[1].enabled
    job[1].set_comment("this 2 is a test")
    jobs.test()



