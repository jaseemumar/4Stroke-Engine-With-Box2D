#! bin/bash/

#~ $(make uninstall)
#~ $(make install)
#~ 
$(./bin/cs296_base)
$(gprof ../bin/cs296_base| python ./gprof2dot.py | dot -Tpng -o output.png)

