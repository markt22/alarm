from crontab import CronTab, CronItem

Days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

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
            day += Days[int(aday) % 7 ] + " "
    enabled = 'Enabled' if self.enabled else 'Disabled'
    desc = "{} set for {} at {}:{} ({})".format(
            self.comment, day, self.hour, self.minute, enabled)
    return desc

def get_day(self, day):
    """
    get_day is a Monkey Patch for CronItem

    Returns true if the dow is active
    """
    days = str(self.dow)
    rc = False
    if days == '*':
        rc = True
    else:
        for a_day in days.split(','):
            if day == Days[int(a_day) % 7]:
                rc = True
                break

    return rc

#Monkey patch CronItem
CronItem.get_description = get_description
CronItem.get_day = get_day
CronItem.days = Days

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
        self.__cron = CronTab(user="mtaylor")
        self.__jobs = list(self.__cron.find_command(cmd))
        self.__cmd = cmd

    def __iter__(self):
        return JobIterator(self.__jobs)

    def NumberAlarms(self):
        return len(self.__jobs)
    
    def write(self):
        self.__cron.write()

    def test(self):
        print "We are testing"
        for job in self.__jobs:
            print job
    
    @property
    def cmd(self):
        return self.__cmd

    def daysTime(self):
        return JobDayTimeStringIterator(self.__jobs)
    
    def get_job(self, idx):
        return self.__jobs[idx]

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
        self.__jobs = jobs
        self.__index = 0
    
    def next(self):
        try:
            job = self.__jobs[self.__index]
        except IndexError:
            raise StopIteration()
        self.__index += 1
        
        return job.get_description()

    def __iter__(self):
        return self 

class JobIterator:
    """
    Iterator interface for the Jobs class

    """
    def __init__(self, jobs):
        self.__jobs = jobs
        self.__index = 0
    
    def next(self):
        try:
            job = self.__jobs[self.__index]
        except IndexError:
            raise StopIteration()
        self.__index += 1
        return (self.__index-1, job)

    def __iter__(self):
        return self 


if __name__ == "__main__":
    jobs = Jobs("mtaylor","alarm.sh")
    print jobs.cmd
    for job in jobs:
        print job[1].get_description()
        print job[1].enabled
    job[1].set_comment("this 2 is a test")
    jobs.test()



