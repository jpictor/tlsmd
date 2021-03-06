#!/usr/bin/python
## TLS Motion Determination (TLSMD)
## Copyright 2002-2010 by TLSMD Development Group (see AUTHORS file)
## This code is part of the TLSMD distribution and governed by
## its license.  Please see the LICENSE file that should have been
## included as part of this package.

## Python modules
import re
#import MySQLdb

## TLSMD
import conf, misc

class MySQLConnect():
    def __init__(self):
        ## TODO: Add fail-safe
        self.db = mysql_connect()
        self.user_data_tbl = "user_data"
        self.status_page_tbl = "status_page"
        self.via_pdb_tbl = "via_pdb"
        self.pdb_list_tbl = "pdb_list"
        self.archive_tbl = "archive"

    def execute_cmd(self, string, dict = None, list = None, select = None):
        self.db.ping()
        error = ''
        try:
            if dict:
                cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            else:
                cursor = self.db.cursor()
            cursor.execute(string)
            if list or dict:
                rows = cursor.fetchall()
            elif select:
                rows = cursor.fetchone()
            else:
                rows = cursor.fetchall()
            cursor.close()
        except MySQLdb.Error, e:
            ## FIXME: This error message should be logged
            error = ("ERROR: %d: %s" % (e.args[0], e.args[1]))
            #self.db.commit()
            if select:
                return None
            else:
                return False

        self.db.commit()
        if rows == None or len(rows) == 0:
            return None
        elif list:
            return rows
        elif select:
            return rows[0]
        else:
            return True

    def retrieve_jdict(self, job_id):
        assert job_id.startswith("TLSMD")

    def archive_old_jobs(self, job_id):
        assert job_id.startswith("TLSMD")
        if not self.job_exists(job_id):
            return False

        string = """INSERT INTO %s
                 SELECT * FROM %s
                 WHERE job_id='%s';""" % (
            self.archive_tbl, self.status_page_tbl, job_id)
        return self.execute_cmd(string)

    def archive_pdb_jobs(self, job_id):
        assert job_id.startswith("TLSMD")
        if not self.job_exists(job_id):
            return False
        string = """INSERT INTO %s
                 SELECT * FROM %s
                 WHERE job_id='%s';""" % (
            self.pdb_list_tbl, self.status_page_tbl, job_id)
        return self.execute_cmd(string)

    def delete_jdict(self, job_id):
        assert job_id.startswith("TLSMD")
        if not self.job_exists(job_id):
            return False
        string = "DELETE FROM %s WHERE job_id='%s';" % (
            self.status_page_tbl, job_id)
        return self.execute_cmd(string)

    def job_new(self):
        ## NOTE: This must always be the first function called for every new
        ## job sumbitted

        ## Get largest job_num so far and increment
        string = "SELECT MAX(job_num) FROM %s;" % (
            self.status_page_tbl)
        max_num = self.execute_cmd(string, dict = False, select = True)
        if max_num:
            job_num = int(max_num) + 1
        else:
            job_num = 1001

        ## assign job_id
        security_code = misc.generate_security_code()
        job_id = "TLSMD%d_%s" % (job_num, security_code)

        ## store new and unique job_id
        string = "INSERT INTO %s (job_num,job_id) VALUES('%s','%s');" % (
            self.status_page_tbl, job_num, job_id)
        self.execute_cmd(string)

        return job_id

    def job_exists(self, job_id):
        string = "SELECT job_id FROM %s WHERE job_id='%s';" % (
            self.status_page_tbl, job_id)
        return self.execute_cmd(string)

    def job_list(self):
        string = "SELECT * FROM %s ORDER BY JobID DESC;" % (
            self.status_page_tbl)
        return self.execute_cmd(string, dict = True, list = True, select = True)

    def job_pdb_list(self):
        string = "SELECT * FROM %s ORDER BY JobID DESC;" % (
            self.pdb_list_tbl)
        return self.execute_cmd(string, dict = True, list = True, select = True)

    def pdb_exists(self, pdb_id):
        string = "SELECT pdb_id FROM %s WHERE pdb_id='%s';" % (
            self.via_pdb_tbl, pdb_id)
        return self.execute_cmd(string, dict = False, select = True)

    def set_pdb_db(self, pdb_id):
        string = "INSERT INTO %s (%s) VALUES('%s');" % (
            self.via_pdb_tbl, "pdb_id", pdb_id)
        return self.execute_cmd(string)

    def get_next_queued_job_id(self):
        job_list = self.job_list()
        for jdict in job_list:
            if jdict.get("state") == "queued":
                return jdict["job_id"]
        return ""

    def user_data_list(self, job_id):
        string = "SELECT * FROM %s WHERE job_id='%s';" % (
            self.status_page_tbl, job_id)
        v = self.execute_cmd(string, dict = True, select = True)
        if v == None:
            return None
        else:
            return v

    def job_get_dict(self, job_id):
        string = "SELECT * FROM %s WHERE job_id='%s';" % (
            self.status_page_tbl, job_id)
        return self.execute_cmd(string, dict = True, select = True)

    def job_data_set(self, job_id, column, value):
        string = "UPDATE %s SET %s='%s' WHERE job_id='%s';" % (
            self.status_page_tbl, column, value, job_id)
        return self.execute_cmd(string)

    def job_data_get(self, job_id, column, dict):
        string = "SELECT %s FROM %s WHERE job_id='%s';" % (
            column, self.status_page_tbl, job_id)

        if dict == False:
            return self.execute_cmd(string, dict, select = True)

        ## Check the current ("status_page") for the job_id
        v = self.execute_cmd(string, dict, select = True)

        if v == None:
            ## job_id is probably too old, so let's check the archive
            string = "SELECT %s FROM %s WHERE job_id='%s';" % (
                column, self.archive_tbl, job_id)
            v = self.execute_cmd(string, dict, select = True)

            if v == None:
                ## Not found in archive
                return None
            else:
                ## Good! We found the job_id in the archive
                return v[column]
        else:
            ## Good! We found the job_id in the current status_page
            return v[column]

    def job_set_pid(self, job_id, pid):
        return self.job_data_set(job_id, "pid", pid)

    def job_get_pid(self, job_id):
        return self.job_data_get(job_id, "pid", dict = True)

    def job_set_submit_time(self, job_id, submit_time):
        return self.job_data_set(job_id, "submit_time", submit_time)

    def job_set_submit_date(self, job_id, submit_date):
        ## This is for internal use only
        return self.job_data_set(job_id, "submit_date", submit_date)

    def job_set_run_time_begin(self, job_id, run_time_begin):
        return self.job_data_set(job_id, "run_time_begin", run_time_begin)

    def job_set_run_time_end(self, job_id, run_time_end):
        return self.job_data_set(job_id, "run_time_end", run_time_end)

    def job_set_state(self, job_id, state):
        return self.job_data_set(job_id, "state", state)

    def job_get_state(self, job_id):
        return self.job_data_get(job_id, "state", dict = True)

    def job_set_via_pdb(self, job_id, bool):
        return self.job_data_set(job_id, "via_pdb", bool)

    def job_get_via_pdb(self, job_id):
        return self.job_data_get(job_id, "via_pdb", dict = True)

    def job_set_header_id(self, job_id, header_id):
        return self.job_data_set(job_id, "header_id", header_id)

    def job_set_remote_addr(self, job_id, value):
        string = "UPDATE %s SET ip_address='%s' WHERE job_id='%s';" % (
            self.status_page_tbl, value, job_id)
        return self.execute_cmd(string)

    def job_get_remote_addr(self, job_id):
        return self.job_data_get(job_id, "ip_address", dict = True)

    def job_set_email(self, job_id, email_address):
        status = self.job_data_set(job_id, "email", email_address)
        return status

    def job_get_email(self, job_id):
        return self.job_data_get(job_id, "email", dict = True)

    def job_set_user_name(self, job_id, user_name):
        return self.job_data_set(job_id, "user_name", user_name)

    def job_get_user_name(self, job_id):
        return self.job_data_get(job_id, "user_name", dict = True)

    def job_set_structure_id(self, job_id, structure_id):
        return self.job_data_set(job_id, "structure_id", structure_id)

    def job_get_structure_id(self, job_id):
        return self.job_data_get(job_id, "structure_id", dict = True)

    def job_set_user_comment(self, job_id, user_comment):
        return self.job_data_set(job_id, "user_comment", user_comment)

    def job_get_user_comment(self, job_id):
        return self.job_data_get(job_id, "user_comment", dict = True)

    def job_set_private_job(self, job_id, private_job):
        return self.job_data_set(job_id, "private_job", private_job)

    def job_get_private_job(self, job_id):
        return self.job_data_get(job_id, "private_job", dict = True)

    def job_set_chain_sizes(self, job_id, chain_sizes):
        return self.job_data_set(job_id, "chain_sizes", chain_sizes)

    def job_get_chain_sizes(self, job_id):
        return self.job_data_get(job_id, "chain_sizes", dict = True)

    def job_set_tls_model(self, job_id, tls_model):
        return self.job_data_set(job_id, "tls_model", tls_model)

    def job_get_tls_model(self, job_id):
        return self.job_data_get(job_id, "tls_model", dict = True)

    def job_set_weight_model(self, job_id, weight_model):
        return self.job_data_set(job_id, "weight", weight_model)

    def job_set_include_atoms(self, job_id, include_atoms):
        return self.job_data_set(job_id, "include_atoms", include_atoms)

    def job_set_plot_format(self, job_id, plot_format):
        return self.job_data_set(job_id, "plot_format", plot_format)

    def job_set_jmol_view(self, job_id, generate_jmol_view):
        return self.job_data_set(job_id, "generate_jmol_view", generate_jmol_view)

    def job_set_jmol_animate(self, job_id, generate_jmol_animate):
        return self.job_data_set(job_id, "generate_jmol_animate", generate_jmol_animate)

    def job_set_histogram(self, job_id, generate_histogram):
        return self.job_data_set(job_id, "generate_histogram", generate_histogram)

    def job_set_cross_chain_analysis(self, job_id, cross_chain_analysis):
        return self.job_data_set(job_id, "cross_chain_analysis", cross_chain_analysis)

    def job_set_nparts(self, job_id, nparts):
        return self.job_data_set(job_id, "nparts", nparts)
