FOCI Tools
==========

Purpose
-------

FOCI Tools are a collection of functions to read output from FOCI experiments and do some simple analysis. 
For example: 
* Load output from NEMO, ECHAM and OpenIFS in an efficient way
* Compute global means on all grids
* Compute sea-ice area and volume

Install
-------

Get source code
```bash
cd /where/you/want/the/repo/to/end/up/
git clone https://github.com/FOCI-OpenIFS/focitools.git
```

Load the `py3_std` environment (see [jupyter_on_HPC_setup_guide](https://git.geomar.de/python/jupyter_on_HPC_setup_guide) for help)
```bash
conda activate py3_std
```

Install FOCI Tools. The preferred way is to do it in editable mode. 
```bash
pip install -e /path/to/focitools/
```

NOTE: Installing in editable mode means you can modify the functions in focitools and then use the modified functions without re-installing the module. However, if you are using a Jupyter notebook you will have to restart your kernel for the changes to take effect. 

How to use
----------

Have a look at the `examples/example_with_FOCI-OpenIFS` notebook. 

Contribute
----------

I'm glad you want to contribute! 

To contribute, please make a new branch and switch to it 
```bash
git branch my_new_branch
git checkout my_new_branch
```
Then do your development on this branch, and merge into the `master` branch later. 

To do (missing features)
------------------------

* Load NEMO data using xorca 
* Methods for runoff mapper
* Methods for MOPS
* Methods for HAMMOZ
* ICON? 

What is a "tool"?
-----------------

A "tool" is (dictionary definition) 
1) a thing used to help perform a job. 
2) a stupid, irritating, or contemptible man.

Sometimes one may consider oneself to be both...

