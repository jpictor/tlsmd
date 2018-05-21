from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField
from django.conf import settings

class TLSMDJob(models.Model):
    ## jobID == id
    job_num = models.IntegerField(null=True, blank=True)
    job_id = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    STATE_CHOICES = (
        ('PROVIDER_HOME', 'PROVIDER_HOME'),
        ('VISIT', 'VISIT')
    )
    state = models.CharField(max_length=36, choices=STATE_CHOICES, db_index=True, null=True, blank=True)
    structure_id = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    header_id = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    run_time_begin = models.DateTimeField(null=True, blank=True)
    run_time_end = models.DateTimeField(null=True, blank=True)
    chain_sizes = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    submit_date = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    ip_address = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    email = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    user_name = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    user_comment = models.TextField(max_length=2048, db_index=True, null=True, blank=True)
    private_job = models.BooleanField(default=False)
    via_pdb = models.BooleanField(default=False)
    pid = models.IntegerField(null=True, blank=True)
    TLS_MODELS = (
        ('ISOT', 'Isotropic'),
        ('ANISO', 'Anisotropic')
    )
    tls_model = models.CharField(max_length=36, choices=TLS_MODELS, db_index=True, null=True, blank=True)
    WEIGHTS = (
        ('NONE', 'NONE'),
        ('IUISO', 'IUISO')
    )
    weight = models.CharField(max_length=36, choices=WEIGHTS, db_index=True, null=True, blank=True)
    INCLUDE_ATOMS = (
        ('ALL', 'ALL'),
        ('MAINCHAIN', 'MAINCHAIN')
    )
    include_atoms = models.CharField(max_length=36, choices=INCLUDE_ATOMS, db_index=True, null=True, blank=True)
    PLOT_FORMATS = (
        ('PNG', 'PNG'),
        ('SVG', 'SVG')
    )
    plot_format = models.CharField(max_length=36, choices=PLOT_FORMATS, db_index=True, null=True, blank=True)
    generate_jmol_view = models.BooleanField(default=False)
    generate_jmol_animate = models.BooleanField(default=False)
    generate_histogram = models.BooleanField(default=False)
    cross_chain_analysis = models.BooleanField(default=False)
    nparts = models.IntegerField(null=True, blank=True)
    resolution = models.FloatField(null=True, blank=True)
    data = JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    last_modified = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'tlsmd_job'
        ordering = ['id']

    def __str__(self):
        return '{}:{}'.format(self.type, self.name)

##== Create main 'status_page' table ===========================================
## CREATE TABLE status_page (jobID INT(5) NOT NULL auto_increment, job_num INT(5),
##        job_id VARCHAR(19), state VARCHAR(10), structure_id VARCHAR(4),
##        header_id VARCHAR(4), submit_time DECIMAL(13,2),
##        run_time_begin DECIMAL(13,2), run_time_end DECIMAL(13,2),
##        chain_sizes VARCHAR(255), submit_date VARCHAR(24),
##        ip_address VARCHAR(15), email VARCHAR(320), user_name VARCHAR(100),
##        user_comment VARCHAR(128), private_job BOOLEAN, via_pdb BOOLEAN,
##        pid SMALLINT(5) UNSIGNED, tls_model ENUM('ISOT','ANISO'),
##        weight ENUM('NONE','IUISO'), include_atoms ENUM('ALL','MAINCHAIN'),
##        plot_format ENUM('PNG','SVG'), generate_jmol_view BOOLEAN,
##        generate_jmol_animate BOOLEAN, generate_histogram BOOLEAN,
##        cross_chain_analysis BOOLEAN, nparts INT(2), resolution DECIMAL(4,2),
##        UNIQUE KEY `job_id` (`job_id`), PRIMARY KEY (jobID));
