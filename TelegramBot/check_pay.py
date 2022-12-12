from bscscan import BscScan
import config as cfg
import aiohttp


async def check_bep20_txs_status(txhash: str) -> bool:
    '''returns True if transaction OKAY, else False'''
    async with BscScan('84NBSBD1U1AQ4Q89G53A5JCT8RU4FQU56C') as client:
        res = await client.get_bep20_token_transfer_events_by_address(
            address=cfg.payAdress_bep20,
            startblock=0,
            endblock=999999999,
            sort='asc')
        for i in res:
            if i['hash'] == txhash:
                if i['contractAddress'] == cfg.USDTcontractAddress_bep20:
                    if (i['to']).lower() == cfg.payAdress_bep20:
                        USDT = (int(i['value']) / 1000000000000000000)
                        if USDT >= cfg.amount:
                            return True
        return False


async def check_trc20_txs_status(txhash: str) -> bool:
    '''https://github.com/tronscan/tronscan-frontend/blob/dev2019/document/api.md
    return True if transaction OKAY, else False'''
    url = f'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=20&start=0&address={cfg.payAdress_trc20}'
    async with aiohttp.request(method='GET', url=url) as resp:
        data = (await resp.json())['data']
    for trans in data:
        if trans['hash'] == txhash:
            value = int(trans['trigger_info']['parameter']['_value']) / 10 ** 6
            reciever = trans['trigger_info']['parameter']['_to']
            contract_adress_USDT = trans['trigger_info']['contract_address']
            if contract_adress_USDT == cfg.USDTcontractAddress_trc20:
                if reciever == cfg.payAdress_trc20:
                    if value >= cfg.amount:
                        return True
    return False
