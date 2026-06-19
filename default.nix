let
  sources = import ./npins;
  pkgs = import sources.nixpkgs { };
in
{
  packages.default = pkgs.callPackage ./nix/package.nix { inherit sources; };
  nixosModules.default = import ./nix/module.nix;
  overlays.default = final: _prev: {
    technical-renaissance = final.callPackage ./nix/package.nix { inherit sources; };
  };
}
