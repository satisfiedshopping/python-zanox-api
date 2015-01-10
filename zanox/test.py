# encoding: utf-8

import unittest2 as unittest

from .apis import PublisherApi


class ExtractDestinationUrlTest(unittest.TestCase):

    def setUp(self):
        self.api = PublisherApi(connect_id='802B8BF4AE99EBE00F41', secret_key='fa4c0c2020Aa4c+ab9Ea0ec8d39E06/df2c5aa44')

    def test_normal(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25738162C98353673&amp;ULP=[[http://www.manfield.com/product/09111600?channel_code=74&amp;product_code=62164779&amp;utm_campaign=sales&amp;utm_content=prfeed&amp;utm_medium=affiliate&amp;utm_source=Zanox]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.manfield.com/product/09111600'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)

    def test_without_http(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25695976C44878398&amp;ULP=[[www.hardloopschoenencenter.nl/product/434398]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.hardloopschoenencenter.nl/product/434398/nike-storm-slim-waistpack.html'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)

    def test_with_extra_url(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25712131C50023437&amp;ULP=[[http://adfarm.mediaplex.com/ad/ck/25522-185146-14530-4?destination=Productfeed&amp;mpro=http%3A%2F%2Fwww.esprit.nl%2Fkids%2Fbaby-0-2-jaar%2Fbaby-boys%2Fjeans-broeken%2Fjeans-%26-broeken-074EEBB008_406%3Fcamp%3DNL_IC_ZX_AF_20_001]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.esprit.nl/kids/baby-0-2-jaar/baby-boys/jeans-broeken/jeans-&-broeken-074EEBB008_406'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)

    def test_path_only(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25738046C20244849&amp;ULP=[[cd/this-et-al/baby-machine/8609983.html?affil=zanox]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.zavvi.nl/cd/this-et-al/baby-machine/8609983.html'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)

    def test_path_only2(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25719026C47878862&amp;ULP=[[/4+paar+verschillende+katoenrijke+sokken/P22323198,nl_NL,pd.html]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.marksandspencer.eu/4-paar-verschillende-katoenrijke-sokken/P22323198,nl_NL,pd.html'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)

    def test_id_only(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25737964C93517905&amp;ULP=[[031662900?channel_code=74&amp;product_code=71491142&amp;utm_campaign=sales&amp;utm_content=prfeed&amp;utm_medium=affiliate&amp;utm_source=Zanox]]&amp;zpar9=[[9010F8C4AD9955DBDC9F]]'
        destination_url = 'http://www.scapino.nl/product/031662900'
        self.assertEqual(self.api.extract_destination_url_from_tracking_url(tracking_url, clean=True), destination_url)


class GenerateTrackingUrlTest(unittest.TestCase):

    def setUp(self):
        self.api = PublisherApi(connect_id='802B8BF4AE99EBE00F41', secret_key='fa4c0c2020Aa4c+ab9Ea0ec8d39E06/df2c5aa44')

    def test_use_deeplink_api(self):
        tracking_url = 'http://ad.zanox.com/ppv/?25739309C31436867&amp;ULP=[[http://www.bullsandbirds.com/schoen-louis03-camel-7354-p-3035.html]]&amp;zpar9=[[802B8BF4AE99EBE00F41]]'
        destination_url = 'http://www.bullsandbirds.com/schoen-louis03-camel-7354-p-3035.html'
        self.assertEqual(self.api.get_tracking_url(destination_url, adspace_id='897026'), tracking_url)

    def test_generate_with_format(self):
        tracking_url = 'http://ad.zanox.com/ppc/?25695976C44878398&ULP=[[http://www.hardloopschoenencenter.nl/product/434398/nike-storm-slim-waistpack.html]]&zpar9=[[802B8BF4AE99EBE00F41]]'
        destination_url = 'http://www.hardloopschoenencenter.nl/product/434398/nike-storm-slim-waistpack.html'
        self.assertEqual(self.api.get_tracking_url(destination_url, merchant_id='25695976C44878398', url_type='ppc', use_deeplink_generator=False), tracking_url)




