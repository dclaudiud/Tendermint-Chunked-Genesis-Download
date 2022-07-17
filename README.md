# Tendermint Chunked Genesis Download

A library to easily download a chunked genesis from a Tendermint chain (eg: Cosmos). Access to an RPC enabled node is required. It is usually running on port 26657 (eg: local node address 127.0.0.1:26657).

## Install

`pip install tendermint-chunked-genesis-download`

## Usage

Import the `tendermint_chunked_genesis_download` package and call the `download_genesis(url)` function. Provide a valid Tendermint RPC url as a parameter to the function.

```
import tendermint_chunked_genesis_download as tcgd

ccgd.download_genesis('https://evmos-rpc.evmosis.com')
```

## Using from command line

```
tendermint-chunked-genesis-download TENDERMINT_RPC_URL
```

## Exceptions

| Name                    | Reason                                                    |
|-------------------------|-----------------------------------------------------------|
| InvalidRPC              | The Tendermint RPC url is invalid                         |
| NodeNotSynchronized     | The Tendermint node is not yet fully synchronized         |
| UnsuccessfulHttpRequest | The node request has not returned a 2XX HTTP success code |

## Dependencies

Python libraries which helped:

* [requests](https://pypi.org/project/requests/)
* [click](https://pypi.org/project/click/)
* [setuptools](https://pypi.org/project/setuptools/)

## Projects that use the genesis download library

* [Evmosis liquid staking module for Evmos](https://evmosis.com/)