__all__ = ('BulkWhoisShadowserver')

import socket
from bulkwhois import BulkWhois

class BulkWhoisShadowserver(BulkWhois):

    """
        An interface to the Shadowserver bulk whois service.

        Usage:

        from bulkwhois.shadowserver import BulkWhoisShadowserver

        bw = BulkWhoisShadowserver()
        bw.lookup_ips(["69.12.38.242", "212.58.241.131"])) 
        
        returns:

        {
            '10.1.1.1': {'as_name': '',
                'asn': '',
                'bgp_prefix': '',
                'cc': '-',
                'ip': '10.1.1.1',
                'org_name': 'PRIVATE IP ADDRESS LAN',
                'register': '-'},
            '192.168.0.1': {'as_name': '',
                'asn': '',
                'bgp_prefix': '',
                'cc': '-',
                'ip': '192.168.0.1',
                'org_name': 'PRIVATE IP ADDRESS LAN',
                'register': '-'}
        }

    """

    def __init__(self, **kwargs):
            super(BulkWhoisShadowserver, self).__init__(**kwargs)
            self.server = "asn.shadowserver.org"
            self.leader = "begin origin"
            self.field_names=["ip", "asn", "bgp_prefix", "as_name", "cc",
                              "register", "org_name"]

    # TODO: shadowserver whois returns nothing if there's one invalid IP addy,
    #       unlike Cymru. Probably need to add check function - that's annoying

if __name__ == "__main__":
    lookups = ["201.21.203.254", "203.21.203.254", "130.102.6.192", "192.168.0.10", "203.20.1.2", "200.200.200.200", "8.8.8.8"]
    bw = BulkWhoisShadowserver()
    print "Server: " + bw.server
    print "Port: " + bw.port
    print "Leader: " + bw.leader
    print "Footer: " + bw.footer
    print bw.lookup_ips_raw(lookups)
    print bw.lookup_ips(lookups)

