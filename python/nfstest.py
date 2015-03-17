#!/usr/bin/python
import os
import pexpect
import sys
import optparse
import re
import thread
threading._DummyThread._Thread__stop = lambda x: 42

PASSWORD = 'broadcom'

parser = optparse.OptionParser()
parser.add_option('-s', '--server', dest='nfsserver', help='NFS Server')
parser.add_option('-c', '--client', dest='nfsclient', help='NFS Client')

(opts, args) = parser.parse_args()

if not opts.nfsserver or not opts.nfsclient:
	parser.print_help()
	sys.exit(1)

def send_expect(sess, line, prompt, timeout_ = 30):
	sess.sendline(line)
	sess.timeout = timeout_
	sess.expect(prompt)

def umount_nfs(ses):
		send_expect(ses, 'umount /media/nfs', '#')

def mount_nfs(ses):
		send_expect(ses, 'umount /media/nfs', '#')
		send_expect(ses, 'mkdir -p /media/nfs', '#')
		send_expect(ses, 'mount -t nfs ' + opts.nfsserver + ':/opt/share /media/nfs', '#')
		send_expect(ses, 'mount', 'type nfs')
		
# The expect for 'type nfs' leaves the prompt '#' in the buffer which will interfere with the next expect. Consume it.
		ses.expect('#')
		send_expect(ses, 'mkdir -p /media/nfs/' + opts.nfsclient, '#')

def spawn_ssh(target):
	child = pexpect.spawn('ssh root@' + target, timeout = 1000)
	child.logfile_read = sys.stdout

	index = child.expect(['password:', 'continue'])

	if index == 1:
		send_expect(child, 'yes', 'password')

	send_expect(child, PASSWORD, '#')

	return child

def nfstest(client, server, iterations):
	i = 0
	while i < iterations:
		i = i + 1
		print 'Start test iteration %d on %s' % (i, client)
		ses = spawn_ssh(opts.nfsclient)

		print 'Client %s mount nfs share' % client
		mount_nfs(ses);

		# Save md5sum from file
		ses.sendline('ls ~/*ig')
		ses.expect('#')
		lines = ses.before + ses.after
		m = re.search(r'/root/(.*).big', lines, re.MULTILINE)
		md5 = m.group(1)
		print 'Recorded md5sum ' + md5

		# Copy file over
		print 'Client %s copying file over ...' % client
		send_expect(ses, 'rm -f /media/nfs/' + opts.nfsclient + '/*', '#')
		send_expect(ses, 'cp /root/*ig /media/nfs/' + opts.nfsclient + '/', '#', 1000)

		lines = ses.before + ses.after

# Recalculate md5sum
		print 'Recalculating md5 on the nfs share...'
		ses.sendline('md5sum /media/nfs/' + opts.nfsclient + '/*')
		ses.expect('big', timeout = 1000)
		lines = ses.before + ses.after

		m = re.search(md5 + '.*' + md5 + '.big', lines, re.MULTILINE)

		if not m:
			print 'md5 does not match. Expected ' + md5 + '. Calculated ' + md5_new
			sys.exit(1)
		else:
			print 'Success!'

		umount_nfs(ses);
		ses.close()

gbl_stop = False
if len(nfsclient_grp1) == 0:
	nfsclient(opts.nfsclient, opts.nfsserver, 1000)
else:
	for nfsclient in nfsclient_grp1:
		try:
			thread.start_new_thread(nfstest, ((nfsclient, nfsserver1, 1000)))
		except:
			print 'failed to start test thread for client %s' % nfsclient
			sys.exit(2)
