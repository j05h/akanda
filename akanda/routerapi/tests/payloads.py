sample_root = """Welcome to the Akanda appliance"""


sample_system_interface = """{"interface": {"description": "", "media": "Ethernet autoselect (1000baseT full-duplex,master)", "mtu": 1500, "state": "up", "groups": "egress", "ifname": "ge1", "lladdr": "00:0c:29:e8:f9:2e", "addresses": ["fe80::20c:29ff:fee8:f92e/64", "192.168.229.129/24"]}}"""


sample_system_interfaces = """{"interfaces": [{"description": "", "media": "null", "mtu": 1500, "state": "down", "groups": "enc", "ifname": "ge0", "lladdr": "null", "addresses": []}, {"description": "", "media": "Ethernet autoselect (1000baseT full-duplex,master)", "mtu": 1500, "state": "up", "groups": "egress", "ifname": "ge1", "lladdr": "00:0c:29:e8:f9:2e", "addresses": ["fe80::20c:29ff:fee8:f92e/64", "192.168.229.129/24"]}, {"description": "", "media": "Ethernet autoselect (1000baseT full-duplex,master)", "mtu": 1500, "state": "up", "groups": [], "ifname": "ge2", "lladdr": "00:0c:29:e8:f9:38", "addresses": ["192.168.57.101/24", "fe80::20c:29ff:fee8:f938/64"]}]}"""

sample_firewall_rules = """pass all flags S/SA block drop in on ! lo0 proto tcp from any to any port 6000:6010"""


sample_pfctl_sr = """
pass all flags S/SA
block drop in on ! lo0 proto tcp from any to any port 6000:6010
"""


sample_pfctl_ss = """
all tcp 192.168.229.129:22 <- 192.168.229.1:52130       ESTABLISHED:ESTABLISHED
all udp 192.168.229.255:17500 <- 192.168.229.1:17500       NO_TRAFFIC:SINGLE
all udp 172.16.5.255:17500 <- 172.16.5.1:17500       NO_TRAFFIC:SINGLE
"""


sample_pfctl_si = """
Status: Enabled for 0 days 01:57:48              Debug: err

State Table                          Total             Rate
  current entries                        4
  searches                            5638            0.8/s
  inserts                               86            0.0/s
  removals                              82            0.0/s
Counters
  match                                 86            0.0/s
  bad-offset                             0            0.0/s
  fragment                               0            0.0/s
  short                                  0            0.0/s
  normalize                              0            0.0/s
  memory                                 0            0.0/s
  bad-timestamp                          0            0.0/s
  congestion                             0            0.0/s
  ip-option                              0            0.0/s
  proto-cksum                            0            0.0/s
  state-mismatch                         0            0.0/s
  state-insert                           0            0.0/s
  state-limit                            0            0.0/s
  src-limit                              0            0.0/s
  synproxy                               0            0.0/s
"""


sample_pfctl_st = """
tcp.first                   120s
tcp.opening                  30s
tcp.established           86400s
tcp.closing                 900s
tcp.finwait                  45s
tcp.closed                   90s
tcp.tsdiff                   30s
udp.first                    60s
udp.single                   30s
udp.multiple                 60s
icmp.first                   20s
icmp.error                   10s
other.first                  60s
other.single                 30s
other.multiple               60s
frag                         30s
interval                     10s
adaptive.start             6000 states
adaptive.end              12000 states
src.track                     0s
"""


sample_pfctl_sm = """
states        hard limit    10000
src-nodes     hard limit    10000
frags         hard limit     5000
tables        hard limit     1000
table-entries hard limit   200000
"""


sample_pfctl_sl = """
"""


sample_pfctl_sA = """
"""


sample_pfctl_sS = """
"""


sample_pfctl_sT = """
"""
