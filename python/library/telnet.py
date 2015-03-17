from expect import expect


class telnet(expect):
    def __init__(self, ipaddr, login, password, prompt = '>'):
        self.TELNET_PROMPT = prompt

        expect.__init__(self, 'telnet ' + ipaddr)
        expect.expect(self, 'login:')
        expect.send_expect(self, login, 'Password')
        expect.send_expect(self, password, self.TELNET_PROMPT)


    def run(self, cmd):
        expect.send_expect(self, cmd, self.TELNET_PROMPT)
        


if __name__ == "__main__":
    tel = telnet('10.220.0.51', 'infinera', 'infinera2', '\$')
    tel.run('ls')
    tel.run('ls -l')
    tel.send_expect('ls /tmp', '\$')

