# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

from typing import Tuple
from unittest import TestCase

from six import binary_type

from iota import Address, Bundle, BundleHash, Fragment, Hash, ProposedBundle, \
  ProposedTransaction, Tag, Transaction, TransactionHash, TransactionTrytes, \
  TryteString, convert_value_to_standard_unit
from iota.crypto.signing import KeyGenerator
from iota.crypto.types import Seed
from iota.transaction import BundleValidator


class BundleTestCase(TestCase):
  def setUp(self):
    super(BundleTestCase, self).setUp()

    # noinspection SpellCheckingInspection
    self.bundle = Bundle([
      # This transaction does not have a message.
      Transaction(
        signature_message_fragment = Fragment(b''),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999A9PG9A'
            b'XCQANAWGJBTFWEAEQCN9WBZB9BJAIIY9UDLIGFOAA'
          ),

        current_index           = 0,
        last_index              = 7,
        value                   = 0,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # This transaction has something that can't be decoded as a UTF-8
      # sequence.
      Transaction(
        signature_message_fragment =
          Fragment(b'OHCFVELH9GYEMHCF9GPHBGIEWHZFU'),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999HAA9UA'
            b'MHCGKEUGYFUBIARAXBFASGLCHCBEVGTBDCSAEBTBM'
          ),

        current_index           = 1,
        last_index              = 7,
        value                   = 10,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # This transaction has a message that fits into a single
      # fragment.
      Transaction(
        signature_message_fragment =
          Fragment.from_string('Hello, world!'),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999D99HEA'
            b'M9XADCPFJDFANCIHR9OBDHTAGGE9TGCI9EO9ZCRBN'
          ),

        current_index           = 2,
        last_index              = 7,
        value                   = 20,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # This transaction has a message that spans multiple fragments.
      Transaction(
        signature_message_fragment =
          Fragment(
            b'J9GAQBCDCDSCEAADCDFDBDXCBDVCQAGAEAGDPCXCSCEANBTCTCDDEACCWCCDIDVC'
            b'WCHDEAPCHDEA9DPCGDHDSAJ9GAOBFDSASASAEAQBCDCDSCEAADCDFDBDXCBDVCQA'
            b'EAYBEANBTCTCDDEACCWCCDIDVCWCHDQAGAEAGDPCXCSCEAVBCDCDBDEDIDPCKD9D'
            b'EABDTCFDJDCDIDGD9DMDSAJ9EAEAGANBCDEAMDCDIDEAWCPCJDTCSASASAEATCFD'
            b'QAEAHDWCPCHDEAXCGDSASASAGAJ9GASASASAEAPCBDEAPCBDGDKDTCFDEAUCCDFD'
            b'EAMDCDIDIBGAEAXCBDHDTCFDFDIDDDHDTCSCEANBTCTCDDEACCWCCDIDVCWCHDEA'
            b'ADPCYCTCGDHDXCRCPC9D9DMDSAEAGAHCTCGDSAEASBEAWCPCJDTCSAGAJ9CCWCTC'
            b'EAHDKDCDEAADTCBDEAGDWCXCJDTCFDTCSCEAKDXCHDWCEATCLDDDTCRCHDPCBDRC'
            b'MDSAEACCWCTCXCFDEAKDPCXCHDXCBDVCEAWCPCSCEABDCDHDEAQCTCTCBDEAXCBD'
            b'EAJDPCXCBDSAJ9GACCWCTCFDTCEAFDTCPC9D9DMDEAXCGDEACDBDTCIBGAEAQCFD'
            b'TCPCHDWCTCSCEAZBWCCDIDRCWCVCSAJ9GACCWCTCFDTCEAFDTCPC9D9DMDEAXCGD'
            b'EACDBDTCQAGAEARCCDBDUCXCFDADTCSCEANBTCTCDDEACCWCCDIDVCWCHDSAJ9GA'
            b'CCCDEAOBJDTCFDMDHDWCXCBDVCIBEACCCDEAHDWCTCEAVCFDTCPCHDEA9CIDTCGD'
            b'HDXCCDBDEACDUCEAVBXCUCTCQAEAHDWCTCEADCBDXCJDTCFDGDTCEAPCBDSCEAOB'
            b'JDTCFDMDHDWCXCBDVCIBGAJ9GAHCTCGDSAGAJ9LBCDHDWCEACDUCEAHDWCTCEAAD'
            b'TCBDEAWCPCSCEAQCTCTCBDEAHDFDPCXCBDTCSCEAUCCDFDEAHDWCXCGDEAADCDAD'
            b'TCBDHDEBEAHDWCTCXCFDEA9DXCJDTCGDEAWCPCSCEAQCTCTCBDEAPCJ9EAEADDFD'
            b'TCDDPCFDPCHDXCCDBDEAUCCDFDEAXCHDEBEAHDWCTCMDEAWCPCSCEAQCTCTCBDEA'
            b'GDTC9DTCRCHDTCSCEAPCHDEAQCXCFDHDWCEAPCGDEAHDWCCDGDTCEAKDWCCDEAKD'
            b'CDID9DSCJ9EAEAKDXCHDBDTCGDGDEAHDWCTCEAPCBDGDKDTCFDEBEAQCIDHDEATC'
            b'JDTCBDEAGDCDEAHDWCTCMDEAUCCDIDBDSCEAHDWCTCADGDTC9DJDTCGDEAVCPCGD'
            b'DDXCBDVCEAPCBDSCEAGDEDIDXCFDADXCBDVCJ9EAEA9DXCZCTCEATCLDRCXCHDTC'
            b'SCEARCWCXC9DSCFDTCBDSAJ9GAKBBDSCEAMDCDIDLAFDTCEAFDTCPCSCMDEAHDCD'
            b'EAVCXCJDTCEAXCHDEAHDCDEAIDGDIBGAEAIDFDVCTCSCEAVBCDCDBDEDIDPCKD9D'
            b'SAJ9GASBEAPCADSAGAJ9GAXBCDKDIBGAJ9GAXBCDKDQAGAEAGDPCXCSCEANBTCTC'
            b'DDEACCWCCDIDVCWCHDSAJ9CCWCTCMDEAQCCDHDWCEA9DXCRCZCTCSCEAHDWCTCXC'
            b'FDEASCFDMDEA9DXCDDGDSAJ9GACCWCCDIDVCWCEASBEASCCDBDLAHDEAHDWCXCBD'
            b'ZCQAGAEAPCSCSCTCSCEANBTCTCDDEACCWCCDIDVCWCHDQAEAGAHDWCPCHDEAMDCD'
            b'IDLAFDTCEAVCCDXCBDVCEAHDCDEA9DXCZCTCEAXCHDSAGAJ9GANBCDTCGDBDLAHD'
            b'EAADPCHDHDTCFDQAGAEAGDPCXCSCEAZBWCCDIDRCWCVCSAEAGAFCTCEAADIDGDHD'
            b'EAZCBDCDKDEAXCHDFAEAXBCDKDFAGAJ9GAXBCDKDIBGAEATCBDEDIDXCFDTCSCEA'
            b'NBTCTCDDEACCWCCDIDVCWCHDSAJ9GAHCTCGDFAEAXBCDKDFAGAJ9GAKB9D9DEAFD'
            b'XCVCWCHDQAGAEAGDPCXCSCEAHDWCTCEARCCDADDDIDHDTCFDEAPCBDSCEAGDTCHD'
            b'HD9DTCSCEAXCBDHDCDEAGDXC9DTCBDRCTCEAPCVCPCXCBDSAJ9EAEACCWCTCEAHD'
            b'KDCDEAADTCB'
          ),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999A9PG9A'
            b'XCQANAWGJBTFWEAEQCN9WBZB9BJAIIY9UDLIGFOAA'
          ),

        current_index           = 3,
        last_index              = 7,
        value                   = 30,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      Transaction(
        signature_message_fragment =
          Fragment(
            b'DEAUCXCSCVCTCHDTCSCSAEACCWCTCEAHDTCBDGDXCCDBDEAKDPCGDEAIDBDQCTCP'
            b'CFDPCQC9DTCSAJ9GAHCCDIDLAFDTCEAFDTCPC9D9DMDEABDCDHDEAVCCDXCBDVCE'
            b'AHDCDEA9DXCZCTCEAXCHDQAGAEACDQCGDTCFDJDTCSCEANBTCTCDDEACCWCCDIDV'
            b'CWCHDSAJ9GACCTC9D9DEAIDGDFAGAJ9GAKB9D9DEAFDXCVCWCHDQAGAEAGDPCXCS'
            b'CEANBTCTCDDEACCWCCDIDVCWCHDSAEAGACCWCTCEAKBBDGDKDTCFDEAHDCDEAHDW'
            b'CTCEAQBFDTCPCHDEA9CIDTCGDHDXCCDBDSASASAGAJ9GAHCTCGDIBGAJ9GAYBUCE'
            b'AVBXCUCTCQAEAHDWCTCEADCBDXCJDTCFDGDTCEAPCBDSCEAOBJDTCFDMDHDWCXCB'
            b'DVCSASASAGAEAGDPCXCSCEANBTCTCDDEACCWCCDIDVCWCHDSAJ9GAHCTCGDIBIBG'
            b'AJ9GASBGDSASASAGAJ9GAHCTCGDIBFAGAJ9GAPBCDFDHDMDRAHDKDCDQAGAEAGDP'
            b'CXCSCEANBTCTCDDEACCWCCDIDVCWCHDQAEAKDXCHDWCEAXCBDUCXCBDXCHDTCEAA'
            b'DPCYCTCGDHDMDEAPCBDSCEARCPC9DADSAJ9EAEAEAEAEAEAEAEA'
          ),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999A9PG9A'
            b'XCQANAWGJBTFWEAEQCN9WBZB9BJAIIY9UDLIGFOAA'
          ),

        current_index           = 4,
        last_index              = 7,
        value                   = 0,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # Input, Part 1 of 2
      Transaction(
        # Make the signature look like a message, so we can verify that
        # the Bundle skips it correctly.
        signature_message_fragment =
          Fragment.from_string('This is a signature, not a message!'),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999WGSBUA'
            b'HDVHYHOBHGP9VCGIZHNCAAQFJGE9YHEHEFTDAGXHY'
          ),

        current_index           = 5,
        last_index              = 7,
        value                   = -100,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # Input, Part 2 of 2
      Transaction(
        # Make the signature look like a message, so we can verify that
        # the Bundle skips it correctly.
        signature_message_fragment =
          Fragment.from_string('This is a signature, not a message!'),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999WGSBUA'
            b'HDVHYHOBHGP9VCGIZHNCAAQFJGE9YHEHEFTDAGXHY'
          ),

        current_index           = 6,
        last_index              = 7,
        value                   = 0,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),

      # Change
      Transaction(
        # It's unusual for a change transaction to have a message, but
        # half the fun of unit tests is designing unusual scenarios!
        signature_message_fragment =
          Fragment.from_string('I can haz change?'),

        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999FFYALH'
            b'N9ACYCP99GZBSDK9CECFI9RAIH9BRCCAHAIAWEFAN'
          ),

        current_index           = 7,
        last_index              = 7,
        value                   = 40,

        # These values are not relevant to the tests.
        branch_transaction_hash = TransactionHash(b''),
        bundle_hash             = BundleHash(b''),
        hash_                   = TransactionHash(b''),
        nonce                   = Hash(b''),
        tag                     = Tag(b''),
        timestamp               = 1485020456,
        trunk_transaction_hash  = TransactionHash(b''),
      ),
    ])

  def test_get_messages_errors_drop(self):
    """
    Decoding messages from a bundle, with ``errors='drop'``.
    """
    messages = self.bundle.get_messages('drop')

    self.assertEqual(len(messages), 3)

    self.assertEqual(messages[0], 'Hello, world!')

    # noinspection SpellCheckingInspection
    self.assertEqual(
      messages[1],

      '''
"Good morning," said Deep Thought at last.
"Er... Good morning, O Deep Thought," said Loonquawl nervously.
  "Do you have... er, that is..."
"... an answer for you?" interrupted Deep Thought majestically. "Yes. I have."
The two men shivered with expectancy. Their waiting had not been in vain.
"There really is one?" breathed Phouchg.
"There really is one," confirmed Deep Thought.
"To Everything? To the great Question of Life, the Universe and Everything?"
"Yes."
Both of the men had been trained for this moment; their lives had been a
  preparation for it; they had been selected at birth as those who would
  witness the answer; but even so they found themselves gasping and squirming
  like excited children.
"And you're ready to give it to us?" urged Loonquawl.
"I am."
"Now?"
"Now," said Deep Thought.
They both licked their dry lips.
"Though I don't think," added Deep Thought, "that you're going to like it."
"Doesn't matter," said Phouchg. "We must know it! Now!"
"Now?" enquired Deep Thought.
"Yes! Now!"
"All right," said the computer and settled into silence again.
  The two men fidgeted. The tension was unbearable.
"You're really not going to like it," observed Deep Thought.
"Tell us!"
"All right," said Deep Thought. "The Answer to the Great Question..."
"Yes?"
"Of Life, the Universe and Everything..." said Deep Thought.
"Yes??"
"Is..."
"Yes?!"
"Forty-two," said Deep Thought, with infinite majesty and calm.
        ''',
    )

    self.assertEqual(messages[2], 'I can haz change?')

  def test_get_messages_errors_strict(self):
    """
    Decoding messages from a bundle, with ``errors='strict'``.
    """
    with self.assertRaises(UnicodeDecodeError):
      self.bundle.get_messages('strict')

  def test_get_messages_errors_ignore(self):
    """
    Decoding messages from a bundle, with ``errors='ignore'``.
    """
    messages = self.bundle.get_messages('ignore')

    self.assertEqual(len(messages), 4)

    # The only message that is treated differently is the invalid one.
    self.assertEqual(messages[0], '祝你好运\x15')

  def test_get_messages_errors_replace(self):
    """
    Decoding messages from a bundle, with ``errors='replace'``.
    """
    messages = self.bundle.get_messages('replace')

    self.assertEqual(len(messages), 4)

    # The only message that is treated differently is the invalid one.
    self.assertEqual(messages[0], '祝你好运�\x15')


class BundleValidatorTestCase(TestCase):
  # noinspection SpellCheckingInspection
  def setUp(self):
    super(BundleValidatorTestCase, self).setUp()

    # Define a valid bundle that will serve as the happy path.
    # We will mangle it in various ways to trigger validation errors.
    self.bundle = Bundle([
      # "Spend" transaction, Part 1 of 1
      Transaction(
        hash_ =
          TransactionHash(
            b'LUQJUUDAZIHSTPBLCZYXWXYKXTFCOCQJ9EHXKLEB'
            b'IJBPSRFSBYRBYODDAZ9NPKPYSMPVNEFXYZQ999999'
          ),

        address =
          Address(
            b'FZXUHBBLASPIMBDIHYTDFCDFIRII9LRJPXFTQTPO'
            b'VLEIFE9NWTFPPQZHDCXYUOUCXHHNRPKCIROYYTWSA'
          ),

        branch_transaction_hash =
          TransactionHash(
            b'UKGIAYNLALFGJOVUZYJGNIOZSXBBZDXVQLUMHGQE'
            b'PZJWYDMGTPJIQXS9GOKXR9WIGWFRWRSKGCJ999999'
          ),

        bundle_hash =
          BundleHash(
            b'ZSATLX9HDENCIARERVLWYHXPQETFL9QKTNC9LUOL'
            b'CDXKKW9MYTLZJDXBNOHURUXSYWMGGD9UDGLHCSZO9'
          ),

        nonce =
          Hash(
            b'LIJVXBVTYMEEPCKJRIQTGAKWJRAMYNPJEGHEWAUL'
            b'XPBBUQPCJTJPRZTISQPJRJGMSBGQLER9OXYQXFGQO'
          ),

        trunk_transaction_hash =
          TransactionHash(
            b'KFCQSGDYENCECCPNNZDVDTBINCBRBERPTQIHFH9G'
            b'YLTCSGUFMVWWSAHVZFXDVEZO9UHAUIU9LNX999999'
          ),

        signature_message_fragment = Fragment(b''),

        current_index = 0,
        last_index    = 3,
        tag           = Tag(b''),
        timestamp     = 1483033814,
        value         = 1,
      ),

      # Input #1, Part 1 of 2
      Transaction(
        hash_ =
          TransactionHash(
            b'KFCQSGDYENCECCPNNZDVDTBINCBRBERPTQIHFH9G'
            b'YLTCSGUFMVWWSAHVZFXDVEZO9UHAUIU9LNX999999'
          ),

        address =
          Address(
            b'GMHOSRRGXJLDPVWRWVSRWI9BCIVLUXWKTJYZATIA'
            b'RAZRUCRGTWXWP9SZPFOVAMLISUPQUKHNDMITUJKIB'
          ),

        branch_transaction_hash =
          TransactionHash(
            b'UKGIAYNLALFGJOVUZYJGNIOZSXBBZDXVQLUMHGQE'
            b'PZJWYDMGTPJIQXS9GOKXR9WIGWFRWRSKGCJ999999'
          ),

        bundle_hash =
          BundleHash(
            b'ZSATLX9HDENCIARERVLWYHXPQETFL9QKTNC9LUOL'
            b'CDXKKW9MYTLZJDXBNOHURUXSYWMGGD9UDGLHCSZO9'
          ),

        nonce =
          Hash(
            b'VRYLDCKEWZJXPQVSWOJVYVBJSCWZQEVKPBG9KGEZ'
            b'GPRQFKFSRNBPXCSVQNJINBRNEPIKAXNHOTJFIVYJO'
          ),

        trunk_transaction_hash =
          TransactionHash(
            b'QSTUKDIBYAZIQVEOMFGKQPHAIPBHUPSDQFFKKHRA'
            b'ABYMYMQDHMTEWCM9IMZHQMGXOTWNSJYHRNA999999'
          ),

        signature_message_fragment =
          Fragment(
            b'XS9OVIXHIGGR9IYQBHGMFAHPZBWLIBNAQPFMPVYUZDOLLFDJIPZEMIOGVANQJSCU'
            b'IPDNNUNAMWEL9OFXXK9NV9UTCRBYTARBJHPQYJYKNAQGMATG9EXQMHGXY9QOHPBA'
            b'FEVABDYMCXORXHBMPLEWJYGYFFBWVXAUXHGLTABBKOQMZLFAYWDAKEOMJPJX9TMT'
            b'GXIJXZTKRRIPAMYY9UNSPPEGFPJE9NFSJFWKYOFZRMPBXZDNQUEKLRUVPXMCTQRE'
            b'ZWICSCVXN9VBLN9DRINRPAZTYJYXPGGRZJLMYXGCLUQNZ9NJGH9GFQPKKVK9N9WR'
            b'IJXDNKUMLLJUVIQRGPHEVWTXQHRLRCWQJCHTPASCVLRGPNWSIUKWIBMDJJ9EUTQ9'
            b'NXZZEJFWY9LCJJSOEPXWETUBKKVZNUKTLUPEPDBLUWCQGYTOXZ9NZUXHBDOUYQBP'
            b'MNECVJ9HGWA9AWU9VHGETWKBU9YZEZGEQKMVTAKPLCZVWKQFXDEFBPKNUCQDSPWA'
            b'LMPFTUFGRFDZH9PQHJ9WXZPCDWGMNASVVEUXEGWATM9ZIMCEEXTHCXFLYG9LQAKV'
            b'UOGORP9UUWYFTWGZ9OFOGSP9KDNPDSQKEMMISEMWQDVFKCSQXSP9RUMNUQJOBACU'
            b'MPIXCGBJLQQGB9GDSMUUUSYWIY9ZNIAIZBJYTAJKJKZIBFPMGDWUEPXSO9HUJRNV'
            b'QE9OTVUPKBVNVUBSILVZEDPC9AMEYAIATE9JEIQQWIMGCZXMHOPXPFUTEPJEATJN'
            b'QWDFZQ9OGPNBFUHLJDJZQJLXCFEUDPZKVCPEBTNBRYNIIKJHUV9EUFVMB9AHTARQ'
            b'DN9TZ9JPAPCEXSYHZPAQLBJMNQ9R9KPWVZLDLFNHYCCQBFVEPMEZSXAB9GOKGOGC'
            b'SOVL9XJSAQYSECY9UUNSVQSJB9BZVYRUURNUDMZVBJTMIDQUKQLMVW99XFDWTOPR'
            b'UBRPKS9BGEAQPIODAMJAILNCH9UVYVWSDCZXZWLO9XJJZ9FQOL9F9ZJDNGMUGFKJ'
            b'PCYURGYBGYRVKPEBKMJPZZGDKZKT9UBFSJEELREWOYDQZVUPVSGPZYIDVOJGNTXC'
            b'OFGCHBGVZPQDNRKAQNVJEYKYTKHTFBJRDMKVSHEWADNYIQOAUFXYMZKNJPLXGYFX'
            b'DTCVDDBUHBDPG9WLNMWPSCCCGVTIOOLEECXKNVAYNNTDLJMDGDGSKOGWO9UYXTTF'
            b'FCRZEDDQNN9ZODTETGMGGUXOYECGNMHGMGXHZSPODIBMBATJJHSPQHDUCZOMWQNI'
            b'CUZG9LAMBOQRQQDIPIBMIDCIAJBBBNDUAIEMFCEASHPUJPFPPXNDUVGDNNYBRRTW'
            b'SPXGXMCSUXYJSTFIRUIDNEUSVKNIDKIBRQNMEDCYQOMJYTMGRZLYHBUYXCRGSAXR'
            b'ZVHTZEAKNAUKJPFGPOGQLTDMSOXR9NVOIAIMCBVWOF9FXAZUKKZKHJEGHFNLUB9B'
            b'TGAICGQGAYZRRHSFIDTNIJPHIHCXTHQUSKJRSVAWFUXLBYA99QKMGLHDNUHOPEW9'
            b'OFNWPDXXRVZREUIQKSVSDCFIJ99TSGSZ9KU9JGE9VXDVVOLMGNMUGSHUZAOFCIMK'
            b'CPEWMG9IHUZAILQCANIUUG9JNEZMT9EONSN9CWWQOTFBEPZRTTJTQFSTQTBERKGE'
            b'NGFFIYMZMCFBYNIOBPOFOIYPUMYYPRXEHUJEVVELOPNXAPCYFXQ9ORMSFICDOZTS'
            b'GQOMDI9FKEKRIMZTWSIWMYAUSBIN9TPFSMQZCYGVPVWKSFZXPE9BP9ALNWQOVJGM'
            b'SCSJSTNUTMUAJUIQTITPPOHG9NKIFRNXSCMDAEW9LSUCTCXITSTZSBYMPOMSMTXP'
            b'CEBEOAUJK9STIZRXUORRQBCYJPCNHFKEVY9YBJL9QGLVUCSZKOLHD9BDNKIVJX9T'
            b'PPXQVGAXUSQQYGFDWQRZPKZKKWB9ZBFXTUGUGOAQLDTJPQXPUPHNATSGILEQCSQX'
            b'X9IAGIVKUW9MVNGKTSCYDMPSVWXCGLXEHWKRPVARKJFWGRYFCATYNZDTRZDGNZAI'
            b'OULYHRIPACAZLN9YHOFDSZYIRZJEGDUZBHFFWWQRNOLLWKZZENKOWQQYHGLMBMPF'
            b'HE9VHDDTBZYHMKQGZNCSLACYRCGYSFFTZQJUSZGJTZKKLWAEBGCRLXQRADCSFQYZ'
            b'G9CM9VLMQZA'
          ),

        current_index = 1,
        last_index    = 3,
        tag           = Tag(b''),
        timestamp     = 1483033814,
        value         = -99,
      ),

      # Input #1, Part 2 of 2
      Transaction(
        hash_ =
          TransactionHash(
            b'QSTUKDIBYAZIQVEOMFGKQPHAIPBHUPSDQFFKKHRA'
            b'ABYMYMQDHMTEWCM9IMZHQMGXOTWNSJYHRNA999999'
          ),

        address =
          Address(
            b'GMHOSRRGXJLDPVWRWVSRWI9BCIVLUXWKTJYZATIA'
            b'RAZRUCRGTWXWP9SZPFOVAMLISUPQUKHNDMITUJKIB'
          ),

        branch_transaction_hash =
          TransactionHash(
            b'UKGIAYNLALFGJOVUZYJGNIOZSXBBZDXVQLUMHGQE'
            b'PZJWYDMGTPJIQXS9GOKXR9WIGWFRWRSKGCJ999999'
          ),

        bundle_hash =
          BundleHash(
            b'ZSATLX9HDENCIARERVLWYHXPQETFL9QKTNC9LUOL'
            b'CDXKKW9MYTLZJDXBNOHURUXSYWMGGD9UDGLHCSZO9'
          ),

        nonce =
          Hash(
            b'AAKVYZOEZSOXTX9LOLHZYLNAS9CXBLSWVZQAMRGW'
            b'YW9GHHMVIOHWBMTXHDBXRTF9DEFFQFQESNVJORNXK'
          ),

        trunk_transaction_hash =
          TransactionHash(
            b'ZYQGVZABMFVLJXHXXJMVAXOXHRJTTQUVDIIQOOXN'
            b'NDPQGDFDRIDQMUWJGCQKKLGEUQRBFAJWZBC999999'
          ),

        signature_message_fragment =
          Fragment(
            b'YSNEGUCUHXEEFXPQEABV9ATGQMMXEVGMZWKKAFAVOVGUECOZZJFQDNRBCSXCOTBD'
            b'BRUJ9HF9CITXQI9ZQGZFKCXMFZTOYHUTCXDIBIMTBKVXMMTPNKRDRLQESLWFZSQQ'
            b'9BCGKVIZAHBWYTNXG9OWOXHAMQECMOVKN9SOEVJBBARPXUXYUQVFPYXWXQQMDIVP'
            b'VITRWTNNBY9CYBHXJTZUVIPJJG9WLTNMFVPXGYZCNOGSLGVMS9YXXNSV9AYPXZTA'
            b'QJYUNUFBCSZBZNKWCPMVMOGFIDENTOOOCPRDJTNGQRLA9YKMLYZQRO9QQJMCSYVF'
            b'YLISFIWQQYMWMHUOEZPATYCEZARLWLAMCZWYWJZVD9WWKYJURTOLITFFRXQUBKST'
            b'DG9CKDBLPXTPCIMKEKRGEXJGLRL9ZST9VOLV9NOFZLIMVOZBDZJUQISUWZKOJCRN'
            b'YRBRJLCTNPV9QIWQJZDQFVPSTW9BJYWHNRVQTITWJYB9HBUQBXTAGK9BZCHYWYPE'
            b'IREDOXCYRW9UXVSLZBBPAFIUEJABMBYKSUPNWVVKAFQJKDAYYRDICTGOTWWDSFLG'
            b'BQFZZ9NBEHZHPHVQUYEETIRUDM9V9LBXFUXTUGUMZG9HRBLXCKMMWWMK9VTKVZSA'
            b'PRSMJVBLFFDHTYCPDXKBUYYLZDPW9EVXANPZOPBASQUPRNCDGHNUK9NDUQSULUZI'
            b'VMIJTPUGMZPCYR9AERBAGUYNGVEHWIIADAAPPMYQOAGBQCXEDTQOGHWHHSWDFZLC'
            b'DVLNPYMGDPZWOZURT9OZKDJKFECXSFIALXJDRJWMWMTNUUNVDUCJAZLDRN9ZWLHH'
            b'SNXDWULUBNLVRDJZQMKCTRCKULKS9VARFZSRYZCPNH9FHXCAFWKPNGOPOFMYXJLE'
            b'LTKUHSZVDQRDJIGQRGOSKYWDCU9EBJMXQDBKTBNQTIZNCALHRNTHKN99WOBQVVEV'
            b'HEDTDRKFPGLIWOSPLAAELQQXDCDWPIFED9OEUPYPKHZBOHPQGQGSEKO9BFIQFYZK'
            b'YEULWSIBZVSPXBGOJTTYBVIIIPAXGL9ZJNNIELFYAUOUBRDWLJJMSAXHQOYGOWDV'
            b'HHPISRZFSHPDLNQDFWRHLWNAJPYM9REAJLZDIAIVLQBFAUJIQKVHJDFPXENI9ZM9'
            b'SFNGSQHDFEDC9CQVXAXTQVLWYMVSLEDCOVNSQLSANLVA9TWSY9BHAJKOCGI9YLAB'
            b'VROCBJRVXRWBKNUXCAXJIAYWSFRDZHIPQSNBRYNKZAFXHDUENVLHFHYIKH9IANFV'
            b'FKWVFJCSEELVTDDUHBPIYNFLTJLINNORIMDEAXMN9LGNGBWVWYWQIPWKBFDKNDOX'
            b'WFKGBAMZIUFYA9DXGAL9OQQTJAUUXTINWZSQUTPUKUMOZCGOBKKFBXCVR9AGTAQS'
            b'SVGTUBBHSIRHFRSIR9SKSZPXQFG9AOYAHZNQR9AHSEFCKWCJHUTLREDVGBQYVBZR'
            b'CZDXFG9PTSAWQOURYKNWYAZNASV9UMUYUMFCQSFDHZD99WUMCORLYTIZMRGNBAY9'
            b'UJYJMMRCLJP9XVLXTAZOHNVVYSCOSDHGUOPXIRBJDXJUCJYLQKUJOTNJCPRBDOKV'
            b'ZEMIGZRNJOQKFFAXQVGGY9YRJORZCOD9REIIIDDTRQ9TJWTFYRKOPLAFNUUPCHXA'
            b'WVPYUQXAFFCTYAESWAFUTQQYZRQVLVZW9OWAAJMPSAEPKWXVEZVTVPQEEBVXNZJP'
            b'ZU9JJSIAEPIT9HE99XNAUYOAKRIFQQJQTFIMWEOKLCH9JKCQTGZPEGWORFB9ARNS'
            b'DPYKRONBONYOGEVEFXGTMQTQBEMFQWEMIDSGAVEQHVHAPSMTCJ9FMEYBWAQWWJCE'
            b'ABUUMMVNDMSBORFLHVIIDOUQHHXQKXTVGRAYTLMECCSVZOZM9JKUWIGGFLMMDGBU'
            b'DBIHJFUINVOKSFTOGFCZEMIBSZNGPL9HXWGTNNAKYIMDITCRMSHFR9BDSFGHXQMR'
            b'ACZOVUOTSJSKMNHNYIFEOD9CVBWYVVMG9ZDNR9FOIXSZSTIO9GLOLPLMW9RPAJYB'
            b'WTCKV9JMSEVGD9ZPEGKXF9XYQMUMJPWTMFZJODFIEYNLI9PWODSPPW9MVJOWZQZU'
            b'CIKXCVVXDKWHXV99GOEZ9CMGUH9OWGLLISNZEPSAPEDHVRKKGFFNGBXFLDBQTTQL'
            b'WVLUITJQ9JM'
          ),

        current_index = 2,
        last_index    = 3,
        tag           = Tag(b''),
        timestamp     = 1483033814,
        value         = 0,
      ),

      # "Change" transaction, Part 1 of 1
      Transaction(
        hash_ =
          TransactionHash(
            b'ZYQGVZABMFVLJXHXXJMVAXOXHRJTTQUVDIIQOOXN'
            b'NDPQGDFDRIDQMUWJGCQKKLGEUQRBFAJWZBC999999'
          ),

        address =
          Address(
            b'YOTMYW9YLZQCSLHB9WRSTZDYYYGUUWLVDRHFQFEX'
            b'UVOQARTQWZGLBU9DVSRDPCWYWQZHLFHY9NGLPZRAQ'
          ),

        branch_transaction_hash =
          TransactionHash(
            b'QCHKLZZBG9XQMNGCDVXZGDRXIJMFZP9XUGAWNNVP'
            b'GXBWB9NVEKEFMUWOEACULFUR9Q9XCWPBRNF999999'
          ),

        bundle_hash =
          BundleHash(
            b'ZSATLX9HDENCIARERVLWYHXPQETFL9QKTNC9LUOL'
            b'CDXKKW9MYTLZJDXBNOHURUXSYWMGGD9UDGLHCSZO9'
          ),

        nonce =
          Hash(
            b'TPGXQFUGNEYYFFKPFWJSXKTWEUKUFTRJCQKKXLXL'
            b'PSOHBZTGIBFPGLSVRIVYAC9NZMOMZLARFZYCNNRCM'
          ),

        trunk_transaction_hash =
          TransactionHash(
            b'UKGIAYNLALFGJOVUZYJGNIOZSXBBZDXVQLUMHGQE'
            b'PZJWYDMGTPJIQXS9GOKXR9WIGWFRWRSKGCJ999999'
          ),

        signature_message_fragment = Fragment(b''),

        current_index = 3,
        last_index    = 3,
        tag           = Tag(b''),
        timestamp     = 1483033814,
        value         = 98,
      ),
    ])

  def test_pass_happy_path(self):
    """
    Bundle passes validation.
    """
    validator = BundleValidator(self.bundle)

    self.assertListEqual(validator.errors, [])
    self.assertTrue(validator.is_valid())

  def test_pass_empty(self):
    """
    Bundle has no transactions.
    """
    validator = BundleValidator(Bundle())

    self.assertListEqual(validator.errors, [])
    self.assertTrue(validator.is_valid())

  def test_fail_balance_positive(self):
    """
    The bundle balance is > 0.
    """
    self.bundle.transactions[0].value += 1

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Bundle has invalid balance (expected 0, actual 1).',
      ],
    )

  def test_fail_balance_negative(self):
    """
    The bundle balance is < 0.
    """
    self.bundle.transactions[3].value -= 1

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Bundle has invalid balance (expected 0, actual -1).',
      ],
    )

  def test_fail_bundle_hash_invalid(self):
    """
    One of the transactions has an invalid ``bundle_hash`` value.
    """
    # noinspection SpellCheckingInspection
    self.bundle.transactions[3].bundle_hash =\
      BundleHash(
        b'NFDPEEZCWVYLKZGSLCQNOFUSENIXRHWWTZFBXMPS'
        b'QHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9PG'
      )

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 3 has invalid bundle hash.',
      ],
    )

  def test_fail_current_index_invalid(self):
    """
    One of the transactions has an invalid ``current_index`` value.
    """
    self.bundle.transactions[3].current_index = 4

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 3 has invalid current index value '
        '(expected 3, actual 4).',
      ],
    )

  def test_fail_last_index_invalid(self):
    """
    One of the transactions has an invalid ``last_index`` value.
    """
    self.bundle.transactions[0].last_index = 2

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 0 has invalid last index value '
        '(expected 3, actual 2).'
      ],
    )

  def test_fail_missing_signature_fragment_underflow(self):
    """
    The last transaction in the bundle is an input, and its second
    signature fragment is missing.
    """
    # Remove the last input's second signature fragment, and the change
    # transaction.
    del self.bundle.transactions[-2:]
    for (i, txn) in enumerate(self.bundle): # type: Tuple[int, Transaction]
      txn.current_index = i
      txn.last_index    = 1

    # Fix bundle balance, since we removed the change transaction.
    self.bundle[1].value = -self.bundle[0].value

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 1 has invalid signature (using 1 fragments).',
      ],
    )

  def test_fail_signature_fragment_address_wrong(self):
    """
    The second signature fragment for an input is associated with the
    wrong address.
    """
    # noinspection SpellCheckingInspection
    self.bundle[2].address =\
      Address(
        b'QHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9P'
        b'GNFDPEEZCWVYLKZGSLCQNOFUSENIXRHWWTZFBXMPS'
      )

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 1 has invalid signature (using 1 fragments).',
      ],
    )

  def test_fail_signature_fragment_value_wrong(self):
    """
    The second signature fragment for an input has a nonzero balance.
    """
    self.bundle[2].value = -1
    self.bundle[-1].value += 1

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 2 has invalid amount (expected 0, actual -1).',
      ],
    )

  def test_fail_signature_invalid(self):
    """
    One of the input signatures fails validation.
    """
    self.bundle[2].signature_message_fragment[:-1] = b'9'

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      [
        'Transaction 1 has invalid signature (using 2 fragments).',
      ],
    )

  def test_fail_multiple_errors(self):
    """
    The bundle has multiple problems.
    """
    del self.bundle.transactions[2]

    validator = BundleValidator(self.bundle)

    self.assertFalse(validator.is_valid())

    self.assertListEqual(
      validator.errors,

      # Note that there is no error about the missing signature
      # fragment for transaction 1.  The bundle fails some basic
      # consistency checks, so we don't even bother to validate
      # signatures.
      [
        'Transaction 0 has invalid last index value '
        '(expected 2, actual 3).',

        'Transaction 1 has invalid last index value '
        '(expected 2, actual 3).',

        'Transaction 2 has invalid current index value '
        '(expected 2, actual 3).',

        'Transaction 2 has invalid last index value '
        '(expected 2, actual 3).',
      ],
    )


class ProposedBundleTestCase(TestCase):
  def setUp(self):
    super(ProposedBundleTestCase, self).setUp()

    # We will use a seed to generate addresses and private keys, to
    # ensure a realistic scenario (and because the alternative is to
    # inject mocks all over the place!).
    # noinspection SpellCheckingInspection
    self.seed =\
      Seed(
        b'TESTVALUE9DONTUSEINPRODUCTION99999RLC9CS'
        b'ZUILGDTLJMRCJSDVEEJO9A9LHAEHMNAMVXRMOXTBN'
      )

    # To speed things up a little bit, though, we can pre-generate a
    # few addresses to use as inputs.

    # noinspection SpellCheckingInspection
    self.input_0_bal_eq_42 =\
      Address(
        balance         = 42,
        key_index       = 0,
        security_level  = 1,

        trytes =
          b'JBLDCCSI9VKU9ZHNZCUTC9NLQIIJX9SIKUJNKNKE'
          b'9KKMHXFMIXHLKQQAVTTNPRCZENGLIPALHKLNKTXCU',
      )

    # noinspection SpellCheckingInspection
    self.input_1_bal_eq_40 =\
      Address(
        balance         = 40,
        key_index       = 1,
        security_level  = 1,

        trytes =
          b'KHWHSTISMVVSDCOMHVFIFCTINWZT9EHJUATYSMCX'
          b'DSMZXPL9KXREBBYHJGRBCYVGPJQEHEDPXLBDJNQNX',
      )

    # noinspection SpellCheckingInspection
    self.input_2_bal_eq_2 =\
      Address(
        balance         = 2,
        key_index       = 2,
        security_level  = 1,

        trytes =
          b'GOAAMRU9EALPO9GKBOWUVZVQEJMB9CSGIZJATHRB'
          b'TRRJPNTSQRZTASRBTQCRFAIDOGTWSHIDGOUUULQIG',
      )

    # noinspection SpellCheckingInspection
    self.input_3_bal_eq_100 =\
      Address(
        balance         = 100,
        key_index       = 3,
        security_level  = 1,

        trytes =
          b'9LPQCSJGYUJMLWKMLJ9KYUYJ9RMDBZZWPHXMGKRG'
          b'YLOAZNKJR9VDYSONVAJRIPVWCOZKFMEKUSWHPSDDZ',
      )

    # noinspection SpellCheckingInspection
    self.input_4_bal_eq_42_sl_2 =\
      Address(
        balance         = 42,
        key_index       = 4,
        security_level  = 2,

        trytes =
          b'NVGLHFZWLEQAWBDJXCWJBMVBVNXEG9DALNBTAYMK'
          b'EMMJ9BCDVVHJJLSTQW9JEJXUUX9JNFGALBNASRDUD',
      )

    # noinspection SpellCheckingInspection
    self.input_5_bal_eq_42_sl_3 =\
      Address(
        balance         = 42,
        key_index       = 5,
        security_level  = 3,

        trytes =
          b'XXYRPQ9BDZGKZZQLYNSBDD9HZLI9OFRK9TZCTU9P'
          b'FAJYXZIZGO9BWLOCNGVMTLFQFMGJWYRMLXSCW9UTQ',
      )

    self.bundle = ProposedBundle()

  def test_add_transaction_short_message(self):
    """
    Adding a transaction to a bundle, with a message short enough to
    fit inside a single transaction.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999AETEXB'
          b'D9YBTH9EMFKF9CAHJIAIKDBEPAMH99DEN9DAJETGN'
        ),

      message = TryteString.from_string('Hello, IOTA!'),
      value   = 42,
    ))

    # We can fit the message inside a single fragment, so only one
    # transaction is necessary.
    self.assertEqual(len(self.bundle), 1)

  def test_add_transaction_long_message(self):
    """
    Adding a transaction to a bundle, with a message so long that it
    has to be split into multiple transactions.
    """
    # noinspection SpellCheckingInspection
    address = Address(
      b'TESTVALUE9DONTUSEINPRODUCTION99999N9GIUF'
      b'HCFIUGLBSCKELC9IYENFPHCEWHIDCHCGGEH9OFZBN'
    )

    tag = Tag.from_string('H2G2')

    self.bundle.add_transaction(ProposedTransaction(
      address = address,
      tag     = tag,

      message = TryteString.from_string(
        '''
"Good morning," said Deep Thought at last.
"Er... Good morning, O Deep Thought," said Loonquawl nervously.
  "Do you have... er, that is..."
"... an answer for you?" interrupted Deep Thought majestically. "Yes. I have."
The two men shivered with expectancy. Their waiting had not been in vain.
"There really is one?" breathed Phouchg.
"There really is one," confirmed Deep Thought.
"To Everything? To the great Question of Life, the Universe and Everything?"
"Yes."
Both of the men had been trained for this moment; their lives had been a
  preparation for it; they had been selected at birth as those who would
  witness the answer; but even so they found themselves gasping and squirming
  like excited children.
"And you're ready to give it to us?" urged Loonquawl.
"I am."
"Now?"
"Now," said Deep Thought.
They both licked their dry lips.
"Though I don't think," added Deep Thought, "that you're going to like it."
"Doesn't matter," said Phouchg. "We must know it! Now!"
"Now?" enquired Deep Thought.
"Yes! Now!"
"All right," said the computer and settled into silence again.
  The two men fidgeted. The tension was unbearable.
"You're really not going to like it," observed Deep Thought.
"Tell us!"
"All right," said Deep Thought. "The Answer to the Great Question..."
"Yes?"
"Of Life, the Universe and Everything..." said Deep Thought.
"Yes??"
"Is..."
"Yes?!"
"Forty-two," said Deep Thought, with infinite majesty and calm.
        '''
      ),

      # Now you know....
      # Eh, who am I kidding?  You probably knew before I did (:
      value = 42,
    ))

    # Because the message is too long to fit into a single fragment,
    # the transaction is split into two parts.
    self.assertEqual(len(self.bundle), 2)

    txn1 = self.bundle[0]
    self.assertEqual(txn1.address, address)
    self.assertEqual(txn1.tag, tag)
    self.assertEqual(txn1.value, 42)

    txn2 = self.bundle[1]
    self.assertEqual(txn2.address, address)
    self.assertEqual(txn2.tag, tag)
    # Supplementary transactions are assigned zero IOTA value.
    self.assertEqual(txn2.value, 0)

  def test_add_transaction_error_already_finalized(self):
    """
    Attempting to add a transaction to a bundle that is already
    finalized.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION999999DCBIE'
          b'U9AIE9H9BCKGMCVCUGYDKDLCAEOHOHZGW9KGS9VGH'
        ),

        value = 0,
    ))
    self.bundle.finalize()

    with self.assertRaises(RuntimeError):
      self.bundle.add_transaction(ProposedTransaction(
        address = Address(b''),
        value   = 0,
      ))

  def test_add_transaction_error_negative_value(self):
    """
    Attempting to add a transaction with a negative value to a bundle.

    Use :py:meth:`ProposedBundle.add_inputs` to add inputs to a bundle.
    """
    with self.assertRaises(ValueError):
      self.bundle.add_transaction(ProposedTransaction(
        address = Address(b''),
        value   = -1,
      ))

  def test_add_inputs_no_change(self):
    """
    Adding inputs to cover the exact amount of the bundle spend.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999VELDTF'
          b'QHDFTHIHFE9II9WFFDFHEATEI99GEDC9BAUH9EBGZ'
        ),

        value = 29,
    ))

    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999OGVEEF'
          b'BCYAM9ZEAADBGBHH9BPBOHFEGCFAM9DESCCHODZ9Y'
        ),

      value = 13,
    ))

    self.bundle.add_inputs([
      self.input_1_bal_eq_40,
      self.input_2_bal_eq_2,
    ])

    # Just to be tricky, add an unnecessary change address, just to
    # make sure the bundle ignores it.
    # noinspection SpellCheckingInspection
    self.bundle.send_unspent_inputs_to(
      Address(
        b'TESTVALUE9DONTUSEINPRODUCTION99999FDCDFD'
        b'VAF9NFLCSCSFFCLCW9KFL9TCAAO9IIHATCREAHGEA'
      ),
    )

    self.bundle.finalize()

    # All of the addresses that we generate for this test case have
    # security level set to 1, so we only need 1 transaction per
    # input (4 total, including the spends).
    #
    # Also note: because the transaction is already balanced, no change
    # transaction is necessary.
    self.assertEqual(len(self.bundle), 4)

  def test_add_inputs_with_change(self):
    """
    Adding inputs to a bundle results in unspent inputs.
    """
    tag = Tag(b'CHANGE9TXN')

    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999VELDTF'
          b'QHDFTHIHFE9II9WFFDFHEATEI99GEDC9BAUH9EBGZ'
        ),

        value = 29,
    ))

    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999OGVEEF'
          b'BCYAM9ZEAADBGBHH9BPBOHFEGCFAM9DESCCHODZ9Y'
        ),

      tag   = tag,
      value = 13,
    ))

    self.bundle.add_inputs([self.input_3_bal_eq_100])

    # noinspection SpellCheckingInspection
    change_address =\
      Address(
        b'TESTVALUE9DONTUSEINPRODUCTION99999KAFGVC'
        b'IBLHS9JBZCEFDELEGFDCZGIEGCPFEIQEYGA9UFPAE'
      )

    self.bundle.send_unspent_inputs_to(change_address)

    self.bundle.finalize()

    # 2 spends + 1 input (with security level 1) + 1 change
    self.assertEqual(len(self.bundle), 4)

    change_txn = self.bundle[-1]
    self.assertEqual(change_txn.address, change_address)
    self.assertEqual(change_txn.value, 58)
    self.assertEqual(change_txn.tag, tag)

  def test_add_inputs_security_level(self):
    """
    Each input's security level determines the number of transactions
    we will need in order to store the entire signature.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(
      ProposedTransaction(
        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999XE9IVG'
            b'EFNDOCQCMERGUATCIEGGOHPHGFIAQEZGNHQ9W99CH',
          ),

        value = 84,
      ),
    )

    self.bundle.add_inputs([
      self.input_4_bal_eq_42_sl_2,
      self.input_5_bal_eq_42_sl_3,
    ])

    self.bundle.finalize()

    # Each input's security level determines how many transactions will
    # be needed to hold all of its signature fragments:
    # 1 spend + 2 fragments for input 0 + 3 fragments for input 1
    self.assertEqual(len(self.bundle), 6)

  def test_add_inputs_error_already_finalized(self):
    """
    Attempting to add inputs to a bundle that is already finalized.
    """
    # Add 1 transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(
      ProposedTransaction(
        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999XE9IVG'
            b'EFNDOCQCMERGUATCIEGGOHPHGFIAQEZGNHQ9W99CH',
          ),

        value = 0,
      ),
    )

    self.bundle.finalize()

    with self.assertRaises(RuntimeError):
      # Even though no inputs are provided, it's still an error; you
      # shouldn't even be calling ``add_inputs`` once the bundle is
      # finalized!
      self.bundle.add_inputs([])

  def test_send_unspent_inputs_to_error_already_finalized(self):
    """
    Invoking ``send_unspent_inputs_to`` on a bundle that is already
    finalized.
    """
    # Add 1 transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999XE9IVG'
          b'EFNDOCQCMERGUATCIEGGOHPHGFIAQEZGNHQ9W99CH'
        ),

      value = 0,
    ))

    self.bundle.finalize()

    with self.assertRaises(RuntimeError):
      self.bundle.send_unspent_inputs_to(Address(b''))

  def test_finalize_error_already_finalized(self):
    """
    Attempting to finalize a bundle that is already finalized.
    """
    # Add 1 transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999XE9IVG'
          b'EFNDOCQCMERGUATCIEGGOHPHGFIAQEZGNHQ9W99CH'
        ),

      value = 0,
    ))

    self.bundle.finalize()

    with self.assertRaises(RuntimeError):
      self.bundle.finalize()

  def test_finalize_error_no_transactions(self):
    """
    Attempting to finalize a bundle with no transactions.
    """
    with self.assertRaises(ValueError):
      self.bundle.finalize()

  def test_finalize_error_negative_balance(self):
    """
    Attempting to finalize a bundle with unspent inputs.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999IGEFUG'
          b'LIHIJGJGZ9CGRENCRHF9XFEAWD9ILFWEJFKDLITCC'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42, self.input_2_bal_eq_2])

    # Bundle spends 42 IOTAs, but inputs total 44 IOTAs.
    self.assertEqual(self.bundle.balance, -2)

    # In order to finalize this bundle, we need to specify a change
    # address.
    with self.assertRaises(ValueError):
      self.bundle.finalize()

  def test_finalize_error_positive_balance(self):
    """
    Attempting to finalize a bundle with insufficient inputs.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999IGEFUG'
          b'LIHIJGJGZ9CGRENCRHF9XFEAWD9ILFWEJFKDLITCC'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_1_bal_eq_40])

    # Bundle spends 42 IOTAs, but inputs total only 40 IOTAs.
    self.assertEqual(self.bundle.balance, 2)

    # In order to finalize this bundle, we need to provide additional
    # inputs.
    with self.assertRaises(ValueError):
      self.bundle.finalize()

  def test_sign_inputs(self):
    """
    Signing inputs in a finalized bundle, using a key generator.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_1_bal_eq_40, self.input_2_bal_eq_2])
    self.bundle.finalize()

    self.bundle.sign_inputs(KeyGenerator(self.seed))

    # Quick sanity check:
    # 1 spend + 2 inputs (security level 1) = 3 transactions.
    # Applying signatures should not introduce any new transactions
    # into the bundle.
    #
    # Note: we will see what happens when we use inputs with different
    # security levels in the next test.
    self.assertEqual(len(self.bundle), 3)

    # The spending transaction does not have a signature.
    self.assertEqual(
      self.bundle[0].signature_message_fragment,
      Fragment(b''),
    )

    # The signature fragments are really long, and we already have unit
    # tests for the signature fragment generator, so to keep this test
    # focused, we are only interested in whether a signature fragment
    # gets applied.
    #
    # References:
    #   - :py:class:`test.crypto.signing_test.SignatureFragmentGeneratorTestCase`
    for i in range(1, len(self.bundle)):
      if self.bundle[i].signature_message_fragment == Fragment(b''):
        self.fail(
          "Transaction {i}'s signature fragment is unexpectedly empty!".format(
            i = i,
          ),
        )

  def test_sign_inputs_security_level(self):
    """
    You may include inputs with different security levels in the same
    bundle.
    """
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(
      ProposedTransaction(
        address =
          Address(
            b'TESTVALUE9DONTUSEINPRODUCTION99999XE9IVG'
            b'EFNDOCQCMERGUATCIEGGOHPHGFIAQEZGNHQ9W99CH',
          ),

        value = 84,
      ),
    )

    self.bundle.add_inputs([
      self.input_4_bal_eq_42_sl_2,
      self.input_5_bal_eq_42_sl_3,
    ])

    self.bundle.finalize()

    self.bundle.sign_inputs(KeyGenerator(self.seed))

    # Quick sanity check.
    self.assertEqual(len(self.bundle), 6)

    # The spending transaction does not have a signature.
    self.assertEqual(
      self.bundle[0].signature_message_fragment,
      Fragment(b''),
    )

    # The signature fragments are really long, and we already have unit
    # tests for the signature fragment generator, so to keep this test
    # focused, we are only interested in whether a signature fragment
    # gets applied.
    #
    # References:
    #   - :py:class:`test.crypto.signing_test.SignatureFragmentGeneratorTestCase`
    for i in range(1, len(self.bundle)):
      if self.bundle[i].signature_message_fragment == Fragment(b''):
        self.fail(
          "Transaction {i}'s signature fragment is unexpectedly empty!".format(
            i = i,
          ),
        )

  def test_sign_inputs_error_not_finalized(self):
    """
    Attempting to sign inputs in a bundle that hasn't been finalized
    yet.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])

    # Oops; did we forget something?
    # self.bundle.finalize()

    with self.assertRaises(RuntimeError):
      self.bundle.sign_inputs(KeyGenerator(b''))

  def test_sign_input_at_single_fragment(self):
    """
    Signing an input at the specified index, only 1 fragment needed.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])
    self.bundle.finalize()

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_0_bal_eq_42)

    self.bundle.sign_input_at(1, private_key)

    # Only 2 transactions are needed for this bundle:
    # 1 spend + 1 input (security level = 1).
    self.assertEqual(len(self.bundle), 2)

    # The spending transaction does not have a signature.
    self.assertEqual(
      self.bundle[0].signature_message_fragment,
      Fragment(b''),
    )

    # The signature fragments are really long, and we already have unit
    # tests for the signature fragment generator, so to keep this test
    # focused, we are only interested in whether a signature fragment
    # gets applied.
    #
    # References:
    #   - :py:class:`test.crypto.signing_test.SignatureFragmentGeneratorTestCase`
    for i in range(1, len(self.bundle)):
      if self.bundle[i].signature_message_fragment == Fragment(b''):
        self.fail(
          "Transaction {i}'s signature fragment is unexpectedly empty!".format(
            i = i,
          ),
        )

  def test_sign_input_at_multiple_fragments(self):
    """
    Signing an input at the specified index, multiple fragments needed.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_5_bal_eq_42_sl_3])
    self.bundle.finalize()

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_5_bal_eq_42_sl_3)

    self.bundle.sign_input_at(1, private_key)

    # 1 spend + 3 inputs (security level = 3).
    self.assertEqual(len(self.bundle), 4)

    # The spending transaction does not have a signature.
    self.assertEqual(
      self.bundle[0].signature_message_fragment,
      Fragment(b''),
    )

    # The signature fragments are really long, and we already have unit
    # tests for the signature fragment generator, so to keep this test
    # focused, we are only interested in whether a signature fragment
    # gets applied.
    #
    # References:
    #   - :py:class:`test.crypto.signing_test.SignatureFragmentGeneratorTestCase`
    for i in range(1, len(self.bundle)):
      if self.bundle[i].signature_message_fragment == Fragment(b''):
        self.fail(
          "Transaction {i}'s signature fragment is unexpectedly empty!".format(
            i = i,
          ),
        )

  def test_sign_input_at_error_not_finalized(self):
    """
    Cannot sign inputs because the bundle isn't finalized yet.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])

    # Oops; did we forget something?
    # self.bundle.finalize()

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_0_bal_eq_42)

    with self.assertRaises(RuntimeError):
      self.bundle.sign_input_at(1, private_key)

  def test_sign_input_at_error_index_invalid(self):
    """
    The specified index doesn't exist in the bundle.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])
    self.bundle.finalize()

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_0_bal_eq_42)

    with self.assertRaises(IndexError):
      self.bundle.sign_input_at(2, private_key)

  def test_sign_input_at_error_index_not_input(self):
    """
    The specified index references a transaction that is not an input.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])
    self.bundle.finalize()

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_0_bal_eq_42)

    with self.assertRaises(ValueError):
      # You can't sign the spend transaction, silly!
      self.bundle.sign_input_at(0, private_key)

  def test_sign_input_at_error_index_wrong_address(self):
    """
    The specified index references a transaction associated with the
    wrong address.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([
      self.input_1_bal_eq_40,
      self.input_2_bal_eq_2,
    ])

    self.bundle.finalize()

    # We generate a private key for input with ``key_index=1``...
    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_1_bal_eq_40)

    with self.assertRaises(ValueError):
      # ... but we try to sign the transaction for input with
      # ``key_index=2``!
      self.bundle.sign_input_at(2, private_key)

  def test_sign_input_at_error_already_signed(self):
    """
    Attempting to sign an input that is already signed.
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])
    self.bundle.finalize()

    # The existing signature fragment doesn't have to be valid; it just
    # has to be not empty.
    self.bundle[1].signature_message_fragment = Fragment(b'A')

    private_key =\
      KeyGenerator(self.seed).get_key_for(self.input_0_bal_eq_42)

    with self.assertRaises(ValueError):
      self.bundle.sign_input_at(1, private_key)

  def test_sign_input_at_error_security_level_wrong(self):
    """
    The private key's security level doesn't match that of the input's
    address.

    This is exceptionally unlikely to occur outside the context of a
    paranoid unit test, but you know how I roll....
    """
    # Add a transaction so that we can finalize the bundle.
    # noinspection SpellCheckingInspection
    self.bundle.add_transaction(ProposedTransaction(
      address =
        Address(
          b'TESTVALUE9DONTUSEINPRODUCTION99999QARFLF'
          b'TDVATBVFTFCGEHLFJBMHPBOBOHFBSGAGWCM9PG9GX'
        ),

      value = 42,
    ))

    self.bundle.add_inputs([self.input_0_bal_eq_42])
    self.bundle.finalize()

    # Note that the private key has the same key index as the input we
    # want to sign, but it uses a different security level.
    private_key = (
      KeyGenerator(self.seed)
        .get_key(index=self.input_0_bal_eq_42.key_index, iterations=2)
    )

    with self.assertRaises(ValueError):
      self.bundle.sign_input_at(1, private_key)


class TransactionHashTestCase(TestCase):
  def test_init_automatic_pad(self):
    """
    Transaction hashes are automatically padded to 81 trytes.
    """
    # noinspection SpellCheckingInspection
    txn = TransactionHash(
      b'JVMTDGDPDFYHMZPMWEKKANBQSLSDTIIHAYQUMZOK'
      b'HXXXGJHJDQPOMDOMNRDKYCZRUFZROZDADTHZC'
    )

    # noinspection SpellCheckingInspection
    self.assertEqual(
      binary_type(txn),

      # Note the extra 9's added to the end.
      b'JVMTDGDPDFYHMZPMWEKKANBQSLSDTIIHAYQUMZOK'
      b'HXXXGJHJDQPOMDOMNRDKYCZRUFZROZDADTHZC9999'
    )

  def test_init_error_too_long(self):
    """
    Attempting to create a transaction hash longer than 81 trytes.
    """
    with self.assertRaises(ValueError):
      # noinspection SpellCheckingInspection
      TransactionHash(
        b'JVMTDGDPDFYHMZPMWEKKANBQSLSDTIIHAYQUMZOK'
        b'HXXXGJHJDQPOMDOMNRDKYCZRUFZROZDADTHZC99999'
      )


class TransactionTestCase(TestCase):
  # noinspection SpellCheckingInspection
  def test_from_tryte_string(self):
    """
    Initializing a Transaction object from a TryteString.
    """
    # :see: http://iotasupport.com/news/index.php/2016/12/02/fixing-the-latest-solid-subtangle-milestone-issue/
    trytes =\
      TransactionTrytes(
        b'GYPRVHBEZOOFXSHQBLCYW9ICTCISLHDBNMMVYD9JJHQMPQCTIQAQTJNNNJ9IDXLRCC'
        b'OYOXYPCLR9PBEY9ORZIEPPDNTI9CQWYZUOTAVBXPSBOFEQAPFLWXSWUIUSJMSJIIIZ'
        b'WIKIRH9GCOEVZFKNXEVCUCIIWZQCQEUVRZOCMEL9AMGXJNMLJCIA9UWGRPPHCEOPTS'
        b'VPKPPPCMQXYBHMSODTWUOABPKWFFFQJHCBVYXLHEWPD9YUDFTGNCYAKQKVEZYRBQRB'
        b'XIAUX9SVEDUKGMTWQIYXRGSWYRK9SRONVGTW9YGHSZRIXWGPCCUCDRMAXBPDFVHSRY'
        b'WHGB9DQSQFQKSNICGPIPTRZINYRXQAFSWSEWIFRMSBMGTNYPRWFSOIIWWT9IDSELM9'
        b'JUOOWFNCCSHUSMGNROBFJX9JQ9XT9PKEGQYQAWAFPRVRRVQPUQBHLSNTEFCDKBWRCD'
        b'X9EYOBB9KPMTLNNQLADBDLZPRVBCKVCYQEOLARJYAGTBFR9QLPKZBOYWZQOVKCVYRG'
        b'YI9ZEFIQRKYXLJBZJDBJDJVQZCGYQMROVHNDBLGNLQODPUXFNTADDVYNZJUVPGB9LV'
        b'PJIYLAPBOEHPMRWUIAJXVQOEM9ROEYUOTNLXVVQEYRQWDTQGDLEYFIYNDPRAIXOZEB'
        b'CS9P99AZTQQLKEILEVXMSHBIDHLXKUOMMNFKPYHONKEYDCHMUNTTNRYVMMEYHPGASP'
        b'ZXASKRUPWQSHDMU9VPS99ZZ9SJJYFUJFFMFORBYDILBXCAVJDPDFHTTTIYOVGLRDYR'
        b'TKHXJORJVYRPTDH9ZCPZ9ZADXZFRSFPIQKWLBRNTWJHXTOAUOL9FVGTUMMPYGYICJD'
        b'XMOESEVDJWLMCVTJLPIEKBE9JTHDQWV9MRMEWFLPWGJFLUXI9BXPSVWCMUWLZSEWHB'
        b'DZKXOLYNOZAPOYLQVZAQMOHGTTQEUAOVKVRRGAHNGPUEKHFVPVCOYSJAWHZU9DRROH'
        b'BETBAFTATVAUGOEGCAYUXACLSSHHVYDHMDGJP9AUCLWLNTFEVGQGHQXSKEMVOVSKQE'
        b'EWHWZUDTYOBGCURRZSJZLFVQQAAYQO9TRLFFN9HTDQXBSPPJYXMNGLLBHOMNVXNOWE'
        b'IDMJVCLLDFHBDONQJCJVLBLCSMDOUQCKKCQJMGTSTHBXPXAMLMSXRIPUBMBAWBFNLH'
        b'LUJTRJLDERLZFUBUSMF999XNHLEEXEENQJNOFFPNPQ9PQICHSATPLZVMVIWLRTKYPI'
        b'XNFGYWOJSQDAXGFHKZPFLPXQEHCYEAGTIWIJEZTAVLNUMAFWGGLXMBNUQTOFCNLJTC'
        b'DMWVVZGVBSEBCPFSM99FLOIDTCLUGPSEDLOKZUAEVBLWNMODGZBWOVQT9DPFOTSKRA'
        b'BQAVOQ9RXWBMAKFYNDCZOJGTCIDMQSQQSODKDXTPFLNOKSIZEOY9HFUTLQRXQMEPGO'
        b'XQGLLPNSXAUCYPGZMNWMQWSWCKAQYKXJTWINSGPPZG9HLDLEAWUWEVCTVRCBDFOXKU'
        b'ROXH9HXXAXVPEJFRSLOGRVGYZASTEBAQNXJJROCYRTDPYFUIQJVDHAKEG9YACV9HCP'
        b'JUEUKOYFNWDXCCJBIFQKYOXGRDHVTHEQUMHO999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999RKWEEVD99A99999999A99999999NFDPEEZCWVYLKZGSLCQNOFUSENI'
        b'XRHWWTZFBXMPSQHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9PGTKORV9IKTJZQ'
        b'UBQAWTKBKZ9NEZHBFIMCLV9TTNJNQZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999'
        b'999TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJNQZUIJDFPTTCTKBJRHAITVSK'
        b'UCUEMD9M9SQJ999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999'
      )

    transaction = Transaction.from_tryte_string(trytes)

    self.assertIsInstance(transaction, Transaction)

    self.assertEqual(
      transaction.hash,

      Hash(
        b'QODOAEJHCFUYFTTPRONYSMMSFDNFWFX9UCMESVWA'
        b'FCVUQYOIJGJMBMGQSFIAFQFMVECYIFXHRGHHEOTMK'
      ),
    )

    self.assertEqual(
      transaction.signature_message_fragment,

      Fragment(
        b'GYPRVHBEZOOFXSHQBLCYW9ICTCISLHDBNMMVYD9JJHQMPQCTIQAQTJNNNJ9IDXLRCC'
        b'OYOXYPCLR9PBEY9ORZIEPPDNTI9CQWYZUOTAVBXPSBOFEQAPFLWXSWUIUSJMSJIIIZ'
        b'WIKIRH9GCOEVZFKNXEVCUCIIWZQCQEUVRZOCMEL9AMGXJNMLJCIA9UWGRPPHCEOPTS'
        b'VPKPPPCMQXYBHMSODTWUOABPKWFFFQJHCBVYXLHEWPD9YUDFTGNCYAKQKVEZYRBQRB'
        b'XIAUX9SVEDUKGMTWQIYXRGSWYRK9SRONVGTW9YGHSZRIXWGPCCUCDRMAXBPDFVHSRY'
        b'WHGB9DQSQFQKSNICGPIPTRZINYRXQAFSWSEWIFRMSBMGTNYPRWFSOIIWWT9IDSELM9'
        b'JUOOWFNCCSHUSMGNROBFJX9JQ9XT9PKEGQYQAWAFPRVRRVQPUQBHLSNTEFCDKBWRCD'
        b'X9EYOBB9KPMTLNNQLADBDLZPRVBCKVCYQEOLARJYAGTBFR9QLPKZBOYWZQOVKCVYRG'
        b'YI9ZEFIQRKYXLJBZJDBJDJVQZCGYQMROVHNDBLGNLQODPUXFNTADDVYNZJUVPGB9LV'
        b'PJIYLAPBOEHPMRWUIAJXVQOEM9ROEYUOTNLXVVQEYRQWDTQGDLEYFIYNDPRAIXOZEB'
        b'CS9P99AZTQQLKEILEVXMSHBIDHLXKUOMMNFKPYHONKEYDCHMUNTTNRYVMMEYHPGASP'
        b'ZXASKRUPWQSHDMU9VPS99ZZ9SJJYFUJFFMFORBYDILBXCAVJDPDFHTTTIYOVGLRDYR'
        b'TKHXJORJVYRPTDH9ZCPZ9ZADXZFRSFPIQKWLBRNTWJHXTOAUOL9FVGTUMMPYGYICJD'
        b'XMOESEVDJWLMCVTJLPIEKBE9JTHDQWV9MRMEWFLPWGJFLUXI9BXPSVWCMUWLZSEWHB'
        b'DZKXOLYNOZAPOYLQVZAQMOHGTTQEUAOVKVRRGAHNGPUEKHFVPVCOYSJAWHZU9DRROH'
        b'BETBAFTATVAUGOEGCAYUXACLSSHHVYDHMDGJP9AUCLWLNTFEVGQGHQXSKEMVOVSKQE'
        b'EWHWZUDTYOBGCURRZSJZLFVQQAAYQO9TRLFFN9HTDQXBSPPJYXMNGLLBHOMNVXNOWE'
        b'IDMJVCLLDFHBDONQJCJVLBLCSMDOUQCKKCQJMGTSTHBXPXAMLMSXRIPUBMBAWBFNLH'
        b'LUJTRJLDERLZFUBUSMF999XNHLEEXEENQJNOFFPNPQ9PQICHSATPLZVMVIWLRTKYPI'
        b'XNFGYWOJSQDAXGFHKZPFLPXQEHCYEAGTIWIJEZTAVLNUMAFWGGLXMBNUQTOFCNLJTC'
        b'DMWVVZGVBSEBCPFSM99FLOIDTCLUGPSEDLOKZUAEVBLWNMODGZBWOVQT9DPFOTSKRA'
        b'BQAVOQ9RXWBMAKFYNDCZOJGTCIDMQSQQSODKDXTPFLNOKSIZEOY9HFUTLQRXQMEPGO'
        b'XQGLLPNSXAUCYPGZMNWMQWSWCKAQYKXJTWINSGPPZG9HLDLEAWUWEVCTVRCBDFOXKU'
        b'ROXH9HXXAXVPEJFRSLOGRVGYZASTEBAQNXJJROCYRTDPYFUIQJVDHAKEG9YACV9HCP'
        b'JUEUKOYFNWDXCCJBIFQKYOXGRDHVTHEQUMHO999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999'
      ),
    )

    self.assertEqual(
      transaction.address,

      Address(
        b'9999999999999999999999999999999999999999'
        b'99999999999999999999999999999999999999999'
      ),
    )

    self.assertEqual(transaction.value, 0)
    self.assertEqual(transaction.tag, Tag(b'999999999999999999999999999'))
    self.assertEqual(transaction.timestamp, 1480690413)
    self.assertEqual(transaction.current_index, 1)
    self.assertEqual(transaction.last_index, 1)

    self.assertEqual(
      transaction.bundle_hash,

      BundleHash(
        b'NFDPEEZCWVYLKZGSLCQNOFUSENIXRHWWTZFBXMPS'
        b'QHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9PG'
      ),
    )

    self.assertEqual(
      transaction.trunk_transaction_hash,

      TransactionHash(
        b'TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJN'
        b'QZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999999'
      ),
    )

    self.assertEqual(
      transaction.branch_transaction_hash,

      TransactionHash(
        b'TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJN'
        b'QZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999999'
      ),
    )

    self.assertEqual(
      transaction.nonce,

      Hash(
        b'9999999999999999999999999999999999999999'
        b'99999999999999999999999999999999999999999'
      ),
    )

  def test_from_tryte_string_with_hash(self):
    """
    Initializing a Transaction object from a TryteString, with a
    pre-computed hash.
    """
    # noinspection SpellCheckingInspection
    txn_hash =\
      TransactionHash(
        b'TESTVALUE9DONTUSEINPRODUCTION99999VALCXC'
        b'DHTDZBVCAAIEZCQCXGEFYBXHNDJFZEBEVELA9HHEJ'
      )

    txn = Transaction.from_tryte_string(b'', hash_=txn_hash)

    self.assertEqual(txn.hash, txn_hash)

  # noinspection SpellCheckingInspection
  def test_as_tryte_string(self):
    """
    Converting a Transaction into a TryteString.
    """
    transaction = Transaction(
      hash_ =
        TransactionHash(
          b'QODOAEJHCFUYFTTPRONYSMMSFDNFWFX9UCMESVWA'
          b'FCVUQYOIJGJMBMGQSFIAFQFMVECYIFXHRGHHEOTMK'
        ),

      signature_message_fragment =
        Fragment(
          b'GYPRVHBEZOOFXSHQBLCYW9ICTCISLHDBNMMVYD9JJHQMPQCTIQAQTJNNNJ9IDXLRCC'
          b'OYOXYPCLR9PBEY9ORZIEPPDNTI9CQWYZUOTAVBXPSBOFEQAPFLWXSWUIUSJMSJIIIZ'
          b'WIKIRH9GCOEVZFKNXEVCUCIIWZQCQEUVRZOCMEL9AMGXJNMLJCIA9UWGRPPHCEOPTS'
          b'VPKPPPCMQXYBHMSODTWUOABPKWFFFQJHCBVYXLHEWPD9YUDFTGNCYAKQKVEZYRBQRB'
          b'XIAUX9SVEDUKGMTWQIYXRGSWYRK9SRONVGTW9YGHSZRIXWGPCCUCDRMAXBPDFVHSRY'
          b'WHGB9DQSQFQKSNICGPIPTRZINYRXQAFSWSEWIFRMSBMGTNYPRWFSOIIWWT9IDSELM9'
          b'JUOOWFNCCSHUSMGNROBFJX9JQ9XT9PKEGQYQAWAFPRVRRVQPUQBHLSNTEFCDKBWRCD'
          b'X9EYOBB9KPMTLNNQLADBDLZPRVBCKVCYQEOLARJYAGTBFR9QLPKZBOYWZQOVKCVYRG'
          b'YI9ZEFIQRKYXLJBZJDBJDJVQZCGYQMROVHNDBLGNLQODPUXFNTADDVYNZJUVPGB9LV'
          b'PJIYLAPBOEHPMRWUIAJXVQOEM9ROEYUOTNLXVVQEYRQWDTQGDLEYFIYNDPRAIXOZEB'
          b'CS9P99AZTQQLKEILEVXMSHBIDHLXKUOMMNFKPYHONKEYDCHMUNTTNRYVMMEYHPGASP'
          b'ZXASKRUPWQSHDMU9VPS99ZZ9SJJYFUJFFMFORBYDILBXCAVJDPDFHTTTIYOVGLRDYR'
          b'TKHXJORJVYRPTDH9ZCPZ9ZADXZFRSFPIQKWLBRNTWJHXTOAUOL9FVGTUMMPYGYICJD'
          b'XMOESEVDJWLMCVTJLPIEKBE9JTHDQWV9MRMEWFLPWGJFLUXI9BXPSVWCMUWLZSEWHB'
          b'DZKXOLYNOZAPOYLQVZAQMOHGTTQEUAOVKVRRGAHNGPUEKHFVPVCOYSJAWHZU9DRROH'
          b'BETBAFTATVAUGOEGCAYUXACLSSHHVYDHMDGJP9AUCLWLNTFEVGQGHQXSKEMVOVSKQE'
          b'EWHWZUDTYOBGCURRZSJZLFVQQAAYQO9TRLFFN9HTDQXBSPPJYXMNGLLBHOMNVXNOWE'
          b'IDMJVCLLDFHBDONQJCJVLBLCSMDOUQCKKCQJMGTSTHBXPXAMLMSXRIPUBMBAWBFNLH'
          b'LUJTRJLDERLZFUBUSMF999XNHLEEXEENQJNOFFPNPQ9PQICHSATPLZVMVIWLRTKYPI'
          b'XNFGYWOJSQDAXGFHKZPFLPXQEHCYEAGTIWIJEZTAVLNUMAFWGGLXMBNUQTOFCNLJTC'
          b'DMWVVZGVBSEBCPFSM99FLOIDTCLUGPSEDLOKZUAEVBLWNMODGZBWOVQT9DPFOTSKRA'
          b'BQAVOQ9RXWBMAKFYNDCZOJGTCIDMQSQQSODKDXTPFLNOKSIZEOY9HFUTLQRXQMEPGO'
          b'XQGLLPNSXAUCYPGZMNWMQWSWCKAQYKXJTWINSGPPZG9HLDLEAWUWEVCTVRCBDFOXKU'
          b'ROXH9HXXAXVPEJFRSLOGRVGYZASTEBAQNXJJROCYRTDPYFUIQJVDHAKEG9YACV9HCP'
          b'JUEUKOYFNWDXCCJBIFQKYOXGRDHVTHEQUMHO999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999999999999999999999999999999999999999999999999999999999999'
          b'999999999'
        ),

      address =
        Address(
          b'9999999999999999999999999999999999999999'
          b'99999999999999999999999999999999999999999'
        ),

      value         = 0,
      tag           = Tag(b'999999999999999999999999999'),
      timestamp     = 1480690413,
      current_index = 1,
      last_index    = 1,

      bundle_hash =
        BundleHash(
          b'NFDPEEZCWVYLKZGSLCQNOFUSENIXRHWWTZFBXMPS'
          b'QHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9PG'
        ),

      trunk_transaction_hash =
        TransactionHash(
          b'TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJN'
          b'QZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999999'
        ),

      branch_transaction_hash =
        TransactionHash(
          b'TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJN'
          b'QZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999999'
        ),

      nonce =
        Hash(
          b'9999999999999999999999999999999999999999'
          b'99999999999999999999999999999999999999999'
        ),
    )

    self.assertEqual(
      transaction.as_tryte_string(),

      TransactionTrytes(
        b'GYPRVHBEZOOFXSHQBLCYW9ICTCISLHDBNMMVYD9JJHQMPQCTIQAQTJNNNJ9IDXLRCC'
        b'OYOXYPCLR9PBEY9ORZIEPPDNTI9CQWYZUOTAVBXPSBOFEQAPFLWXSWUIUSJMSJIIIZ'
        b'WIKIRH9GCOEVZFKNXEVCUCIIWZQCQEUVRZOCMEL9AMGXJNMLJCIA9UWGRPPHCEOPTS'
        b'VPKPPPCMQXYBHMSODTWUOABPKWFFFQJHCBVYXLHEWPD9YUDFTGNCYAKQKVEZYRBQRB'
        b'XIAUX9SVEDUKGMTWQIYXRGSWYRK9SRONVGTW9YGHSZRIXWGPCCUCDRMAXBPDFVHSRY'
        b'WHGB9DQSQFQKSNICGPIPTRZINYRXQAFSWSEWIFRMSBMGTNYPRWFSOIIWWT9IDSELM9'
        b'JUOOWFNCCSHUSMGNROBFJX9JQ9XT9PKEGQYQAWAFPRVRRVQPUQBHLSNTEFCDKBWRCD'
        b'X9EYOBB9KPMTLNNQLADBDLZPRVBCKVCYQEOLARJYAGTBFR9QLPKZBOYWZQOVKCVYRG'
        b'YI9ZEFIQRKYXLJBZJDBJDJVQZCGYQMROVHNDBLGNLQODPUXFNTADDVYNZJUVPGB9LV'
        b'PJIYLAPBOEHPMRWUIAJXVQOEM9ROEYUOTNLXVVQEYRQWDTQGDLEYFIYNDPRAIXOZEB'
        b'CS9P99AZTQQLKEILEVXMSHBIDHLXKUOMMNFKPYHONKEYDCHMUNTTNRYVMMEYHPGASP'
        b'ZXASKRUPWQSHDMU9VPS99ZZ9SJJYFUJFFMFORBYDILBXCAVJDPDFHTTTIYOVGLRDYR'
        b'TKHXJORJVYRPTDH9ZCPZ9ZADXZFRSFPIQKWLBRNTWJHXTOAUOL9FVGTUMMPYGYICJD'
        b'XMOESEVDJWLMCVTJLPIEKBE9JTHDQWV9MRMEWFLPWGJFLUXI9BXPSVWCMUWLZSEWHB'
        b'DZKXOLYNOZAPOYLQVZAQMOHGTTQEUAOVKVRRGAHNGPUEKHFVPVCOYSJAWHZU9DRROH'
        b'BETBAFTATVAUGOEGCAYUXACLSSHHVYDHMDGJP9AUCLWLNTFEVGQGHQXSKEMVOVSKQE'
        b'EWHWZUDTYOBGCURRZSJZLFVQQAAYQO9TRLFFN9HTDQXBSPPJYXMNGLLBHOMNVXNOWE'
        b'IDMJVCLLDFHBDONQJCJVLBLCSMDOUQCKKCQJMGTSTHBXPXAMLMSXRIPUBMBAWBFNLH'
        b'LUJTRJLDERLZFUBUSMF999XNHLEEXEENQJNOFFPNPQ9PQICHSATPLZVMVIWLRTKYPI'
        b'XNFGYWOJSQDAXGFHKZPFLPXQEHCYEAGTIWIJEZTAVLNUMAFWGGLXMBNUQTOFCNLJTC'
        b'DMWVVZGVBSEBCPFSM99FLOIDTCLUGPSEDLOKZUAEVBLWNMODGZBWOVQT9DPFOTSKRA'
        b'BQAVOQ9RXWBMAKFYNDCZOJGTCIDMQSQQSODKDXTPFLNOKSIZEOY9HFUTLQRXQMEPGO'
        b'XQGLLPNSXAUCYPGZMNWMQWSWCKAQYKXJTWINSGPPZG9HLDLEAWUWEVCTVRCBDFOXKU'
        b'ROXH9HXXAXVPEJFRSLOGRVGYZASTEBAQNXJJROCYRTDPYFUIQJVDHAKEG9YACV9HCP'
        b'JUEUKOYFNWDXCCJBIFQKYOXGRDHVTHEQUMHO999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999999999999999999999999999999999999'
        b'999999999999RKWEEVD99A99999999A99999999NFDPEEZCWVYLKZGSLCQNOFUSENI'
        b'XRHWWTZFBXMPSQHEDFWZULBZFEOMNLRNIDQKDNNIELAOXOVMYEI9PGTKORV9IKTJZQ'
        b'UBQAWTKBKZ9NEZHBFIMCLV9TTNJNQZUIJDFPTTCTKBJRHAITVSKUCUEMD9M9SQJ999'
        b'999TKORV9IKTJZQUBQAWTKBKZ9NEZHBFIMCLV9TTNJNQZUIJDFPTTCTKBJRHAITVSK'
        b'UCUEMD9M9SQJ999999999999999999999999999999999999999999999999999999'
        b'999999999999999999999999999999999',
      ),
    )


class UnitConverterTestCase(TestCase):

  def test_convert_to_smaller_unit(self):
    """
    Converting to smaller unit.
    """
    self.assertEqual(convert_value_to_standard_unit('1.618 Mi', 'i'), 1618000)

  def test_convert_to_bigger_unit(self):
    """
    Converting to bigger unit.
    """
    self.assertEqual(convert_value_to_standard_unit('42 i', 'Ki'), 0.042)

  def test_convert_to_same_size_unit(self):
    """
    Converting to unit of same size.
    """
    self.assertEqual(
      convert_value_to_standard_unit('299792458 Mi', 'Mi'),
      299792458,
    )

  def test_convert_from_invalid_symbol(self):
    """
    Attempting conversion from value suffixed with invalid symbol.
    """
    with self.assertRaises(ValueError):
      convert_value_to_standard_unit('3.141592 Xi', 'Pi')

  def test_convert_to_invalid_symbol(self):
    """
    Attempting conversion to invalid symbol.
    """
    with self.assertRaises(ValueError):
      convert_value_to_standard_unit('3.141592 Pi', 'Xi')

  def test_convert_type_list(self):
    """
    Attempting to convert invalid type: list.
    """
    with self.assertRaises(ValueError):
      # noinspection PyTypeChecker
      convert_value_to_standard_unit(['3.141592', 'Pi'], 'Gi')

  def test_convert_type_float(self):
    """
    Attempting to convert invalid type: float.
    """
    with self.assertRaises(ValueError):
      # noinspection PyTypeChecker
      convert_value_to_standard_unit(3.141592, 'Pi')

  def test_convert_value_no_space(self):
    """
    Attempting to convert value missing a space separating amount and suffix.
    """
    with self.assertRaises(ValueError):
      convert_value_to_standard_unit('3.141592Pi', 'Gi')

  def test_convert_fractional_iotas(self):
    """
    Converting from/to fractional iotas.
    """
    self.assertEqual(convert_value_to_standard_unit('1.6182 Ki', 'i'), 1618.2)

  def test_convert_negative_values(self):
    """
    Converting negative values.
    """
    self.assertEqual(convert_value_to_standard_unit('-1.618 Ki', 'i'), -1618)

  def test_convert_wrong_case_symbol(self):
    """
    Attempting to convert value containing suffix specified with wrong case.
    """
    with self.assertRaises(ValueError):
      convert_value_to_standard_unit('3.141592 pI', 'Gi')
