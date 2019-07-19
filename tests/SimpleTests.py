from teddi import *


class SimpleTests(TestSuite):

    @Test
    async def MessageSendAndRetrieveTest(self):
        Logger.logStep('Send a message')
        await self.teddi.send_message('Hello, world!')

        Logger.logStep('Get message and verify is correct')
        text = await self.teddi.get_last_message(self.teddi.client.user)

        assertEqual(text, 'Hello, world!', fail=f'Last message was \'{text}\' not \'Hello, world!\'', success='Message is correct')

    @Test
    async def UptimeTest(self):
        Logger.logStep('Send command .uptime')
        await self.teddi.send_message('.uptime')

        Logger.logStep('Wait for response')
        await self.teddi.client.wait_for('message', timeout=5)

        Logger.logStep('Get RoBot response')
        text = await self.teddi.get_last_message()

        Logger.logStep('Validate response')
        try:
            assertTrue('uptime' in text.lower(), fail='RoBot sent an unexpexted response', success='Robot response is correct')
        except AssertTrueException as e:
            await self.teddi.send_message('Robot response is incorrect')
            raise e
        await self.teddi.send_message('Robot response is correct')


if __name__ == '__main__':
    teddi = Teddi('NjAxNjE3NDkxNDQ5MzQ4MTI2.XTFNSA.SYdGnLGNOYclsCB0J6D7KLUZDMk')
    teddi.add_suite(SimpleTests)
    teddi.connect()
