## TLS Motion Determination (TLSMD)
## Copyright 2002-2010 by TLSMD Development Group (see AUTHORS file)
## This code is part of the TLSMD distribution and governed by
## its license.  Please see the LICENSE file that should have been
## included as part of this package.
"""Installation settings. When installed to run as a web application, the layout
of the directories from the tlsmd root directory is as follows:

$TLSMD_ROOT/cgi-bin 
$TLSMD_ROOT/jobs     # for user-submitted jobs (not via pdb.org)
$TLSMD_ROOT/pdb      # for jobs submitted via pdb.org
$TLSMD_ROOT/jmol     # Jmol jar files
$TLSMD_ROOT/examples # examples of PDBs showing good results from TLSMD

"""
import os
import time
import const
import console

## BEGIN: ENVIRONMENT VARIABLES CONFIGURATION
os.environ["GDFONTPATH"]             = "/usr/local/share/fonts"
os.environ["GNUPLOT_DEFAULT_GDFONT"] = "verdana"
## END: ENVIRONMENT VARIABLES CONFIGURATION

## BEGIN: CONFIGURATION PATHS AND URLS
BASE_PUBLIC_URL        = "http://skuld.bmsc.washington.edu"
TLSMD_ROOT             = os.environ.get("TLSMD_ROOT", "/home/tlsmd/tlsmd")
TLSMD_WWW_ROOT         = "/home/tlsmd/public_html"
TLSMD_PUBLIC_URL       = "http://skuld.bmsc.washington.edu/~tlsmd"
TLSMD_BASE_URL         = "/~tlsmd"
WEBTLSMDD              = "http://localhost:10100"
#WEBTLSMDD_DATABASE     = "/home/tlsmd/database/webtlsmd.db" ## no longer used
ADMIN_PASSWORD_FILE    = "/home/tlsmd/database/cgi-admin"
MAIL                   = "/bin/mail"
TRACEBACK_EMAIL        = "tlsmdtraceback"
LOG_FILE               = "/home/tlsmd/log/tlsmd_runlog.txt"
RESIDUALS_LOG_FILE     = "/home/tlsmd/log/residuals.log"
PDB_URL                = "http://www.pdb.org/pdb/explore/explore.do?structureId="
GET_PDB_URL            = "http://www.rcsb.org/pdb/files"
## END: CONFIGURATION PATHS AND URLS

## override default configuration
ALTCONF = "/etc/tlsmd.conf"
if os.path.exists(ALTCONF):
    execfile(ALTCONF)

## derived paths
TLSMD_PROGRAM_PATH     = os.path.join(TLSMD_ROOT, "bin", "tlsmd.py")
WEBTLSMD_URL           = "%s/cgi-bin/webtlsmd.cgi" % (TLSMD_PUBLIC_URL)
WEBTMP_PATH            = "/var/www/webtmp"
WEBTMP_URL             = "%s/webtmp" % BASE_PUBLIC_URL
GNUPLOT                = "/usr/local/bin/gnuplot"
GNUPLOT_FONT_PATH      = os.path.join(TLSMD_ROOT, "fonts/LucidaSansOblique.ttf")
GNUPLOT_FONT           = "LucidaSansOblique"
REFINEPREP_URL         = "%s/cgi-bin/refineprep.cgi" % (TLSMD_PUBLIC_URL)
TLSMD_WORK_DIR         = os.path.join(TLSMD_WWW_ROOT, "jobs")
TLSMD_WORK_URL         = "%s/jobs" % (TLSMD_BASE_URL)
JMOL_DIR               = "../../../jmol" # Directory path must be relative, not an absolute URL.
JMOL_PATH              = "/home/tlsmd/tlsmd/bin/jmol"
WEBTLSMDD_PDB_URL      = "%s/pdb" % (TLSMD_PUBLIC_URL)
WEBTLSMDD_PDB_DIR      = os.path.join(TLSMD_WWW_ROOT, "pdb")
WEBTLSMDD_PDBID_FILE   = os.path.join(WEBTLSMDD_PDB_DIR, "pdbids.txt")
FLATFILES_DIR          = "/data/tlsmd/flatfiles"
TLSANIM2R3D            = "/home/tlsmd/tlsmd/bin/tlsanim2r3d"
PDB_ANIMATE_SCRIPT     = "/home/tlsmd/tlsmd/bin/pdb_animate.pl"

## General defaults
MAX_PARALLEL_JOBS     = 4   ## maximum number of parallel jobs allowable at the same time
MAX_JOB_ID_LEN        = 20  ## maximum string length of "job_id" (e.g., "TLSMD15620_CrjLhBTM")
LARGEST_CHAIN_ALLOWED = 1700  ## don't allow any chains with residues larger than this
MIN_AMINO_PER_CHAIN   = 10  ## minimum (amino acid) residues per chain
MIN_NUCLEIC_PER_CHAIN = 5   ## minimum (nucleic acid) residues per chain
NPARTS                = 20  ## maximum number of TLS partitons for each chain (default/max allowed = 20)
PRIVATE_JOBS          = True  ## controls the default "private" settings; overrides form!
PDB_FILENAME          = "struct.pdb"  ## This is the default name given to structures
ADP_PROB              = 50  ## the isoprobability contour level for all visualizations
DEFAULT_WILSON_B      = 20.00 ## controls which default Bfactor is in pure TLS PDBs
MAX_WILSON_B          = 50.00 ## numbers beyond this are...? TODO: Find out, 2010-05-04
ANISO_RATIO           = 0.90  ## aniso_ratio = num_aniso_atoms/num_atoms; sets 
                              ## the tls_model type to "ANISO" if >ANISO_RATIO;
                              ## "ISOT" otherwise (default)

## the pixel width of the TLS visualization rendered ray traces
VIS_WIDTH  = 320 ## default: 320
VIS_HEIGHT = 200 ## default: 200

## sanity checks globals
MIN_STDDEV_BFACT = 0.01
MAX_STDDEV_BFACT = 60.0

## gnuplot globals
GNUPLOT_FONT_SIZE = 10
GNUPLOT_WIDTH     = 640
GNUPLOT_HEIGHT    = 480

## BMean Plot
BMEAN_PLOT_WIDTH  = 640
BMEAN_PLOT_HEIGHT = 300
BMEAN_PLOT_GROUP_TITLES = False

## MySQL global
USE_BDB   = False
USE_MYSQL = True
MYSQL_LOG = False
MYSQL_LOG_FILE = "/home/tlsmd/log/mysql.log"

## These are for selecting only backbone atoms; used in Raster3D
DISPLACE_ATOM_NAME_DICT = {
    "CA": True, "P": True, 
    "O5*": True, "C5*": True, "C4*": True, "C3*": True, "O3*": True,
    "O5'": True, "C5'": True, "C4'": True, "C3'": True, "O3'": True
    }

## the Jmol viewer is a square window, generated with this pixel size
JMOL_SKIP = False ## Toggle switch
JMOL_SIZE = 600
## turn on/off various sections
RENDER_SKIP    = False
REFMAC_SKIP    = False
HISTOGRAM_SKIP = True
GEN_RAW_GREY   = True

## the following are used for the summary/thumb 'struct.png' image.
## These are optional. Uses internal 'parse_molauto.pl' script!
THUMBNAIL      = True  ## (default: False)
MOLAUTO        = "/usr/local/bin/molauto"
PARSE_MOLAUTO_SCRIPT = "/home/tlsmd/tlsmd/bin/parse_molauto.pl"
MOLSCRIPT      = "/usr/local/bin/molscript"
RENDER         = "/usr/local/bin/render"
RENDER_SIZE    = "200x200"
RINGS3D        = "/usr/local/bin/rings3d"
R3D_LIB        = "/usr/local/share/Raster3D/materials"
GREY_R3D_FILE  = os.path.join(R3D_LIB, "grey.r3d")

## turn on/off multi-chain (matrix) analysis
CROSS_CHAIN_ANALYSIS = False ## Under development

class GlobalConfiguration(object):
    def __init__(self):
        self.tls_model = "ISOT"
        self.weight_model = "UNIT"
        self.include_atoms = "ALL"
        self.min_subsegment_size = 4
        self.adp_prob = ADP_PROB
        self.nparts = NPARTS
        self.verbose = False
        self.use_svg = False
        self.skip_html = False
        self.skip_jmol = True
        self.generate_jmol_view = False
        self.generate_jmol_animate = False
        self.generate_histogram = False
        self.cross_chain_analysis = False
        self.user_comment = ""
        self.webtlsmdd = None
        self.job_id = None
        self.struct_id = None
        self.start_time = time.time()
        self.target_struct_path = None
        self.target_struct_chain_id = None
        self.recombination = False
        self.adp_smoothing = 0

    def prnt(self):
        console.stdoutln("TLS Motion Determination (TLSMD) Version %s" % (const.VERSION))
        console.endln()
        console.kvformat("TLS PARAMETER FIT ENGINE", self.tls_model)
        console.kvformat("MIN_SUBSEGMENT_SIZE", self.min_subsegment_size)
        console.kvformat("ATOM B-FACTOR WEIGHT_MODEL", self.weight_model)
        console.kvformat("PROTEIN ATOMS CONSIDERED", self.include_atoms)
        console.endln()

    def verify(self):
        assert self.tls_model     in ["ANISO", "ISOT", "NLANISO", "NLISOT"]
        assert self.weight_model  in ["UNIT", "IUISO"]
        assert self.include_atoms in ["ALL", "MAINCHAIN", "CA"]

globalconf = GlobalConfiguration()

