### Downloading files from github :
* Create a directory for project and download all the files. Follow these steps :
```
mkdir 100TeV
cd 100TeV
module load git
git init
git pull https://github.com/preritj/100TeVsetup.git
```

### Installing Madgraph :
* Download madgraph from the web in some other directory : 
```
wget https://launchpad.net/mg5amcnlo/2.0/2.3.0/+download/MG5_aMC_v2.3.3.tar.gz 
tar -zxvf MG5_aMC_v2.3.3.tar.gz
```

* To include S<sub>T</sub>  cut, some madgraph files need to be modified. I have placed these modified files (with paths) in `MadGraph` directory, replace your original MadGraph files with the ones included here. You can do this in one step as follows from your `100TeV` project directory:
```
cp -r Madgraph/* <your_Madgraph_directory>/ 
``` 

* Finally check that everything works. Go to `<your_Madgraph_directory>` and try:
```
./bin/mg5_aMC
```
and test a simple test process : 
```
generate p p > z
output test
quit
```

### Installing Pythia 6 :
* If the above step works, install Pythia 6 inside Madgraph by issuing the following command at *Madgraph prompt* (i.e. after running `./bin/mg5_aMC` )
```
install pythia-pgs
```

### Installing Delphes :

* First, we need to install `tcl` 
```
wget http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz
tar -zxvf tcl8.6.5-src.tar.gz
```
* Since we don't have root permission, install `tcl` in some `<install_directory>`. Follow these steps
```
cd tcl8.6.5/unix
./configure --prefix=<install_directory>
make 
make install
```

* Add `tcl` path to bashrc. Open `~/.bashrc` and add following lines to the file :
```
export PATH=<your_tcl_install_directory>/bin:$PATH
export LD_LIBRARY_PATH=<your_tcl_install_directory>/lib:$LD_LIBRARY_PATH
``` 
Close the file and do 
```
source ~/.bashrc
```

* Next we want to install Delphes, but outside Madgraph to get the latest version. Do the following steps *outside* of your Madgraph directory :
```
wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.3.2.tar.gz
tar -zxvf Delphes-3.3.2.tar.gz
```

* Delphes requires `root`, which is installed in the cluster *but* it has to be loaded. To load `root`, use the following command in terminal :
```
module load root/5.34
``` 

* Now install Delphes. Go inside the Delphes directory and do :
```
./configure
make
```

* One last step, we have to make Madgraph aware of the Delphes path. Open the file `input/mg5_configuration.txt` in the Madgraph directory. Then, uncomment and edit the following line 
```
delphes_path = <your Delphes directory>
``` 


### Generating events :
* First edit the `config` file and set your username, process and your Madgraph directory path. 
Feel free to edit `MGrun.sh` to set your run time, memory usage, etc. I have already set them to optimal values
* To generate events, do :
```
sbatch MGrun.sh
```
* You can check if your job is running by issuing the command 
```
myq
``` 
* You can have a look at the status of your run using the following command from your `100TeV` project directory :
```
tail -100 MGrun.out
```
* The root files will be stored in `data/<username>/100TeV/`
* In case the runs are not completed in time, rerun the `MGrun.sh` script. It will resume event generation from the previous run.
* To cancel a job, use :
```
scancel <job_ID>
```
where `<job_ID>` can be viewed by issuing the command `myq`

