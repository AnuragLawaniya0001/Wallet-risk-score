🧠 Overview
This project analyzes a list of Ethereum wallet addresses and assigns each one a risk score between 0 and 1000 based on various wallet activity indicators. The risk score reflects how active, trustworthy, and DeFi-engaged the wallet appears to be.

📥 1. Data Collection Method
We use the Ethplorer API (freekey access) to fetch public on-chain wallet information, including:

ETH balance

Token holdings

Transaction count

Wallet creation date (if available)

Interaction with known DeFi tokens

Each wallet from wallet_list.txt is queried individually, and the resulting data is used for scoring.

📊 2. Feature Selection Rationale
We chose wallet-level features that are publicly available and commonly used to evaluate a wallet’s activity and risk profile:

Feature	Why it matters
ETH Balance	Active wallets typically hold ETH for gas and transactions
Token Holdings	Wallets that hold tokens are more engaged in the ecosystem
Transaction Count	Frequent transactions indicate real user behavior (vs dormant wallets)
Wallet Age	Older wallets are less likely to be scams or bots
DeFi Token Exposure	Usage of protocols like Aave, Uniswap, Compound is a strong sign of DeFi participation

⚖️ 3. Scoring Method
✅ Current (Working) Logic
Each wallet starts with a score of 0 and earns points based on activity indicators:

Condition	Points
ETH balance > 0	+200
Holds any tokens	+150
More than 10 transactions	+150
Wallet older than 1 year	+200
Holds DeFi tokens (Aave, Compound, Uniswap, Maker)	+300
Max Score	1000

This logic is simple, scalable, and works across most public wallets.

❌ Why the First Logic Was Rejected
Initially, we attempted to use a DeFi protocol-specific API (expand.network) to check wallet interaction with protocols like Aave (e.g., borrow/lend balance).

Problems faced:
Data Inconsistency: Some wallet queries returned empty or missing fields

403/400 Errors: The endpoint often required authentication or query parameters that failed silently

Unreliable Response Format: Even valid responses returned data: [], making it impossible to determine if it was an error or an inactive wallet

As a result, risk scores were always 0, even for active wallets.

➡️ Final Decision
We switched to a wallet-level analysis using Ethplorer, which ensures:

Consistent and parsable JSON structure

Reliable scoring across all wallets

No authentication barriers for testing

📈 4. Justification of Risk Indicators
We based our scoring on common-sense indicators of wallet trust:

No ETH = low chance of real user behavior

No tokens or txns = dormant or spam wallet

DeFi exposure = sophisticated or power user

New wallet = higher risk of rug pulls or flash attacks

This scoring framework allows simple extensibility — you can add more points for things like NFT ownership, gas usage, or DAO participation in future versions.

✅ Final Output
The final output is saved in wallet_scores.csv with this structure:


wallet_address,score
0xabc123...,850
0xdeadbeef...,100
0xnewwallet...,0
Each score reflects how healthy and active the wallet appears.

