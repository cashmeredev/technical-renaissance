{
  python3Packages,
  sources ? import ../npins,
}:

let
  rustimport = python3Packages.buildPythonPackage {
    pname = "rustimport";
    version = "1.3.4";
    pyproject = true;
    src = sources.rustimport;
    build-system = [ python3Packages.setuptools ];
    dependencies = [ python3Packages.toml ];
    doCheck = false;
  };

  robyn = python3Packages.buildPythonPackage {
    pname = "robyn";
    version = "0.86.0";
    format = "wheel";
    src = sources.robyn;
    dependencies = with python3Packages; [
      inquirerpy
      multiprocess
      orjson
      rustimport
      uvloop
      watchdog
      jinja2
    ];
    doCheck = false;
  };
in
python3Packages.buildPythonApplication {
  pname = "technical-renaissance";
  version = "0.1.0";
  pyproject = true;
  src = ../.;

  build-system = [ python3Packages.uv-build ];
  dependencies = [ robyn ];

  doCheck = false;

  meta = {
    description = "Webring for the #technicalrenaissance IRC channel";
    mainProgram = "technical-renaissance";
  };
}
