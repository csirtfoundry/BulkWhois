__all__ = ('BulkWhois')

import telnetlib
import socket
import logging 

class BulkWhois(object):
    """
        Query a list of IP addresses from a bulk whois server. This is an 
        efficient way to query a large number of IP addresses. It sends all
        the IP addresses at once, and receives all whois results together.

        This module takes the approach that you know what you're doing: if
        you have non-IP data in there (such as hostnames), the whois server
        will ignore them and they won't be included in results.

        This class is not designed to be called directly: rather, use one of
        the subclass interfaces to specific bulk whois servers such as 
        bulkwhois.cymru or bulkwhois.shadowserver, which are set to appropriate
        default settings for those services.

        Usage:

        import BulkWhois from bulkwhois

        bw = BulkWhois()
        records = lookup_ips(["192.168.0.1", "10.1.1.1"])

        Args:
            leader: Any text that needs to appear before the bulk whois query
            footer: Any text that needs to appear after the bulk whois query
            server: the hostname of the whois server to use
            port: the whois server port number to connect to
            record_delim: the char to split records received from the server
                          who
            field_delim: the char to split individual fields in each record
            has_results_header: set to True if the whois server send a header
                                line in the results which has no whois data
            fields: a list defining the order of the names of the fields 
                    returned by the server. Used to populate the dict returned.
    """


    leader = ""
    footer = ""
    server = ""
    port = -1
    record_delim = ""
    field_delim = ""
    has_result_header = False
    field_names = []

    def __init__(self, 
                 leader="begin", 
                 footer="end", 
                 server="asn.shadowserver.org", 
                 port="43", 
                 record_delim="\n",
                 field_delim="|",
                 has_result_header=False):
        self.leader = leader
        self.footer = footer
        self.server = server
        self.port = port
        self.record_delim = record_delim
        self.field_delim = field_delim
        self.has_result_header = has_result_header

    def _lookup(self, ip_list):
        """
            Take a list of IP addresses, format them according to the
            whois server spec, connect on the specified port, send the
            formatted data, return the data received.

            Raises:
                IOError on any connection problems
        """
        result = ""
        ip_list = self._filter_ipv4(ip_list)
        query = self._format_list(ip_list)

        try:
            tn = telnetlib.Telnet(self.server, self.port)   
            tn.write(query)
            result = tn.read_all()
            tn.close()
        except socket.gaierror as se:
            raise IOError("Couldn't connect to %s:%s" % (self.server, 
                                                         self.port))
        except EOFError as ee:
            raise IOError("Server dropped connection")

        return result

    def lookup_ips_raw(self, ip_list):
        """
            Get the raw output returned by the whois server as a string.
        """
        return self._lookup(ip_list)

    def lookup_ips(self, ip_list):
        """
            Return a dict of dicts indexed by IP address with whois 
            results.

            Ensure that the "ip" field exists in the field_names array in the
            position of the IP address.

            Args:
                ip_list: an array of IP addresses. We don't check that
                the IP addresses are valid: the whois server will not return
                a result for invalid addresses.

            Returns:
                A dict mapping records by IP address. Dict fields are named
                according to the fields_name array.

            Raises:
                ValueError is "ip" field is not set in field_names.
        """

        raw = self._lookup(ip_list)

        records = {}
        ip_index = self.field_names.index("ip")
        
        if "ip" not in self.field_names:
            raise ValueError("You need to include an 'ip' field in the field_names array.")

        for line_num, line in enumerate(raw.split(self.record_delim)):
            # some whois results have a header we'll throw away
            if line_num == 0 and self.has_result_header:
                next

            fields = line.split(self.field_delim)
            # lots of fields space padded
            fields = [field.strip() for field in fields]

            if len(fields) < len(self.field_names):
                # skip this line: malformed, or doesn't match out template
                pass
            else:
                records.setdefault(fields[ip_index], dict(zip(self.field_names, fields)))

        return records

    def _filter_ipv4(self, ip_list):
        clean_ips = []

        for ip in ip_list:
            try:
                socket.inet_pton(socket.AF_INET, ip)
            except socket.error:
                logging.info("'%s' isn't an IPv4 address: ignoring" % str(ip))
            else:
                clean_ips.append(ip)
        return clean_ips



    def _format_list(self, ip_list):
        return self.record_delim.join([self.leader, self.record_delim.join(ip_list), \
               self.footer]) + self.record_delim

 
if __name__ == "__main__":
    lookups = ["201.21.203.254", "203.21.203.254", "130.102.6.192", "192.168.0.10", "203.20.1.2", "200.200.200.200", "8.8.8.8"]
    bw = BulkWhois(leader="begin origin")
    bw.field_names=["ip", "asn", "bgp_prefix", "as_name", "cc", "register", "org_name"]
    print bw.lookup_ips_raw(lookups)
    print bw.lookup_ips(lookups)

    bw2 = BulkWhois(leader="begin\nverbose", server="asn.cymru.com")
    bw2.field_names=["asn", "ip", "bgp_prefix", "cc", "registry", "allocated", "as_name"]
    print bw2.lookup_ips_raw(lookups)
    print bw2.lookup_ips(lookups)


