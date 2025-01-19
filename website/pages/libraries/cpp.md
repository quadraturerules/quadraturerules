# C++ library

The source code of the quadraturerules C++ library can be downloaded from the
[latest release on GitHub](https://github.com/mscroggs/quadraturerules/releases/latest/).
It can be installed by running:

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

Once the library is installed, you can run the tests by running:

```bash
python src/test/run_tests.py
```

Or you can run individual tests:

```bash
cd src/test/{TEST_NAME}
cmake .
make .
./{TEST_NAME}
```
