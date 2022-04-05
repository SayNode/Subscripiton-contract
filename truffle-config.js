module.exports = {
  networks: {
      development: {
          host: "localhost",
          port: 8545,
          network_id: "*", // Match any network id
          skipDryRun: true,
          production: true,
          gasPrice: 128
      }
  },
  compilers: {
    solc: {
      version: "0.8.13"
    }
  }
};