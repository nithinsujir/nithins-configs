import ftplib
from expect import expect


class ftp(expect):
    FTP_PROMPT = 'ftp>'

    def __init__(self, ipaddr, login, password):

        expect.__init__(self, 'ftp ' + ipaddr)
        expect.expect(self, 'Name')
        expect.send_expect(self, login, 'Password')
        expect.send_expect(self, password, self.FTP_PROMPT)


    def run(self, cmd, time_out = None):
        expect.send_expect(self, cmd, self.FTP_PROMPT, time_out)
        


if __name__ == "__main__":
    ft = ftp('10.220.0.51', 'infinera', 'infinera2')
    ft.run('ls')
