{pkgs}: {
  deps = [
    pkgs.postgresql
    pkgs.openssl
    pkgs.cacert
    pkgs.iana-etc
  ];
}
