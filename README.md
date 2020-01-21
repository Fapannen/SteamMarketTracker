# SteamMarketTracker
Python script that scans Steam Marketplace for the lowest price of your desired item

Script asks you to enter search query ( like you would on https://steamcommunity.com/market/ ), then keeps scanning the lowest prices and keeps you informed.
Currently more items at once are supported but not optimized properly.

## TBD
- Implement optimization for more items
- Implement more in-depth details and statistics
- Parsing is too complex, incorporating html parser might work better ( soup was fishy tho )
- Overall general redundant complexity of the code
- Prevent script crash when Steam is unavailable

## Dependencies
- Http requests ( pip install requests )
