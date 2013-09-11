# coding: utf-8


from distutils.core import setup


doclines = open("README.md").readlines()

setup(name="pimobjects",
      version="0.1",
      author="Osvaldo Santana Neto",
      author_email="osvaldo.neto@titansgroup.com.br",
      license="Apache",
      zip_safe=True,
      url="https://github.com/osantana/pimobjects",
      platforms=["any"],
      packages=["pimobjects"],
      tests_require=["nose==1.3.0"],
      description=doclines[0],
      long_description="\n".join(doclines[2:]),
      classifiers="""
      Development Status :: 5 - Production/Stable
      Environment :: Console
      License :: OSI Approved :: BSD License
      Intended Audience :: Developers
      Natural Language :: English
      Programming Language :: Python
      Operating System :: OS Independent
      Topic :: Text Processing""".strip().splitlines(),
)
