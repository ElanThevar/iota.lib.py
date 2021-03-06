# coding=utf-8
"""
Example script that shows how to use PyOTA to send a transfer to an address.
"""
from iota import *

SEED1 = b"THESEEDOFTHEWALLETSENDINGGOESHERE999999999999999999999999999999999999999999999999"
ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2 = b"RECEIVINGWALLETADDRESSGOESHERE9WITHCHECKSUMANDSECURITYLEVEL2999999999999999999999999999999"

# Create the API instance.
api =\
  Iota(
    # URI of a locally running node.
    'http://localhost:14265/',

    # Seed used for cryptographic functions.
    seed = SEED1
  )

# For more information, see :py:meth:`Iota.send_transfer`.
api.send_transfer(
  depth = 100,

  # One or more :py:class:`ProposedTransaction` objects to add to the
  # bundle.
  transfers = [
    ProposedTransaction(
      # Recipient of the transfer.
      address =
        Address(
          ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2,
        ),

      # Amount of IOTA to transfer.
      # This value may be zero.
      value = 1,

      # Optional tag to attach to the transfer.
      tag = Tag(b'EXAMPLE'),

      # Optional message to include with the transfer.
      message = TryteString.from_string('Hello!'),
    ),
  ],
)
