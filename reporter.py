import psutil
import socket
from prometheus_client import Gauge,start_http_server
from time import sleep

metrics_list = Gauge('metrics', 'descript', ['ip','stat'])
host_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

class Reporter():
    def __init__(self):
        self.cpu_stat_list = []
        self.mem_stat_list = []
        self.disk_usage_list = []
        self.disk_io_list = []
        self.net_list = []
        self.net_io_list = []
        self.process_info_list = []

    def ClearAll(self):
        self.__init__()

    def CollectCpuStat(self):
        cpu_stat_l = psutil.cpu_percent(interval=1, percpu=True)
        i = 0
        for cpu in cpu_stat_l:
            i = i + 1
            cpu_name = "cpu_" + str(i)
            cpu_s = {}
            cpu_s[cpu_name] = cpu
            self.cpu_stat_list.append(cpu_s)

    def CollectMemStat(self):
        mem = psutil.virtual_memory()
        mem_stat = {}
        mem_stat['mem_total'] = mem.total
        mem_stat['mem_available'] = mem.available
        mem_stat['mem_percent'] = mem.percent
        mem_stat['mem_used'] = mem.used
        mem_stat['mem_free'] = mem.free
        mem_stat['mem_active'] = mem.active
        mem_stat['mem_inactive'] = mem.inactive
        #mem_stat['wired'] = mem.wired
        self.mem_stat_list.append(mem_stat)

    def CollectDiskUsage(self):
        disk_usage =  psutil.disk_usage('/')
        disk_usage_stat = {}
        disk_usage_stat['disk_total'] = disk_usage.total
        disk_usage_stat['disk_used'] = disk_usage.used
        disk_usage_stat['disk_free'] = disk_usage.free
        disk_usage_stat['disk_percent'] = disk_usage.percent
        self.disk_usage_list.append(disk_usage_stat)


    def CollectDiskIo(self):
        disk_io_stat = {}
        disk_io = psutil.disk_io_counters()
        disk_io_stat['disk_io_read_count'] = disk_io.read_count
        disk_io_stat['disk_io_write_count'] = disk_io.write_count
        disk_io_stat['disk_io_read_bytes'] = disk_io.read_bytes
        disk_io_stat['disk_io_write_bytes'] = disk_io.write_bytes
        disk_io_stat['disk_io_read_time'] = disk_io.read_time
        disk_io_stat['disk_io_write_time'] = disk_io.write_time
        self.disk_io_list.append(disk_io_stat)

    def CollectNetIo(self):
        net_io = psutil.net_io_counters()
        net_io_stat = {}
        net_io_stat['net_io_bytes_sent'] = net_io.bytes_sent
        net_io_stat['net_io_bytes_recv'] = net_io.bytes_recv
        net_io_stat['net_io_packets_sent'] = net_io.packets_sent
        net_io_stat['net_io_packets_recv'] = net_io.packets_recv
        net_io_stat['net_io_errin'] = net_io.errin
        net_io_stat['net_io_errout'] = net_io.errout
        net_io_stat['net_io_dropin'] = net_io.dropin
        net_io_stat['net_io_dropout'] = net_io.dropout
        self.net_io_list.append(net_io_stat)

        net_if_addrs = psutil.net_if_addrs()
        for value in net_if_addrs.iteritems() :
            addr_stat = {}
            addr_name = value[0]
            snicaddrs = value[1]
            for snic in snicaddrs:
                if snic.family == 2:
                    ip = snic.address
            addr_stat[addr_name] = ip
            self.net_list.append(addr_stat)

    def CollectPids(self):
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            process_info = {}
            process_info['process_name'] = p.name()
            process_info['process_username'] = p.username()
            process_info['process_cpu_user'] = p.cpu_times().user
            process_info['process_cpu_sys'] = p.cpu_times().system
            process_info['process_mem_rss'] = p.memory_info().rss
            self.process_info_list.append(process_info)

    def DebugString(self):
        print(self.cpu_stat_list)
        print(self.mem_stat_list)
        print(self.net_list)
        for process_info in self.process_info_list:
            print(process_info)
        print(self.net_io_list)
        print(self.disk_io_list)
        print(self.disk_usage_list)

    def SysColleter(self):
        self.ClearAll()
        self.CollectCpuStat()
        self.CollectMemStat()
        self.CollectDiskUsage()
        self.CollectDiskIo()
        self.CollectNetIo()
        #self.CollectPids()

    def MetricsReport(self):
        for list_info in [self.cpu_stat_list, self.mem_stat_list, self.net_io_list, self.disk_io_list, self.disk_usage_list]:
            for info in list_info:
                for k,v in info.iteritems():
                    print("{} => {}".format(k, v))
                    metrics_list.labels(ip = host_ip, stat = k).set(v)

if __name__ == '__main__':
    start_http_server(9999)
    while True:
        reporter = Reporter()
        reporter.SysColleter()
        #reporter.DebugString()
        reporter.MetricsReport()
        sleep(10)
