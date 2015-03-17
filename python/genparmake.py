import os
import re
import sys
import tempfile

STATE_IDLE       =  1
STATE_SUBDIR     =  2
C_CPU = os.getenv('C_CPU')

dirs = ['mcm', 'component']

subdirdeps = {}
makelist = []
libnames = {}


blacklist = { 'component/scaffold':0,
            }

def del_duplicates(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)

    return new_list

def get_subdirs(makedir):
    try:
        fil = open(makedir + '/Makefile', 'r')
    except IOError:
        # Ignore error
        return []

    state = STATE_IDLE
    vname = ''
    variables = {}
    subdirs = ''

    # Process this makefile
    #print 'Processing: ' + makedir
    makedir = re.sub('\./', '', makedir)
    makedir = re.sub('/', '_', makedir)
    makedir = re.sub('_$', '', makedir)

    while True:
        if state == STATE_IDLE:
            line = fil.readline()

            if line == '':
                break

            # ignore comments
            if re.match('^#.*', line):
                continue

            m = re.search(r'SUBDIRS(.*)', line)

            if m:
                state = STATE_SUBDIR

        elif state == STATE_SUBDIR:
            subdirs = subdirs + line

            # If there is \ at the end of line stay in SUBDIR state
            # else move to IDLE
            if re.search(r'\\$', line):
                line = fil.readline()
            else:
                state = STATE_IDLE

            
    fil.close()

    subdirs = re.sub(r'\n', '', subdirs)
    subdirs = re.sub(r'\\', '', subdirs)
    subdirs = re.sub(r':=', '', subdirs)
    subdirs = re.sub(r'BIN_SUBDIRS', '', subdirs)
    subdirs = re.sub(r'SO_SUBDIRS', '', subdirs)
    subdirs = re.sub(r'SUBDIRS', '', subdirs)
    subdirs = re.sub(r'\$\(\)', '', subdirs)
    subdirs = re.sub(r'\s+', ' ', subdirs)
    subdirs = re.sub(r'^\s', '', subdirs)
    subdirs = re.sub(r'\s$', '', subdirs)
    subdirs = re.sub(r'\+=', '', subdirs)
    subdirs = re.sub(r'#', '', subdirs)
    subdirs = re.sub(r'w32', '', subdirs)

    if subdirs == '':
        return []

    subdirs = del_duplicates(subdirs.split(' '))

    try:
        subdirs.remove('')
    except ValueError:
        pass

    return subdirs


def list_makefiles():
    fil = open('makefiles.txt', 'w')
    while len(dirs) > 0:
        dirname = dirs.pop(0)
        #print 'Processing ' + dirname

        fil.write(os.path.join(dirname, 'Makefile') + '\n')
        subdirs = get_subdirs(dirname)
        #print subdirs

        for subdir in subdirs:
            newdir = os.path.join(dirname, subdir)

            if blacklist.has_key(newdir):
                #print newdir + ' blacklisted'
                pass
            else:
                dirs.append(newdir)

    fil.close()


def add_makefile(makedir):
    if blacklist.has_key(makedir):
        print makedir + ' blacklisted'
        return

    # Skip win32
    if re.search('win32', makedir) or re.search('w32',makedir):
        print 'Skipping win32/w32 ' + makedir
        return

    
    # Skip ppc
    if C_CPU == 'x86':
        if re.search('ppc', makedir):
            print 'Skipping ppc ' + makedir
            return


    makelist.append(makedir)

    #parent = os.path.dirname(makedir)
    #if not parent ==  '':
    #    subdirdeps[parent].append(makedir)


def walk_callback(arg, directory, files):
    try:
        fil = open(os.path.join(directory, 'Makefile'), 'r')
    except IOError:
        return

    lines = fil.readlines()
    fil.close()

    for line in lines:
        if re.match(r'^\s*OB_SOURCES.*', line):
            line = re.sub('OB_SOURCES', '', line)
            line = re.sub('\s*', '', line)
            line = re.sub(':=', '', line)

            if not line == '':
                directory = re.sub(r'\./', '', directory)
                arg.write(directory + '\n')



def gen_ob_make():
    tempfil = tempfile.TemporaryFile()
    os.path.walk('.', walk_callback, tempfil)

    tempfil.seek(0)
    lines = tempfil.readlines()

    obfil = open('PObMakefile', 'w')
    obfil.write('allob:')
    for line in lines:
        obfil.write(' ' + line.strip())
    obfil.write('\n\n')

    for line in lines:
        obfil.write('.PHONY: ' + line.strip() + '\n')
        obfil.write(line.strip() + ':\n')
        obfil.write('\tmake -C ' + line.strip() + ' ob nr=1\n\n')
    
    obfil.close()
    tempfil.close()


def gen_par_make():
    parmake = open('PMakefile.' + C_CPU, 'w')

    fil = open('makefiles.txt', 'r')
    makefiles = fil.readlines()
    fil.close()

    for makefile in makefiles:
        makefile = re.sub(r'\s*', '', makefile)
        makefile = re.sub(r'\./', '', makefile)
        makedir = re.sub(r'Makefile', '', makefile)
        makedir = re.sub(r'/$', '', makedir)

        try:
            fil = open(makefile, 'r')
        except IOError:
            continue

        contents = fil.read()
        fil.close()

        if re.search(r'QNX_LINK', contents, re.MULTILINE):
            print 'Ignoring due to LINK: ' + makefile

        # If LIB_NAME does not exist, add it
        elif not re.search('LIB_NAME', contents, re.MULTILINE):
            add_makefile(makedir)
        else:
            # Check if libname exists. If empty, add the makefile
            if re.search('^\s*LIB_NAME\s*:=\s*$', contents, re.MULTILINE):
                add_makefile(makedir)
            else:
                m = re.search('^\s*LIB_NAME\s*:=\s*(.*)\s*$', contents, re.MULTILINE)
                if not m:
                    raise 'Still not parsed: ' + makefile
                else:
                    libname = m.group(1)

                    if libnames.has_key(libname):
                        olddir = libnames[libname]
                        subdirdeps[olddir] = makedir

                        libnames[libname] = makedir

                    else:
                        libnames[libname] = makedir
                        print 'Adding libname: ' + libname

                    add_makefile(makedir)



    parmake.write('.PHONY: par\n')
    parmake.write('par: ',)

    for makefile in makelist:
        parmake.write(makefile + ' ')

    parmake.write('\n\n')

    for makefile in makelist:
        if makefile == '':
            continue

        parmake.write('.PHONY: ' + makefile + '\n')
        parmake.write(makefile + ':')

        if subdirdeps.has_key(makefile):
            parmake.write(' ' + subdirdeps[makefile])
        parmake.write('\n')

        parmake.write('\techo "make -C ' + makefile + '"\n')
        parmake.write('\tmake -C ' + makefile + ' nr=1 nob=1\n\n')

    parmake.close()



list_makefiles()

gen_ob_make()
gen_par_make()


sys.exit(0)

#========================== Early implementation

os.system('find . -name Makefile | xargs grep LIB_NAME > /tmp/libs.txt')

fil = open('/tmp/libs.txt', 'r')
lines = fil.readlines()
fil.close()

libdir = {}
libdep = {}

makedirs = []


for line in lines:
    if re.match(r'.*:=\s*$', line):
        pass
    else:

        m = re.match(r'(.*)Makefile:.*:= *(.*)$', line)

        dirname = m.group(1)
        libname = m.group(2)
        libname = re.sub(r'\s*', '', libname)

        # Skip ob
        if re.match(r'.*/ob/$', dirname):
            continue

        # Skip win32
        if re.match(r'.*/win32/$', dirname):
            continue

        # ignore commented libname lines
        if re.search('#\s*LIB_NAME', line):
            continue

        makedirs.append(dirname)

        if m:
            dirname = re.sub(r'\./', '', dirname)
            dirname = re.sub(r'/$', '', dirname)
            libdir.setdefault(libname, []).append(dirname)

        else:
            raise 'Parsing failed'

print libdir

STATE_LINK       =  3
STATE_VARIABLE   =  4

for makedir in makedirs:
    fil = open(makedir + '/Makefile', 'r')
    state = STATE_IDLE
    vname = ''
    variables = {}

    # Process this makefile
    #print 'Processing: ' + makedir
    makedir = re.sub('\./', '', makedir)
    makedir = re.sub('/', '_', makedir)
    makedir = re.sub('_$', '', makedir)

    while True:
        if state == STATE_IDLE:
            line = fil.readline()

            if line == '':
                break

            # ignore comments
            if re.match('^#.*', line):
                continue

            m = re.search(r'SUBDIRS(.*)', line)
            #n = re.search(r'QNX_LINK(.*)', line)
            v = re.match(r'(.*) *:=(.*)', line)

            if m:
                state = STATE_SUBDIR
            #elif n:
            #    state = STATE_LINK
            elif v:
                state = STATE_VARIABLE
                vname = v.group(1)
                vname = re.sub(r'\s*', '', vname)

        elif state == STATE_SUBDIR:
            if subdirs.has_key(makedir):
                subdirs[makedir] = subdirs[makedir] + ' ' + line
            else:
                subdirs[makedir] = m.group(1)

            # If there is \ at the end of line stay in SUBDIR state
            # else move to IDLE
            if re.search(r'\\$', line):
                line = fil.readline()
            else:
                state = STATE_IDLE

        elif state == STATE_VARIABLE:
            if variables.has_key(vname):
                variables[vname] = variables[vname] + ' ' + line
            else:
                variables[vname] = v.group(2)

            variables[vname] = re.sub(r'\\', '', variables[vname])
            variables[vname] = re.sub(r'\n', '', variables[vname])
            variables[vname] = re.sub(r'\t', '', variables[vname])
            variables[vname] = re.sub(r' +', ' ', variables[vname])
            variables[vname] = re.sub(r'^\s', '', variables[vname])
            variables[vname] = re.sub(r'-Wl', '', variables[vname])
            variables[vname] = re.sub(r'-\(', '', variables[vname])
            variables[vname] = re.sub(r'-\)', '', variables[vname])

            # If there is \ at the end of line stay in LINK state
            # else move to IDLE

            if re.search(r'\\$', line):
                line = fil.readline()
            else:
                state = STATE_IDLE

            
    # Update dependencies
    print variables
    libname = variables['LIB_NAME']

    if variables.has_key(libname + '_QNX_LINK'):
        print 'Dependency: ' + libname + ' -> ' + variables[libname + '_QNX_LINK']
    else:
        print 'Dependency: ' + libname + ' -> None'

    fil.close()


#print linkdeps


#        elif state == STATE_LINK:
#            if linkdeps.has_key(makedir):
#                linkdeps[makedir] = linkdeps[makedir] + ' ' + line
#            else:
#                linkdeps[makedir] = n.group(1)
#
#            linkdeps[makedir] = re.sub(r'\\', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'-l', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'-Wl', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'-\(', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'-\)', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'\n', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'\t', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r':=', '', linkdeps[makedir])
#            linkdeps[makedir] = re.sub(r'=', '', linkdeps[makedir])
#
#            # If there is \ at the end of line stay in LINK state
#            # else move to IDLE
#            if re.search(r'\\$', line):
#                line = fil.readline()
#            else:
#                state = STATE_IDLE
#
