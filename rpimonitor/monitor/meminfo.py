"""Process /proc/meminfo """

def _parse_proc_meminfo_line(line):
    name, value, unit = line.split()
    name, value, unit = name[:-1], int(value), unit.lower()
    if unit == "kb":
        value *= 1024
    elif unit == "mb":
        value *= 1024 * 1024
    elif unit == "gb":
        value *= 1024 * 1024 * 1024
    return name, value

def parse_proc_meminfo_lines(lines):
    """Parse the lines returned from /proc/meminfo"""
    results = {}
    for line in lines:
        name, value = _parse_proc_meminfo_line(line)
        results[name] = value
    return results

def parse_proc_meminfo_lines2(lines):
    """Parse the lines returned from /proc/meminfo"""
    return dict(_parse_proc_meminfo_line(line) for line in lines)

def sample_proc_meminfo():
    """Takes a reading from /proc/stat and returns the parsed data"""
    with open('/proc/meminfo') as f:
        return parse_proc_meminfo_lines2(f.readlines())

if __name__ == "__main__":
    meminfo = sample_proc_meminfo()
    print(meminfo)
    print(meminfo['MemTotal'] / (1024 * 1024))
    
    