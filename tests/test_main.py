from pyflow.testing import WorklowTestCase

from main import main


class TestFiatMain(WorklowTestCase):
    def test_run(self):
        envs = {
            "CRYPTO": "bitcoin",
            "FIAT": "USD",
        }

        args = ["100", "ARS"]

        workflow = self.workflow(**envs)
        feedback = self.run_workflow(workflow, main, *args)

        ars, usd, btc = feedback["items"]

        self.assertEqual(ars["title"], "Argentine Peso")
        self.assertEqual(ars["subtitle"], "ARS / fiat")
        self.assertEqual(ars["icon"]["path"], "./img/fiat/ARS.png")
        self.assertFalse(ars["valid"])

        self.assertTrue(usd["title"].endswith("USD"))
        self.assertTrue(usd["subtitle"].startswith("[fiat] 1 ARS"))
        self.assertTrue(usd["subtitle"].endswith("USD"))

        self.assertTrue(btc["title"].endswith("BTC"))
        self.assertTrue(btc["subtitle"].startswith("[crypto] 1 ARS"))
        self.assertTrue(btc["subtitle"].endswith("BTC"))

    def test_crypto(self):
        envs = {
            "CRYPTO": "algorand",
            "FIAT": "USD",
        }

        args = ["100", "ADA"]

        workflow = self.workflow(**envs)
        feedback = self.run_workflow(workflow, main, *args)

        ada, usd, algo = feedback["items"]

        self.assertEqual(ada["title"], "Cardano")
        self.assertEqual(ada["subtitle"], "ADA / crypto")
        self.assertEqual(ada["icon"]["path"], "/tmp/alfred-currency-converter/cardano.png")
        self.assertFalse(ada["valid"])

        self.assertTrue(usd["title"].endswith("USD"))
        self.assertTrue(usd["subtitle"].startswith("[fiat] 1 ADA"))
        self.assertTrue(usd["subtitle"].endswith("USD"))

        self.assertTrue(algo["title"].endswith("ALGO"))
        self.assertTrue(algo["subtitle"].startswith("[crypto] 1 ADA"))
        self.assertTrue(algo["subtitle"].endswith("ALGO"))