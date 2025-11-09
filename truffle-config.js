module.exports = {
  networks: {
    development: {
      host: "192.168.1.72",  // Ganache PC IP
      port: 7545,
      network_id: "*"
    }
  },
  compilers: { solc: { version: "0.8.17" } }
};
