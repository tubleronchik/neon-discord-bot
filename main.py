import discord
from web3_helper import setup_provider, get_contract, transfer
from utils import read_config
import web3

client = discord.Client(heartbeat_timeout=120)
config = read_config()
w3 = setup_provider(config["http_node_provider"], config["owner_pk"])
xrt = get_contract(w3, config["xrt_contract_address"])

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == config['guild']:
            break
    print(
        f'{client.user} is connected to the {guild.name}\n'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.channel) == config['channel']:
        print(f"Got message: {message}")
        print(f"Got message content: {message.content}")
        mes = str(message.content).split()
        for word in mes:
            word = word.strip()
            if web3.Web3.isAddress(word):
                address = word
                tx_hash = await transfer(xrt, w3, address, config["xrt_owner"], config["amount"])
                if tx_hash:
                    await message.channel.send(f"XRT to Address {address} from {message.author} was sent. Tx hash: {tx_hash}")
                else:
                    await message.channel.send(f"Couldn't send XRT to {address} from {message.author}.\n Please, send your address again")
                break
            else:
                await message.channel.send(f"Message {word} from {message.author} is not one of the recognized address formats. Please, provide correct address.")

if __name__ == '__main__':
    client.run(config['token'])