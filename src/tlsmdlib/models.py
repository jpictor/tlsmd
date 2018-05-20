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
