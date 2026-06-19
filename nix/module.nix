{
  config,
  lib,
  pkgs,
  ...
}:

let
  cfg = config.services.technical-renaissance;
in
{
  options.services.technical-renaissance = {
    enable = lib.mkEnableOption "the Technical Renaissance webring";

    package = lib.mkOption {
      type = lib.types.package;
      default = pkgs.callPackage ./package.nix { };
      description = "The technical-renaissance package to run.";
    };

    host = lib.mkOption {
      type = lib.types.str;
      default = "127.0.0.1";
      description = "Address the webring listens on.";
    };

    port = lib.mkOption {
      type = lib.types.port;
      default = 8080;
      description = "Port the webring listens on.";
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.technical-renaissance = {
      description = "Technical Renaissance webring";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];

      environment = {
        HOST = cfg.host;
        PORT = toString cfg.port;
      };

      serviceConfig = {
        ExecStart = lib.getExe cfg.package;
        DynamicUser = true;
        Restart = "on-failure";
      };
    };
  };
}
