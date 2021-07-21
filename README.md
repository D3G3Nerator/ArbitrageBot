# ArbitrageBot
A Python Bot which detects Arbitrage opportunities in Decentralized Exchanges.

## Intro
This script will detect Arbitrage Opportunities in Decentralized Markets (via the `0x` protocol, and the `1inch` exchange aggregator).

Arbitrage Opportunities are logged in an intutive instruction format:

<img width="713" alt="Screenshot 2021-07-21 at 12 26 50" src="https://user-images.githubusercontent.com/44982443/126481550-170a1b29-2f31-4eb1-843a-ebbf061f189a.png">

(Just an example. A real Arbitrage Opportunity would have a positive profit)

Eventually, the script will be able to forward said instructions linked to a Flashloan Capable Smart Contract.

The script implements nested multi-threading, for speed purposes (but can still be improved).
