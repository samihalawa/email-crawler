{pkgs}: {
  deps = [
    pkgs.tree
    pkgs.run
    pkgs.postgresql
    pkgs.openssl
    pkgs.cacert
    pkgs.iana-etc
  ];
}
