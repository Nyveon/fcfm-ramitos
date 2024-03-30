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
          hash = "sha256-5UFhI8tUtIP2IjmGvd0CCTkLuLBcIMfmKQjQ2tnc6RE=";
          format = "wheel";
          python = "py3";
          dist = "py3";
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
          hash = "sha256-qgbxnwqoubkp2+XNE2d8m6Bf5/+BlWT0IKrgLGRcYyI=";
          format = "wheel";
          python = "py3";
          dist = "py3";
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
    # actual build inputs
    nativeBuildInputs = with pythonPkgs; [flit-core];
    # runtime dependencies
    propagatedBuildInputs = with pythonPkgs; [
      flask
      flask-wtf
      pyrebase4
      firebase-admin
    ];
  }
