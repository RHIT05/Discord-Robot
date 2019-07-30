from teddi import *
import sys
import secrets


class PermissionsModuleTests(TestSuite):

    @Test
    async def GivePermissionTest(self):
        await self.clearPerms()

        Logger.logStep('Generate random permission')
        perm = secrets.token_hex(8)

        await self.givePerm(perm)

        Logger.logStep('Check output of .perms for permission')
        text = await self.getPerms()

        Logger.logStep('Check that permission is in RoBot output')
        assertTrue(perm in text, fail='Permission was not given', success='Permission given correctly')

    async def clearPerms(self):
        Logger.logStep('Clear permissions')
        text = await self.send_cmd_get_reply(f'.clearperms {self.teddi.client.user.mention}')

        Logger.logStep('Check that RoBot replied correctly')
        assertEqual(text, f'Permissions cleared for {self.teddi.client.user.name}.')

        text = await self.getPerms()

        Logger.logStep('Check that RoBot replied correctly')
        expected = f'Here are your current permissions, {self.teddi.client.user.mention}\n```\n\n```'
        assertEqual(text, expected, fail=f'Output of .perms was unexpected, clearperms did not work', success='Permissions properly cleared')

    async def givePerm(self, perm):
        Logger.logStep('Give permission to Teddi')
        text = await self.send_cmd_get_reply(f'.giveperm {perm} {self.teddi.client.user.mention}')

        Logger.logStep('Check that RoBot replied correctly')
        assertEqual(text, f'Gave permission \'{perm}\' to {self.teddi.client.user.name}.')

    async def getPerms(self):
        return await self.send_cmd_get_reply('.perms')

    async def send_cmd_get_reply(self, cmd):
        Logger.logStep(f'Send command: {cmd}')
        await self.teddi.send_message(cmd)

        Logger.logStep('Wait for response')
        await self.teddi.client.wait_for('message', timeout=5)

        Logger.logStep('Get RoBot response')
        return await self.teddi.get_last_message()


if __name__ == '__main__':
    teddi = Teddi(sys.argv[1])
    teddi.add_suite(PermissionsModuleTests)
    teddi.connect()
