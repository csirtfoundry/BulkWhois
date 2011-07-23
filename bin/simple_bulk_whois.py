#!/usr/bin/env python

from bulkwhois.cymru import BulkWhoisCymru

bulk_whois = BulkWhoisCymru()
records = bulk_whois.lookup_ips(["212.58.246.91", "203.2.218.214"])

for record in records:
    print "\t".join([records[record]["ip"], records[record]["asn"], records[record]["as_name"], records[record]["cc"]])
