{
  description = "Aplicación web para opiniones e información de Ramos FCFM";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
    pre-commit-hooks.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    pre-commit-hooks,
  }: let
    supportedSystems = ["x86_64-linux"];
    forEachSupportedSystem = f:
      nixpkgs.lib.genAttrs supportedSystems (system:
        f {
          inherit system;
          pkgs = import nixpkgs {inherit system;};
        });
  in {
    packages = forEachSupportedSystem ({pkgs, ...}: let
      fcfm-ramos = pkgs.callPackage ./default.nix {};
    in {
      inherit fcfm-ramos;
      default = fcfm-ramos;
      fcfm-ramos-image = pkgs.dockerTools.buildLayeredImage {
        name = "fcfm-ramos";
        tag = "latest";
        contents = [fcfm-ramos];
      };
    });

    checks = forEachSupportedSystem ({
      pkgs,
      system,
    }: {
      pre-commit-check = pre-commit-hooks.lib.${system}.run {
        src = builtins.path {
          path = ./.;
          name = "fcfm-ramos";
        };
        hooks.alejandra.enable = true;
        hooks.black.enable = true;
        hooks.black.excludes = ["migrations"];
      };
    });

    formatter = forEachSupportedSystem ({pkgs, ...}: pkgs.alejandra);

    devShells = forEachSupportedSystem ({
      pkgs,
      system,
    }: {
      default = pkgs.mkShell {
        inherit (self.checks.${system}.pre-commit-check) shellHook;
        buildInputs = with pkgs; [python312 black];
      };
    });
  };
}
