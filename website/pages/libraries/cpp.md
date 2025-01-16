# C++ library

The latest version of the quadraturerules C++ library can be installed by running:

```bash
wget https://github.com/mscroggs/quadraturerules/releases/download/{{VERSION}}/cpp_source.tar.gz
mkdir src
tar -xvf cpp_source.tar.gz -C src
mkdir build
cd build
cmake ../src
make
make install
```
