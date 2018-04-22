"""Process /proc/meminfo """

import aiofiles

class MemInfo(object):
    """Methods for interacting with /proc/meminfo"""

    def __init__(self, values):
        self.values = values

    @classmethod
    def _parse_line(cls, line):
        name, value, _ = line.split()
        return name[:-1], int(value)

    @classmethod
    def parse_lines(cls, lines):
        """Parse the lines returned from /proc/meminfo"""
        return MemInfo(dict(cls._parse_line(line) for line in lines))

    @classmethod
    def sample(cls):
        """Takes a reading from /proc/stat and returns the parsed data"""
        with open('/proc/meminfo') as f:
            return cls.parse_lines(f.readlines())

    @classmethod
    async def sample_async(cls):
        """Takes a reading from /proc/stat and returns the parsed data"""
        async with aiofiles.open('/proc/meminfo') as file_ptr:
            lines = await file_ptr.readlines()
            return cls.parse_lines(lines)

    @property
    def total(self):
        """Total installed memory (MemTotal and SwapTotal in
              /proc/meminfo)"""
        return self.mem_total + self.swap_total

    @property
    def mem_total(self):
        """Total physical memory (MemTotal in /proc/meminfo)"""
        return self.values['MemTotal']

    @property
    def swap_total(self):
        """Total swap memory (SwapTotal in /proc/meminfo)"""
        return self.values['SwapTotal']
        
    @property
    def used(self):
        """Used memory (calculated as total - free - buffers - cache)"""
        return self.total - self.free - self.buffers - self.cache
        
    @property
    def mem_used(self):
        """Used physical memory (calculated as mem_total - mem_free - buffers - cache)"""
        return self.mem_total - self.mem_free - self.buffers - self.cache
        
    @property
    def swap_used(self):
        """Used swap (calculated as total - free - buffers - cache)"""
        return self.swap_total - self.swap_free

    @property
    def free(self):
        """Unused memory (MemFree and SwapFree in /proc/meminfo)"""
        return self.values['MemFree'] + self.values['SwapFree']

    @property
    def mem_free(self):
        """Unused physical memory (MemFree in /proc/meminfo)"""
        return self.values['MemFree']

    @property
    def swap_free(self):
        """Unused swap memory (SwapFree in /proc/meminfo)"""
        return self.values['SwapFree']

    @property
    def shared(self):
        """Memory used (mostly) by tmpfs (Shmem in /proc/meminfo)"""
        return self.values['Shmem']

    @property
    def buffers(self):
        """Memory used by kernel buffers (Buffers in /proc/meminfo)"""
        return self.values['Buffers']

    @property
    def cache(self):
        """Memory used by the page cache and slabs (Cached and SReclaimable
           in /proc/meminfo)"""
        return self.values['Cached'] + self.values['SReclaimable']

    @property
    def available(self):
        """Estimation of how much memory is available for starting new, 
           without swapping (MemAvailable in /proc/meminfo)."""
        return self.values['MemAvailable']

    @property
    def usage(self):
        """Percentyage of all memory used"""
        return self.used / self.total

    @property
    def mem_usage(self):
        """Percentyage of all memory used"""
        return self.mem_used / self.mem_total

    @property
    def swap_usage(self):
        """Percentyage of all memory used"""
        return self.swap_used / self.swap_total

    def __str__(self):
        return f"total: {meminfo.total}, used: {meminfo.used}, free: {meminfo.free}, shared: {self.shared}, buffers: {self.buffers}, cache: {self.cache}, buff/cache: {self.buffers + self.cache} available: {meminfo.available}"

if __name__ == "__main__":
    meminfo = MemInfo.sample()
    print(meminfo)
    print(meminfo.usage)
    print(meminfo.mem_usage)
    print(meminfo.swap_usage)
    
    