# ArbitrageBot
A Python Bot which detects Arbitrage opportunities in Decentralized Exchanges.

This Python script will detect Arbitrage Opportunities in Decentralized Markets (via the 0x protocol, and the 1inch exchange aggregator).
When an Arbitrage Opportunity is detected, it is printed in an intutive instruction format, as such:

The script will eventually be linked to a Flashloan Smart Contract (capable of receiving said instructions and taking advantage of the detected opportunities).

The script implements nested multi-threading, for speed purposes (but can still be improved).
