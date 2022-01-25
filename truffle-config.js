const HDWalletProvider = require("@truffle/hdwallet-provider");
const mnemonic = 'hip carry despair senior try borrow scorpion worry mango soccer approve depth'

module.exports = {
  networks: {
    ropsten: {
      provider: function() {
        return new HDWalletProvider(mnemonic, "https://ropsten.infura.io/v3/2f93f099906e46a58e16e7d93fa4d2de")
      },
      network_id: 3
    },
    development: {
      host: "127.0.0.1",
      port: 7545,     // Ganache
      network_id: "*" // Match any network id
    },
    develop: {
      port: 8545
    }
  }
};
