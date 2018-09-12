# cheyenne-cheatsheet

## 1. Glade Quota: `gladequota`
```
abanihi@cheyenne1: ~ $ gladequota 
Current GLADE space usage: abanihi

  Space                                 Used       Quota    % Full      # Files
---------------------------------- ----------- ----------- --------- -----------
/glade/scratch/abanihi                 0.00 TB    10.00 TB    0.00 %           4
/glade/work/abanihi                    0.64 GB  1024.00 GB    0.06 %       14098
/glade/scratch_old/abanihi             0.00 TB    10.00 TB    0.00 %         741
/glade/p_old/work/abanihi              0.00 GB   512.00 GB    0.00 %           1
/glade/u/home/abanihi                  1.54 GB    50.00 GB    3.08 %       19414

/glade/scratch  - 38.1% used (5712 TB used out of 15000 TB total)
```

## 2. Using environment modules 

- `module add/remove <software>`
- `module avail`: show all currently-loadable modules 
- `module list` : show loaded modules 
- `module purge` : remove all loaded modules 
- `module save/restore <name>` : create/load a saved set of software 
- `module spider <software>` : search for a particular module

## 3. Interacting with the job schedulers

### 3.1 PBS on Cheyenne

- `qsub <script>` : submit batch job
- `qstat <jobid>` : query job status 
- `qdel <jobid>` : delete/kill a job
- `qinteractive -A <project>` : Run an interactive job 
- `qcmd -A <project> -- cmd.exe` : Run a command on a single compute node 

### 3.2 Slurm on DAV 

- `sbatch <script>` : Submit batch job 
- `squeue -j <jobid>` : query job status
- `scancel <jobid>` : delete/kill a job 
- `execdev -A <project>` : Run interactive job on DAV
- `execca -A <project>` : 
- `execgy -A <project>` : 
- `execgpu -A <project>` :

## 4. Accessing Geyser, and Caldera using the Slurm scheduler

### 4.1. Basic commands for managing jobs when using Slurm 

- `squeue -u $USER`: list your current job
- `scontrol show job <ID>` : examine a job in detail
- `scancel <ID>` : kill a job 

### 4.2. Starting interactive jobs 

- `execgy -a <project>` : run on a geyser node 
- `execca -a <project>` : run on a caldera node 
- `execdav -a <project>` : run on the first available DAV resources (caldera, geyser), regardless of location 


