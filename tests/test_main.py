from pyflow.testing import WorklowTestCase

from main import main


class TestMain(WorklowTestCase):
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
        self.assertIn("(ARS blackmarket)", usd["mods"]["alt"]["subtitle"])
        self.assertIn("(ARS blackmarket)", usd["mods"]["cmd"]["subtitle"])

        self.assertTrue(btc["title"].endswith("BTC"))
        self.assertTrue(btc["subtitle"].startswith("[crypto] 1 ARS"))
        self.assertTrue(btc["subtitle"].endswith("BTC"))
        self.assertIn("(ARS blackmarket)", usd["mods"]["alt"]["subtitle"])
        self.assertIn("(ARS blackmarket)", btc["mods"]["cmd"]["subtitle"])
