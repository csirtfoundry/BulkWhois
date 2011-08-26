__all__ = ('BulkWhoisCymru')

from bulkwhois import BulkWhois

class BulkWhoisCymru(BulkWhois):

    """
        An interface to the Shadowserver bulk whois service.

        Usage:

        from bulkwhois.shadowserver import BulkWhoisShadowserver

        bw = BulkWhoisShadowserver()
        bw.lookup_ips(["69.12.38.242", "212.58.241.131"])) 

        returns:
            {
                '212.58.241.131': 
                    {
                        'allocated': '1999-10-08',
                        'as_name': 'TELIANET TeliaNet Global Network',
                        'asn': '1299',
                        'bgp_prefix': '212.58.224.0/19',
                        'cc': 'GB',
                        'ip': '212.58.241.131',
                        'registry': 'ripencc'
                    },
                '69.12.38.242': 
                    {
                        'allocated': '2002-12-04',
                        'as_name': 'LEVEL3 Level 3 Communications',
                        'asn': '3356',
                        'bgp_prefix': '69.12.0.0/17',
                        'cc': 'US',
                        'ip': '69.12.38.242',
                        'registry': 'arin'
                    }
             }
    """

    def __init__(self, **kwargs):
            super(BulkWhoisCymru, self).__init__(**kwargs)
            self.server = "whois.cymru.com"
            self.leader = "begin\nverbose"
            self.has_result_header = True
            self.field_names=["asn", "ip", "bgp_prefix", "cc", "registry", "allocated", "as_name"]

if __name__ == "__main__":
    lookups = ["201.21.203.254", "203.21.203.254", "130.102.6.192", "192.168.0.10", "203.20.1.2", "200.200.200.200", "8.8.8.8"]
    bw = BulkWhoisCymru()
    print "Server: " + bw.server
    print "Port: " + bw.port
    print "Leader: " + bw.leader
    print "Footer: " + bw.footer
    print bw.lookup_ips_raw(lookups)
    print bw.lookup_ips(lookups)

