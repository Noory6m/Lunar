import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen
import app

class HorizonsTests(unittest.TestCase):
    def query(self,**overrides):
        p=dict(lat='-89.46316',lon='-137.48955',alt='1.9457',start='2026-11-14T00:00Z',end='2026-11-15T00:00Z',step='60');p.update(overrides);return urlencode(p)
    def test_valid_lunar_observer(self):
        p=app.validate_query(self.query());url=app.query_url('10',p)
        self.assertIn('coord%40301',url);self.assertIn('222.51045',url)
        self.assertEqual(p['start'].utcoffset().total_seconds(),0)
    def test_rejects_invalid_and_unbounded_requests(self):
        for changes in ({'lat':'nan'},{'step':'0'},{'step':'60.1'},{'end':'2026-11-13'},{'end':'2027-11-14'},{'lat':'91'},{'start':'bad'},{'step':'10','end':'2026-12-14'}):
            with self.subTest(changes=changes),self.assertRaises(app.InputError):app.validate_query(self.query(**changes))
    def test_actual_horizons_column_order(self):
        raw='header\n$$SOE\n 2026-Nov-14 00:00,*, ,264.092758292,1.501419941,1942.009,147784060.74,0.0,\n$$EOE\nfooter'
        rows=app.parse_table(raw);self.assertEqual(rows[0]['time'],1794614400000);self.assertAlmostEqual(rows[0]['el'],1.501419941);self.assertEqual(rows[0]['distanceKm'],147784060.74)
    def test_unavailable_values_are_not_silently_zero(self):
        with self.assertRaises(RuntimeError):app.parse_table('$$SOE\n2026-Nov-14 00:00,*, ,n.a.,0,0,0,\n$$EOE')
        with self.assertRaises(RuntimeError):app.parse_table('no table')

class WebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.base=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
    def test_no_account_needed(self):
        with urlopen(self.base+'/api/health') as r:self.assertFalse(json.load(r)['auth_required'])
        with urlopen(self.base+'/') as r:
            html=r.read().decode();self.assertIn('3D Moon',html);self.assertNotIn('fonts.googleapis',html);self.assertIn("connect-src 'self'",r.headers['Content-Security-Policy'])
    def test_browser_modules_have_javascript_mime(self):
        for path in ('/mission.js','/globe.js','/analysis-worker.js','/assets/three.module.js'):
            with self.subTest(path=path),urlopen(self.base+path) as r:self.assertIn('javascript',r.headers['Content-Type'])
    def test_bad_api_query_does_not_call_nasa(self):
        with self.assertRaises(HTTPError) as cm:urlopen(self.base+'/api/ephemeris?lat=nan')
        self.assertEqual(cm.exception.code,400)
    def test_real_bundled_data_and_example(self):
        for name in ('globe-dem.json','mission-terrain.json','regional-terrain.json'):
            d=json.loads((app.FRONTEND/'assets'/name).read_text());self.assertEqual(len(d['z']),d['rows']*d['cols']);self.assertTrue(all(isinstance(n,(float,int)) for n in d['z']))
        d=json.loads((app.FRONTEND/'assets/horizons-example.json').read_text());self.assertEqual(len(d['sun']),len(d['earth']));self.assertEqual(len(d['sun']),169);self.assertEqual(d['sun'][0]['time'],1794614400000)

if __name__=='__main__':unittest.main()
