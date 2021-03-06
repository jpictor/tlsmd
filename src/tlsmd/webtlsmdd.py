#!/usr/bin/python
# coding=UTF-8
## TLS Motion Determination (TLSMD)
## Copyright 2002-2010 by TLSMD Development Group (see AUTHORS file)
## This code is part of the TLSMD distribution and governed by
## its license.  Please see the LICENSE file that should have been
## included as part of this package.

## Python
import os
import sys
import shutil
import time
import string
import random
import traceback
## NOTE: The order of these signals is important!
from signal import SIG_IGN ## Needed for daemon_main()
from signal import SIGUSR1 ## Needed for SignalJob()
from signal import SIGHUP  ## Needed for KillJob()
import signal
import cPickle
#import bsddb
import socket
import xmlrpclib
import SocketServer
import SimpleXMLRPCServer
import urllib
import gzip       ## for fetching PDBs from pdb.org
import StringIO

## pymmlib
from mmLib import FileIO

## TLSMD
from tlsmdlib import conf, const, tls_calcs, email, misc, mysql_support

mysql = mysql_support.MySQLConnect()

def fatal(text):
    sys.stderr.write("[FATAL ERROR] %s\n" % (text))
    raise SystemExit


def SetStructureFile(webtlsmdd, job_id, struct_bin):
    """Creates job directory, saves structure file to the job directory,
    and sets all jdict defaults.
    """
    if not mysql.job_exists(job_id):
        return False

    try:
        os.chdir(conf.TLSMD_WORK_DIR)
    except OSError:
        return "Unable to change to conf.TLSMD_WORK_DIR = '%s'" % (
            conf.TLSMD_WORK_DIR)

    ## NOTE: This is the first place the webserver creates the job directory
    try:
        os.mkdir(job_id)
    except OSError:
        return "Unable to make job directory %s" % (job_id)

    job_dir = os.path.join(conf.TLSMD_WORK_DIR, job_id)
    os.chdir(job_dir)

    try:
        os.mkdir("ANALYSIS")
    except OSError:
        return "Unable to make ANALYSIS sub-directory for job_id: %s" % (
            job_id)

    ## Copy sanity.png from "All atoms" sanity check (in tlsmdlib/webtlsmd.py)
    ## to job_dir
    try:
        src_png_file = "%s/%s.png" % (conf.WEBTMP_PATH, job_id)
        dst_png_file = "%s/%s/sanity.png" % (conf.TLSMD_WORK_DIR, job_id)
        if os.path.exists(src_png_file):
            shutil.copy(src_png_file, dst_png_file)
    except OSError:
        return "Unable to copy sanity.png for job_id: %s" % job_id

    #mysql.job_set_id(job_id)
    #mysql.job_set_header_id(job_id, "test") ## DEBUG

    ## save PDB file
    pdb_filename = conf.PDB_FILENAME
    filobj = open(pdb_filename, "w")
    filobj.write(struct_bin.data)
    filobj.close()

    ## Generate summary/thumb 'struct.png' image
    if conf.THUMBNAIL:
        misc.render_struct(job_dir)

    ## Generate 'struct.r3d' for Raster3D
    if conf.GEN_RAW_GREY:
        misc.generate_raw_grey_struct(job_dir)

    ## set basic properties of the job
    job_url = "%s/%s" % (conf.TLSMD_WORK_URL, job_id)

    log_url = "%s/log.txt" % (job_url)
    log_file = "%s/log.txt" % (job_dir)
    if not os.path.exists(log_file):
        open(log_file, 'w').close() ## touch log.txt

    #tarball_url       = "%s/%s.tar.gz" % (job_url, job_id)
    analysis_dir      = "%s/ANALYSIS" % (job_dir)
    analysis_base_url = "%s/ANALYSIS" % (job_url)
    analysis_url      = "%s/ANALYSIS/index.html" % (job_url)

    ## TODO: Add version to MySQL status_page table
    #mysql.job_set_version(job_id, const.VERSION)

    ## submission time and initial state
    submit_time = time.time()
    mysql.job_set_state(job_id, "submit1")
    mysql.job_set_submit_time(job_id, submit_time)

    ## This is for internal use only
    tm_struct = time.localtime(submit_time)
    submit_date = time.strftime("%Y-%m-%d %H:%M:%S", tm_struct)
    mysql.job_set_submit_date(job_id, submit_date)

    ## now load the structure and build the submission form
    try:
        struct = FileIO.LoadStructure(fil = pdb_filename)
    except:
        return "The Python Macromolecular Library was unable to load your structure file."

    if not struct.structure_id:
        struct.structure_id = "XXXX"
    mysql.job_set_structure_id(job_id, struct.structure_id)

    ## Select Chains for Analysis
    num_atoms = 0
    num_aniso_atoms = 0
    largest_chain_seen = 0

    chain_descriptions = ""
    chains = []
    for chain in struct.iter_chains():
        naa = chain.count_amino_acids()
        nna = chain.count_nucleic_acids()
        ota = chain.count_fragments()
        num_frags = 0

        ## minimum number of residues (amino/nucleic) per chain
        ## TODO: Does this work better? 2009-07-24
        if naa > 0:
            if naa < conf.MIN_AMINO_PER_CHAIN:
                continue
            num_frags = naa
            largest_chain_seen = max(naa, largest_chain_seen)
        elif nna > 0:
            if nna < conf.MIN_NUCLEIC_PER_CHAIN:
                continue
            num_frags = nna
            largest_chain_seen = max(nna, largest_chain_seen)
        elif naa == 0 and nna == 0:
            ## The chain has neither amino or nucleic acid atoms, so assign
            ## num_frags = ota -> "other atom" types
            num_frags = ota

            ## this chain has nucleic acids in it, so generate r3d file for
            ## just the sugars
            misc.generate_bases_r3d(job_dir, chain.chain_id)
            misc.generate_sugars_r3d(job_dir, chain.chain_id)

        ## TODO: Allow for MIN_NUCLEIC_PER_CHAIN and MIN_AMINO_PER_CHAIN diffs, 2009-07-19
        ## TODO: Record ignored chains (because too small) in logfile, 2009-07-19
        #if num_frags < conf.MIN_RESIDUES_PER_CHAIN:
        #if naa < conf.MIN_AMINO_PER_CHAIN or nna < conf.MIN_NUCLEIC_PER_CHAIN:
        #if (naa > 0 and naa < conf.MIN_AMINO_PER_CHAIN) or\
        #   (nna > 0 and nna < conf.MIN_NUCLEIC_PER_CHAIN):
        #    #log_file = open(log_file, 'w+')
        #    #log_file.write("Ignoring chain %s; too small" % chain.chain_id)
        #    #log_file.close()
        #    continue

        ## create chain description labels
        ## E.g., chains_descriptions = "A:10:0:aa;B:20:1:na;C:30:0:na;"
        chain_descriptions = chain_descriptions + chain.chain_id + ":"
        if naa > 0:
            chain_descriptions = chain_descriptions + str(num_frags) + ":1:aa;"
        elif nna > 0:
            chain_descriptions = chain_descriptions + str(num_frags) + ":1:na;"
        else:
            chain_descriptions = chain_descriptions + str(num_frags) + ":0:ot;"

        for atm in chain.iter_all_atoms():
            num_atoms += 1
            if atm.U is not None:
                num_aniso_atoms += 1

    if num_atoms < 1:
        webtlsmdd.remove_job(job_id)
        return 'Your submitted structure contained no atoms'

    if largest_chain_seen > conf.LARGEST_CHAIN_ALLOWED:
        webtlsmdd.remove_job(job_id)
        return 'Your submitted structure contained a chain exceeding the %s residue limit' % (
            conf.LARGEST_CHAIN_ALLOWED)

    mysql.job_set_chain_sizes(job_id, chain_descriptions)

    ## set defaults
    mysql.job_set_user_name(job_id, "")
    mysql.job_set_email(job_id, "")
    mysql.job_set_user_comment(job_id, conf.globalconf.user_comment)
    mysql.job_set_plot_format(job_id, "PNG")
    mysql.job_set_nparts(job_id, conf.globalconf.nparts)
    mysql.job_set_via_pdb(job_id, "0")

    mysql.job_set_private_job(job_id, "0")
    mysql.job_set_jmol_view(job_id, "0")
    mysql.job_set_jmol_animate(job_id, "0")
    mysql.job_set_histogram(job_id, "0")
    mysql.job_set_cross_chain_analysis(job_id, "0")
    if conf.PRIVATE_JOBS:
        mysql.job_set_private_job(job_id, "1")
    if conf.globalconf.generate_jmol_view:
        mysql.job_set_jmol_view(job_id, "1")
    if conf.globalconf.generate_jmol_animate:
        mysql.job_set_jmol_animate(job_id, "1")
    if conf.globalconf.generate_histogram:
        mysql.job_set_histogram(job_id, "1")
    if conf.globalconf.cross_chain_analysis:
        mysql.job_set_cross_chain_analysis(job_id, "1")

    try:
        aniso_ratio = float(num_aniso_atoms) / float(num_atoms)
    except ZeroDivisionError:
        return 'Your submitted structure contained no atoms'

    if aniso_ratio > conf.ANISO_RATIO:
        mysql.job_set_tls_model(job_id, "ANISO")
    else:
        mysql.job_set_tls_model(job_id, "ISOT")

    mysql.job_set_weight_model(job_id, "NONE")
    mysql.job_set_include_atoms(job_id, "ALL")

    return ""

def RequeueJob(webtlsmdd, job_id):
    """Pushes job to the end of the list.
    """
    ## FIXME: This will no longer work! The BerkeleyDB code has been removed
    ## and now we must use MySQL, 2009-06-29
    if mysql.job_get_state(job_id) == 'running':
        return False
    else:
        return False ## temp. until fixed, 2009-07-01
        #gdict = webtlsmdd.jobdb.retrieve_globals()
        #job_num = gdict['next_job_num']
        #gdict['next_job_num'] = job_num + 1
        #webtlsmdd.jobdb.store_globals(gdict)
        #webtlsmdd.jobdb.job_data_set(job_id, 'job_num', job_num)
        #return True

def RemoveJob(webtlsmdd, job_id):
    """Removes the job from both the database and working directory.
    If job is still running when this function is called, it will first call
    KillJob(), then remove the associated data and files.
    """
    if not mysql.job_exists(job_id):
        return False

    try:
        job_dir = os.path.join(conf.TLSMD_WORK_DIR, job_id)
        shutil.rmtree(job_dir)
    except:
        return False

    ## TODO: Also delete data in 'pdb_list' and 'via_pdb' tables, _if_ they
    ## were submitted via pdb.org. 2010-04-01
    mysql.delete_jdict(job_id)
    return True

def SignalJob(webtlsmdd, job_id):
    """Causes a job stuck on a certain task to skip that step and move on to
    the next step. It will eventually have a state "warnings".
    """
    ## FIXME: Doesn't seem to work, 2009-06-12
    if not mysql.job_exists(job_id):
        return False

    job_dir = os.path.join(conf.TLSMD_WORK_DIR, job_id)
    if job_dir and os.path.isdir(job_dir):
        try:
            pid = int(mysql.job_get_pid(job_id))
        except:
            return False
        try:
            ## Send signal SIGUSR1 and try to continue to job process.
            os.kill(pid, SIGUSR1)
            os.waitpid()
        except:
            return False

    return True

def KillJob(webtlsmdd, job_id):
    """Kills jobs in state "running" by pid and moves them to the
    "Completed Jobs" section as "killed" state.
    """
    ## FIXME: We want to keep the job_id around in order to inform the user
    ## that their job has been "killed", 2009-05-29

    if not mysql.job_exists(job_id):
        return False

    job_dir = os.path.join(conf.TLSMD_WORK_DIR, job_id)
    if job_dir and os.path.isdir(job_dir):
        try:
            if mysql.job_get_pid(job_id) == None:
                sys.stderr.write("[WARNING]: Could not find job pid in database for job_id: %s\n" % job_id)
                return False
            else:
                pid = int(mysql.job_get_pid(job_id))
                sys.stderr.write("[NOTE]: Found pid='%s' for job_id: %s\n" % (pid, job_id))
        except:
            sys.stderr.write("[ERROR]: Could not connect to database for job_id: %s\n" % job_id)
            return False
        try:
            os.kill(pid, SIGHUP)
            os.waitpid()
            sys.stderr.write("[NOTE]: Killing pid for job_id: %s\n" % job_id)
        except:
            sys.stderr.write("[ERROR]: Could not kill pid for job_id: %s\n" % job_id)
            return False

    return True

def Refmac5RefinementPrep(job_id, struct_id, chain_ntls, wilson):
    """Called with a list of tuples (job_id, struct_id, [chain_id, ntls], wilson).
    Generates PDB and TLSIN files for refinement with REFMAC5 + PHENIX.
    Returns a single string if there is an error, otherwise a
    dictionary of results is returned.
    """
    try:
        struct_id = mysql.job_get_structure_id(job_id)
    except:
        return "Could not find the directory related to job_id: %s" % job_id

    if mysql.job_get_via_pdb(job_id) == 1:
        ## If a job was submitted via pdb.org, the results/analyses files are
        ## in a different directory/path and so does the URL.
        pdb_id = struct_id
        job_dir = os.path.join(conf.WEBTLSMDD_PDB_DIR, pdb_id)
        job_url = os.path.join(conf.TLSMD_PUBLIC_URL, "pdb", pdb_id)
        analysis_dir = os.path.join(job_dir, "ANALYSIS")
        analysis_base_url = "%s/ANALYSIS" % (job_url)
    else:
        ## User-submitted (non-pdb.org) results/analyses files are in the
        ## standard place (aka directory/path/url) and are deleted every
        ## DELETE_DAYS (see webtlsmdcleanup.py) days.
        job_dir = os.path.join(conf.TLSMD_WORK_DIR, job_id)
        job_url = os.path.join(conf.TLSMD_PUBLIC_URL, "jobs", job_id)
        analysis_dir = os.path.join(job_dir, "ANALYSIS")
        analysis_base_url = "%s/ANALYSIS" % (job_url)

    if not os.path.isdir(analysis_dir):
        return "Job analysis directory does not exist: %s" % analysis_dir

    old_dir = os.getcwd()
    os.chdir(analysis_dir)

    ## input structure
    pdbin = "%s.pdb" % (struct_id)
    if not os.path.isfile(pdbin):
        pdbin = None
        for pdbx in glob.glob("*.pdb"):
            if len(pdbx) == 8:
                struct_id = pdbx[:4]
                pdbin = pdbx
                break
        if pdbin is None:
            os.chdir(old_dir)
            return "Input PDB File %s Not Found" % (pdbin)

    ## the per-chain TLSOUT files from TLSMD must be merged
    tlsins = []
    for chain_id, ntls in chain_ntls:
        tlsin = "%s_CHAIN%s_NTLS%d.tlsout" % (struct_id, chain_id, ntls)
        if not os.path.isfile(tlsin):
            os.chdir(old_dir)
            return "Input TLSIN File %s Not Found" % (tlsin)
        tlsins.append(tlsin)

    job_num = job_id.split("_")[0]
    secure_dir = job_id.split("_")[1]

    if not os.path.exists(secure_dir):
        os.mkdir(secure_dir)

    ## form unique pdbout/tlsout filenames from job_id
    pdbout1 = "%s/%s_TLS+Biso.pdb" % (secure_dir, job_num)
    pdbout2 = "%s/%s_pureTLS.pdb" %  (secure_dir, job_num)

    ## the tlsout from this program is going to be the tlsin
    ## for refinement, so it's important for the filename to have
    ## the tlsin extension so the user is not confused
    tlsout1 = "%s/%s_TLS+Biso.tlsin" % (secure_dir, job_num)
    tlsout2 = "%s/%s_pureTLS.tlsin"  % (secure_dir, job_num)
    phenix  = "%s/%s.phenix" % (secure_dir, job_num)

    ## make urls for linking
    pdbout_url1 = "%s/%s" % (analysis_base_url, pdbout1)
    pdbout_url2 = "%s/%s" % (analysis_base_url, pdbout2)
    tlsout_url1 = "%s/%s" % (analysis_base_url, tlsout1)
    tlsout_url2 = "%s/%s" % (analysis_base_url, tlsout2)
    phenix_url  = "%s/%s" % (analysis_base_url, phenix)

    ## create the REFMAC/PHENIX files
    tls_calcs.refmac5_prep(pdbin, tlsins, pdbout1, tlsout1)
    tls_calcs.phenix_prep(pdbin, tlsins, phenix)
    tls_calcs.refmac_pure_tls_prep(pdbin, tlsins, wilson, pdbout2, tlsout2)

    os.chdir(old_dir)

    return dict(pdbout1 = pdbout1,
                pdbout_url1 = pdbout_url1,
                pdbout2 = pdbout2,
                pdbout_url2 = pdbout_url2,
                tlsout1 = tlsout1,
                tlsout_url1 = tlsout_url1,
                tlsout2 = tlsout2,
                tlsout_url2 = tlsout_url2,
                phenix = phenix,
                phenix_url = phenix_url)


class WebTLSMDDaemon():
    def __init__(self):
        self.jobdb = None

    def set_structure_file(self, job_id, struct_bin):
        """Creates job directory, saves structure file to the job directory,
        and sets all jdict defaults.
        """
        return SetStructureFile(self, job_id, struct_bin)

    def remove_job(self, job_id):
        """Removes the job from both the database and working directory.
        If job is still running when this function is called, it will first call
        KillJob(), then remove the associated data and files.
        """
        try:
            KillJob(self, job_id)
        except:
            pass
        return RemoveJob(self, job_id)

    def delete_job(self, job_id):
        """Removes/Deletes the job from both the database and working directory.
        Note that this will only be called for jobs that are no longer running.
        """
        return RemoveJob(self, job_id)

    def signal_job(self, job_id):
        """Signals a job stuck on a certain task to skip that step and move on
        to the next step. It will eventually have a state 'warnings'.
        """
        return SignalJob(self, job_id)

    def kill_job(self, job_id):
        """Kills jobs in state 'running' by pid and moves them to the
        'Completed Jobs' section as 'killed' state.
        """
        return KillJob(self, job_id)

    def requeue_job(self, job_id):
        """Pushes the job to the back of the queue.
        """
        return RequeueJob(self, job_id)

    def refmac5_refinement_prep(self, job_id, struct_id, chain_ntls, wilson):
        """Called with a list of tuples (job_id, struct_id, [chain_id, ntls], wilson).
        Generates PDB and TLSIN files for refinement with REFMAC5 + PHENIX.
        Returns a single string if there is an error, otherwise a
        dictionary of results is returned.
        """
        return Refmac5RefinementPrep(job_id, struct_id, chain_ntls, wilson)

    def fetch_pdb(self, pdbid):
        """Retrieves the PDB file from RCSB.
        """
        try:
            cdata = urllib.urlopen("%s/%s.pdb.gz" % (conf.GET_PDB_URL,pdbid)).read()
            sys.stdout.write("FOUND PDB: %s" % pdbid)
            data = gzip.GzipFile(fileobj = StringIO.StringIO(cdata)).read()
        except IOError:
            return xmlrpclib.Binary("")
        return xmlrpclib.Binary(data)


class WebTLSMD_XMLRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Override the standard XMLRPC request handler to open the database before
    calling the method.
    """
    ## TODO: Can this be removed? 2009-06-01
    def handle(self):
        #self.server.webtlsmdd.jobdb = JobDatabase(self.server.webtlsmdd.db_file)
        return SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.handle(self)


class WebTLSMD_XMLRPCServer(
            SocketServer.ForkingMixIn,
            SimpleXMLRPCServer.SimpleXMLRPCServer):
    """Use customized XMLRPC server which forks for requests and uses the
    customized request handler.
    """
    def __init__(self, host_port):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(
            self,
            host_port,
            WebTLSMD_XMLRPCRequestHandler,
            False)


def daemon_main():
    rtype, baseurl, port = conf.WEBTLSMDD.split(":")
    host_port = ("localhost", int(port))

    sys.stdout.write("STARTING webtlsmdd.py DAEMON..................: %s\n" % misc.timestamp())
    sys.stdout.write("webtlsmdd.py xmlrpc server version............: %s\n" % (const.VERSION))
    sys.stdout.write("listening for incoming connections at URL.....: %s\n" % (conf.WEBTLSMDD))
    sys.stdout.write("job (working) directory.......................: %s\n" % (conf.TLSMD_WORK_DIR))

    os.chdir(conf.TLSMD_WORK_DIR)

    ## Switched from handle_SIGCHLD to SIG_IGN. Christoph Champ, 2008-03-10
    signal.signal(signal.SIGCHLD, SIG_IGN)

    webtlsmdd = WebTLSMDDaemon()

    try:
        xmlrpc_server = WebTLSMD_XMLRPCServer(host_port)
    except socket.error:
        sys.stderr.write("[ERROR] unable to bind to host,port: %s\n" % (str(host_port)))
        raise SystemExit

    xmlrpc_server.webtlsmdd = webtlsmdd
    xmlrpc_server.register_instance(webtlsmdd)
    xmlrpc_server.serve_forever()

def main():
    try:
        daemon_main()
    except:
        email.SendTracebackEmail("webtlsmdd.py exception")
        raise

def inspect():
    mysql = mysql_support.MySQLConnect()

    if sys.argv[1] == "list":
        for dbkey in mysql.job_list():
            print dbkey["jobID"], dbkey["job_id"], dbkey["submit_date"]

    ## FIXME: This does not work yet. 2010-07-02
    if sys.argv[1] == "remove":
        print "This option does not work yet."

def usage():
    print "webtlsmdd.py [list | remove] args..."

if __name__=="__main__":
    if len(sys.argv) == 1:
        try:
            main()
        except KeyboardInterrupt:
            raise SystemExit
    else:
        inspect()
    sys.exit(0)
