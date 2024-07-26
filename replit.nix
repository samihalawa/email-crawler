{pkgs}: {
  deps = [
    pkgs.python312Packages.psycopg2
    pkgs.postgresql
    pkgs.openssl
    pkgs.cacert
    pkgs.iana-etc
  ];
}
