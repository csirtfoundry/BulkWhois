===========
BulkWhois
===========

BulkWhois provides a simple interface to several bulk whois servers. This 
allows you to look up the ASNs, AS names, country codes, and other assorted
information very efficiently for a large number of IP addresses.

Currently implemented bulk whois servers are:
    Cymru: BulkWhoisCymru
    Shadowserver: BulkWhoisShadowserver

Note that these whois servers generally only accept IPv4 IP addresses, not 
hostnames. IPv6 support is not widely supported by bulk whois servers at
present, but will add in support once this becomes available.

So, it's up to the caller to convert hostnames to IP addresses first. 
Anything which isn't an IPv4 address generates a warning and is dropped 
before sending to the whois server.


Usage::

    #!/usr/bin/env python

    from bulkwhois.shadowserver import BulkWhoisShadowserver

    bulk_whois = BulkWhoisShadowserver()
    records = bulk_whois.lookup_ips(["212.58.246.91", "203.2.218.214"])

    for record in records:
        print "\t".join([records[record]["ip"], records[record]["asn"], 
                        records[record]["as_name"], records[record]["cc"]])
   
Installation
============

python setup.py install

Implementation
==============

Current implementation assumes accessing a bulk whois server with a telnet-like
interface. Generally, input takes the form of:

begin
192.168.0.1
192.168.0.2
end

Note that different bulk whois servers return different data, so better to 
choose one you're happy with first and stick with it to keep things 
consistent.

For example, using different modules the sample code returns this:

BulkWhoisShadowServer

203.2.218.214   9342    ABCNET-AS   AU
212.58.246.91   2818    BBC UK

BulkWhoisCymru

203.2.218.214   9342    ABCNET-AS-AP Australian Broadcasting Commission AU
212.58.246.91   2818    BBC BBC Internet Services, UK   GB

Further information:

http://www.shadowserver.org/wiki/pmwiki.php/Services/IP-BGP
http://www.team-cymru.org/Services/ip-to-asn.html
