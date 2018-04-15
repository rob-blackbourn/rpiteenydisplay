"""Routines to get information from /proc/stat on a Raspberry Pi 3 B+ running Raspbian Stretch
"""

class CpuStat(object):
    """ Represents the cpu data from /proc/stat
    """

    def __init__(self, user, nice, system, idle, iowait, irq, softirq, steal, quest, quest_nice):
        self.user = user
        self.nice = nice
        self.system = system
        self.idle = idle
        self.iowait = iowait
        self.irq = irq
        self.softirq = softirq
        self.steal = steal
        self.quest = quest
        self.quest_nice = quest_nice

    @property
    def busy_time(self):
        """The amount of time the CPOU ihas been busy since the last boot"""
        return self.user + self.nice + self.system + self.irq + self.softirq + self.steal

    @property
    def idle_time(self):
        """The amount of time the cpu has been idle since th last boot"""
        return self.idle + self.iowait

    @property
    def usage(self):
        """The CPU usage as a ratio of busy time to total time"""
        return self.busy_time / (self.busy_time + self.idle_time)

    def __sub__(self, other):
        """Calculate the change between two readings"""
        return CpuStat(
            self.user - other.user,
            self.nice - other.nice,
            self.system - other.system,
            self.idle - other.idle,
            self.iowait - other.iowait,
            self.irq - other.irq,
            self.softirq - other.softirq,
            self.steal - other.steal,
            self.quest - other.quest,
            self.quest_nice - other.quest_nice)

def parse_proc_stat_lines(lines):
    """Parses the lines of /proc/stat"""
    stats = {}
    for line in map(lambda x: x.strip(), lines):
        items = line.split(' ')
        name, values = items[0], items[1:]
        if name.startswith('cpu'):
            if name == "cpu":
                stats[name] = CpuStat(*list(map(int, values[1:])))
            else:
                if 'cores' not in stats:
                    stats['cores'] = {}
                cpu_id = int(name[3:])
                stats['cores'][cpu_id] = CpuStat(*list(map(int, values)))
        elif name in ['ctxt', 'btime', 'processes', 'procs_running', 'procs_blocked']:
            stats[name] = int(values[0])
        else:
            stats[name] = list(map(int, values))
    return stats

def sample_proc_stat():
    """Takes a reading from /proc/stat and returns the parsed data"""
    with open('/proc/stat') as fp:
        return parse_proc_stat_lines(fp.readlines())
