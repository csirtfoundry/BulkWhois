import nose
from pprint import pprint
from bulkwhois import BulkWhois

def setup_server():
    bw = BulkWhois(leader="begin origin", server='asn.shadowserver.org')
    bw.field_names=["ip", "asn", "bgp_prefix", "as_name", "cc", "register", "org_name"]
    return bw

def test_no_ips():
    ips = []
    bw = setup_server()
    assert(bw.lookup_ips(ips) == {})

def test_invalid_server_name():
    ips = ["1.1.1.1"]
    bad_server = "garbage.invalid"
    bw = setup_server()
    bw.server = bad_server
    try:
        bw.lookup_ips(ips)
    except IOError as e:
        print e
        assert str(e) == "Couldn't connect to %s:%s" % (bad_server, bw.port), e
    except Exception as e2:
        # we shouldn't receive other errors
        assert False, str(e2)

def test_valid_ips():
    ips = ["201.21.203.254", "203.21.203.254", "130.102.6.192", "192.168.0.10", "203.20.1.2", "200.200.200.200", "8.8.8.8"]
    bw = setup_server()
    recs = bw.lookup_ips(ips)
    assert(len(recs.keys()) == len(ips))

def test_invalid_ips():
    # all but one of these will be ignored by whois server, should result in empty set
    # one valid included to ensure we got some result
    ips = ["203.21.203.254", "8", "foo", "400.2.2.2", "www.google.com"]
    bw = setup_server()
    recs = bw.lookup_ips(ips)
    assert len(recs.keys()) == 1, "Received %d records, expected 1" % \
                                  len(recs.keys())
