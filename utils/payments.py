from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.const import Assets
import asyncio
from config import PAY_TOKEN


async def gen_pay_url(price:float):
    cryptopay = AioCryptoPay(PAY_TOKEN, network=Networks.MAIN_NET)
    invoice = await cryptopay.create_invoice(
        asset=Assets.TON,
        amount=price
        )
    await cryptopay.close()
    return invoice.bot_invoice_url , invoice.invoice_id

async def check_pay(check_id):
    cryptopay = AioCryptoPay(PAY_TOKEN, network=Networks.MAIN_NET)
    invoice = await cryptopay.get_invoices(invoice_ids=[check_id,])
    await cryptopay.close()
    if invoice[0].status == "paid":
        return True
    return False

async def main():
    check_id = await gen_pay_url(1)
    await check_pay(check_id[-1])

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())