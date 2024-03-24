{
  python312,
  fetchPypi,
}: let
  packageOverrides = final: prev: {
    pyrebase4 = let
      pname = "Pyrebase4";
      version = "4.7.1";
    in
      prev.buildPythonPackage {
        inherit pname version;
        src = fetchPypi {
          inherit pname version;
          hash = "sha256-Jw9oJ9ADnZiEYiLJ8mZGumxAHNibfAOMOr429IAdd1Q=";
        };
        format = "wheel";
      };
    firebase-admin = let
      pname = "firebase-admin";
      version = "6.4.0";
    in
      prev.buildPythonPackage {
        inherit pname version;
        src = fetchPypi {
          inherit version;
          pname = "firebase_admin";
          hash = "sha256-Ssg+4Aq+aEmLnwjXAbVQp3s6We+6YQqeL7PXsVFRZsY=";
        };
        format = "wheel";
      };
  };
  python = python312.override {
    inherit packageOverrides;
    self = python;
  };
  pythonPkgs = python.pkgs;
in
  python.pkgs.buildPythonApplication {
    pname = "fcfm-ramos";
    version = "0.0.1";
    src = builtins.path {
      path = ./.;
      name = "fcfm-ramos";
    };
    format = "pyproject";
    nativeBuildInputs = with pythonPkgs; [flit-core]; # actual build inputs
    buildInputs = with pythonPkgs; [flask flask-wtf pyrebase4 firebase-admin]; # runtime dependencies
  }
